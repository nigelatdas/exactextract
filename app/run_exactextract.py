# run exactextract process
# eg: exactextract -r "wheat:../hacking/512z_au_crop_yield_2023-10-04.tif[1]" -p ~/system_farms.gpkg -f id --output ../data/full_512z_au_crop_yield_2023-10-04__001.csv -s "sum(wheat)" -s "count(wheat)" -s "rawsum(wheat:0.01)" -s "rawhitcount(wheat:0.01)" -s "rawcount(wheat:0.01)"  --strategy raster-sequential

# import os
import sys

# import argparse
import subprocess

import logging
import boto3
from botocore.exceptions import ClientError
import os
import urllib3
import json


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_config():
    return {
        # /vsis3_streaming/
        "shape_data": "/vsis3/nigel-temp-bucket/system_farms.gpkg",
        # "shape_data": "./data/system_farms.gpkg",
        "shape_id": "id",
        "raster": {
            "path": "/vsis3/nigel-temp-bucket/cog_au_crop_yield_2023-10-04.tif",
            # "path": "./data/cog_au_crop_yield_2023-10-04.tif",
            "bands": [
                {"name": "wheat", "band": "1", "stats": ["sum", "count", "area"]},
                {"name": "barley", "band": "2", "stats": ["sum", "count", "area"]},
                {"name": "canola", "band": "3", "stats": ["sum", "count", "area"]},
            ],
        },
        "strategy": "raster-sequential",
        "output": "./output/output.csv",
    }


# Experiment 1: all files in s3.
# Experiment 2: all files in efs.
# Experiment 3: all files in efs, but with a shared memory volume.
# Experiment 4: all files in efs, but with a shared memory volume, and a shared disk volume.

# example s3 path
# s3://nigel-temp-bucket/512z_au_crop_yield_2023-10-04.tif

# TODO:
# make it run in ECS
# grab shape data via mongo query
# write output to mongo


def main():
    contents = urllib3.request(
        "http://169.254.170.2"
        + os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI")
    ).read()
    env_dict = json.loads(contents)

    # set if it's not set
    if os.environ.get("AWS_ACCESS_KEY_ID") is None:
        os.environ["AWS_ACCESS_KEY_ID"] = env_dict["AccessKeyId"]
    if os.environ.get("AWS_SECRET_ACCESS_KEY") is None:
        os.environ["AWS_SECRET_ACCESS_KEY"] = env_dict["SecretAccessKey"]
    if os.environ.get("AWS_SESSION_TOKEN") is None:
        os.environ["AWS_SESSION_TOKEN"] = env_dict["Token"]
    if os.environ.get("AWS_REGION") is None:
        os.environ["AWS_REGION"] = "ap-southeast-2"

    # {
    #     "AccessKeyId": "ACCESS_KEY_ID",
    #     "Expiration": "EXPIRATION_DATE",
    #     "RoleArn": "TASK_ROLE_ARN",
    #     "SecretAccessKey": "SECRET_ACCESS_KEY",
    #     "Token": "SECURITY_TOKEN_STRING"
    # }

    config = get_config()
    execute(config)
    upload_file(config["output"], "nigel-temp-bucket", "output.csv")


def execute(config):
    exe = ["exactextract"]
    strategy = ["--strategy", config["strategy"]]
    output = ["--output", config["output"]]
    geometries = ["-p", config["shape_data"]]
    fid = ["-f", config["shape_id"]]

    def stats(layer, raster, band, stats):
        return flatten(
            [
                [
                    "-r",
                    "{}:{}{}".format(
                        layer, raster, "[{}]".format(band) if band != "" else ""
                    ),
                ],
                flatten([["-s", "{}({})".format(s, layer)] for s in stats]),
            ]
        )

    all_stats = flatten(
        [
            stats(
                layer["name"], config["raster"]["path"], layer["band"], layer["stats"]
            )
            for layer in config["raster"]["bands"]
        ]
    )

    cmd = exe + strategy + geometries + fid + all_stats + output
    print(cmd)
    # flush std out
    sys.stdout.flush()
    subprocess.run(cmd)


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # database_url = os.environ.get("DATABASE_URL", "localhost:5432")

    # Upload the file
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        aws_session_token=os.environ["AWS_SESSION_TOKEN"],
        region_name=os.environ["AWS_REGION"],
    )

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

    # set this env var ('AWS_REGION')
    # set this env var ('AWS_SECRET_ACCESS_KEY')
    # set this env var ('AWS_ACCESS_KEY_ID')
    # set this env var ('AWS_SESSION_TOKEN')


if __name__ == "__main__":
    main()
