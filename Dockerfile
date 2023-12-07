FROM debian:bookworm-slim as build-deps

LABEL maintainer="dbaston@isciences.com"

RUN apt-get update && apt-get install -y \
  build-essential \
  cmake \
  curl \
  doxygen \
  gdal-bin \
  git \
  graphviz \
  libgdal-dev \
  libgeos-dev \
  unzip \
  wget

COPY . /exactextract

RUN mkdir /cmake-build-release && \
  cd /cmake-build-release && \
  cmake -DCMAKE_BUILD_TYPE=Release /exactextract && \
  make && \
  ./catch_tests && \
  make install && \
  rm -rf /cmake-build-release

ENTRYPOINT ["exactextract"]

#--------------------

# Use an official Python runtime as a parent image
FROM python:3.9.13-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY --from=build-deps exactextract /app
COPY app/requirements.txt /app
RUN pip3 install -r requirements.txt

# COPY data/raster/512z_au_crop_yield_2023-10-04.tif /app
# COPY data/geoms/system_farms.gpkg /app
COPY app/run_exactextract.py /app

# Set the entry point to run the scripts
ENTRYPOINT ["python", "run_exactextract.py"]