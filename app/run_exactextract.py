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


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_config():
    return {
        #        "shape_data": "/vsis3/nigel-temp-bucket/system_farms.gpkg",
        "shape_data": "./data/system_farms.gpkg",
        "shape_id": "id",
        "raster": {
            #            "path": "/vsis3/nigel-temp-bucket/cog_au_crop_yield_2023-10-04.tif",
            "path": "./data/cog_au_crop_yield_2023-10-04.tif",
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
    config = get_config()
    execute(config)
    # upload_file(config["output"], "nigel-temp-bucket", "output.csv")


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

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    main()
