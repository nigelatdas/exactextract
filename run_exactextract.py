# run exactextract process
# eg: exactextract -r "wheat:../hacking/512z_au_crop_yield_2023-10-04.tif[1]" -p ~/system_farms.gpkg -f id --output ../data/full_512z_au_crop_yield_2023-10-04__001.csv -s "sum(wheat)" -s "count(wheat)" -s "rawsum(wheat:0.01)" -s "rawhitcount(wheat:0.01)" -s "rawcount(wheat:0.01)"  --strategy raster-sequential

# import os
# import sys
# import argparse
import subprocess


def flatten(l):
    return [item for sublist in l for item in sublist]


# TODO:
# 1. grab shape data via mongo query
# 2. grab raster data from s3 bucket OR from efs mounted drive


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "input",
    #     help="input raster file",
    #     type=str,
    #     example="wheat:512z_au_crop_yield_2023-10-04.tif[1]",
    # )
    # parser.add_argument("output", help="output csv file")
    # parser.add_argument("shape", help="shape file")
    # parser.add_argument("stat", help="stat to calculate")
    # # parser.add_argument('--band', help='band to extract', type=int, default=1)
    # # parser.add_argument('--nodata', help='nodata value', type=float, default=-9999)
    # # parser.add_argument('--threads', help='number of threads', type=int, default=1)
    # parser.add_argument(
    #     "--overwrite", help="overwrite output file", action="store_true"
    # )
    # args = parser.parse_args()

    # if not os.path.exists(args.input):
    #     print("Input file does not exist: {}".format(args.input))
    #     sys.exit(1)

    # if os.path.exists(args.output):
    #     if args.overwrite:
    #         os.remove(args.output)
    #     else:
    #         print("Output file already exists: {}".format(args.output))
    #         sys.exit(1)

    # if not os.path.exists(args.shape):
    #     print("Shape file does not exist: {}".format(args.shape))
    #     sys.exit(1)

    # cmd = flatten(
    #     [
    #         [
    #             "exactextract",
    #         ],
    #         [
    #             "-p",
    #             args.shape,
    #         ],
    #         [
    #             "-f",
    #             "id",
    #         ],
    #         [
    #             "-r",
    #             args.input,
    #         ],
    #         [
    #             "-o",
    #             args.output,
    #         ],
    #         [
    #             "-s",
    #             "sum(wheat)",
    #         ],
    #         [
    #             "-s",
    #             "count(wheat)",
    #         ],
    #         [
    #             "-s",
    #             "rawsum(wheat:0.01)",
    #         ],
    #         [
    #             "-s",
    #             "rawhitcount(wheat:0.01)",
    #         ],
    #         [
    #             "-s",
    #             "rawcount(wheat:0.01)",
    #         ],
    #         [
    #             "--strategy",
    #             "raster-sequential",
    #         ],
    #     ]
    # )

    cmd = [
        "exactextract",
        "-r",
        '"wheat:./512z_au_crop_yield_2023-10-04.tif[1]"',
        "-r",
        '"barley:./512z_au_crop_yield_2023-10-04.tif[2]"',
        "-r",
        '"canola:./512z_au_crop_yield_2023-10-04.tif[3]"',
        "-p",
        "./system_farms.gpkg",
        "-f",
        "id",
        "--output",
        "./512z_au_crop_yield_2023-10-04__001.csv",
        "-s",
        '"sum(wheat)"',
        "-s",
        '"count(wheat)"',
        "-s",
        '"rawsum(wheat:0.01)"',
        "-s",
        '"rawhitcount(wheat:0.01)"',
        "-s",
        '"rawcount(wheat:0.01)"',
        "-s",
        '"sum(barley)"',
        "-s",
        '"count(barley)"',
        "-s",
        '"rawsum(barley:0.01)"',
        "-s",
        '"rawhitcount(barley:0.01)"',
        "-s",
        '"rawcount(barley:0.01)"',
        "-s",
        '"sum(canola)"',
        "-s",
        '"count(canola)"',
        "-s",
        '"rawsum(canola:0.01)"',
        "-s",
        '"rawhitcount(canola:0.01)"',
        "-s",
        '"rawcount(canola:0.01)"',
        "--strategy",
        "raster-sequential",
    ]

    subprocess.run(cmd)
