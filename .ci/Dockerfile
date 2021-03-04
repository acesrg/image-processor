FROM python:3.8.7-slim-buster

#librerías necesarias
#RUN pip install rasterio geopandas pycrs watchdog inotify_simple
COPY src/requirements.txt .
RUN pip install -r requirements.txt

#seteo esta variable porque estoy trayendo el gdal de manera externa y no compilandolo con gcc
ENV GDAL_DATA=/usr/local/lib/python3.8/site-packages/fiona/gdal_data
