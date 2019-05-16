"""
Read the given grib2 file and export them as png files 
"""
# region modules
from __future__ import print_function
from __future__ import division
import datetime
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import gdal
from time import sleep


# endregion modules
class grib_reader(object):
    def __init__(self):
        self._process_path = r"i:\temp\sumodel"

    @property
    def process_path(self):
        return self._process_path

    @process_path.setter
    def process_path(self, value):
        self._process_path = value

    def date_decorator(func):
        def wrapper(self):
            st = datetime.datetime.now()
            func(self)
            print(datetime.datetime.now() - st)

        return wrapper

    def line_decorator(func):
        def wrapper(self):
            print("=" * 50)
            func(self)
            print("=" * 50)

        return wrapper

    @date_decorator
    def write_topng(self, fname, dataset):
        import png
        try:
            f = open(fname, 'wb')
            w = png.Writer(len(dataset[0]), len(dataset), palette=self.fsc_palette, bitdepth=8)
            w.write(f, dataset)
            return 1
        except BaseException as be:
            print(be.message)
            raise Exception("Cannot write PNG file ::", fname)
            return 0

    @line_decorator
    @date_decorator
    def run(self):
        if self._process_path is None:
            raise Exception("Process path is not defined")
        print("Scrpit is being initiated")
        grib2_files = [os.path.join(gribing.process_path, row) for row in glob.glob1(gribing.process_path, "*.grib2")]
        for file_ in grib2_files:
            print(file_, "is being processed")
            temp_grib_dataset = gdal.Open(file_)
            for raster in range(1, temp_grib_dataset.RasterCount + 1):
                st = datetime.datetime.now()
                temp_grib_dataraster = temp_grib_dataset.GetRasterBand(raster)
                fig = plt.figure()
                plt.imshow(temp_grib_dataraster.ReadAsArray())
                plt.savefig(os.path.join(os.path.splitext(file_)[0] + "__" + str(raster) + ".png"))
                print(datetime.datetime.now() - st)
                plt.clf()
                plt.close('all')
                del fig


if __name__ == '__main__':
    gribing = grib_reader()
    gribing.process_path = '/mnt/temp/sumodel'
    grib_reader.process_path
    gribing.run()
