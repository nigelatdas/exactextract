#FROM isciences/exactextract:latest as build-deps
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

# --------------------

FROM python:3.13.0a2-bookworm


RUN apt-get update && apt-get install -y \
  binutils \
  libproj-dev \
  gdal-bin \
  libgdal-dev \
  libgeos-dev 

COPY --from=build-deps /usr/local/bin/exactextract /usr/local/bin/exactextract

# Set the working directory to /app
WORKDIR /app

# mount app/requirements and install them
RUN --mount=type=bind,source=./app/requirements.txt,target=/tmp/requirements.txt \
  pip3 install -r  /tmp/requirements.txt


# COPY data/raster/512z_au_crop_yield_2023-10-04.tif /app
# COPY data/geoms/system_farms.gpkg /app
COPY app/run_exactextract.py .

# Set the entry point to run the scripts
ENTRYPOINT ["python", "run_exactextract.py"]