# region modules
from __future__ import print_function
from __future__ import division
import datetime

import numpy as np
import pandas as pd

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import gdal
from time import sleep
from xlsxwriter.utility import xl_range

# endregion modules
class grib_reader(object):
    def __init__(self):
        self. start_time = datetime.datetime.now()
        self._process_path = r"/mnt/temp/sumodel"

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

    @staticmethod
    def GetExtent(gt, cols, rows):
        ''' Return list of corner coordinates from a geotransform

            @type gt:   C{tuple/list}
            @param gt: geotransform
            @type cols:   C{int}
            @param cols: number of columns in the dataset
            @type rows:   C{int}
            @param rows: number of rows in the dataset
            @rtype:    C{[float,...,float]}
            @return:   coordinates of each corner
        '''
        ext = []
        xarr = [0, cols]
        yarr = [0, rows]

        for px in xarr:
            for py in yarr:
                x = gt[0] + (px * gt[1]) + (py * gt[2])
                y = gt[3] + (px * gt[4]) + (py * gt[5])
                ext.append([x, y])
                print
                x, y
            yarr.reverse()
        return ext

    @line_decorator
    @date_decorator
    def run(self):
        if self._process_path is None:
            raise Exception("Process path is not defined")
        print("Scrpit is being initiated")
        # grib2_files = [os.path.join(gribing.process_path, row) for row in glob.glob1(gribing.process_path, "wnd10m*.grb2")]
        grib2_files = [os.path.join(gribing.process_path, row) for row in glob.glob1(gribing.process_path, "201902pressfc.gdas.201902*.grib2")]
        for file_ in grib2_files:
            print(file_, "is being processed")
            temp_grib_dataset = gdal.Open(file_)
            counter, CC, Start_date = 0, 0, datetime.datetime.strptime('20190225', '%Y%m%d')
            writer = pd.ExcelWriter(os.path.join(os.path.splitext(file_)[0] + "__" + ".xlsx"),
                                    engine='xlsxwriter')
            for raster in range(1, temp_grib_dataset.RasterCount + 1):
                if raster >= 771:
                    print(raster)
                    counter += 1
                    if 7<=counter<9:
                        if counter  == 8:
                            counter = 0
                        print(raster, raster, raster, raster, raster, raster, raster, )
                    else:
                        print(raster)
                        CC += 1

                        st = datetime.datetime.now()
                        temp_grib_dataraster = temp_grib_dataset.GetRasterBand(raster)


                        # workbook = xlsxwriter.Workbook(os.path.join(os.path.splitext(file_)[0] + "__" + str(raster) + ".xlsx"))
                        # worksheet = workbook.add_worksheet()

                        writer = pd.ExcelWriter(os.path.join(os.path.splitext(file_)[0] + "__" + str(raster) + ".xlsx"),
                                                engine='xlsxwriter')
                        print((Start_date + datetime.timedelta(hours=CC)).strftime("%Y%m%d_%H%M"))
                        workbook = writer.book

                        df = pd.DataFrame(data=temp_grib_dataraster.ReadAsArray()/100.0)
                        # import osr
                        # f_name = "d_sil.gtiff"
                        # # f_name = os.path.join(os.path.splitext(file_)[0] + "__" + str(raster) + ".gtiff")
                        # projection = osr.SpatialReference()
                        # projection.SetWellKnownGeogCS("EPSG:" + str(4326))
                        # driver = gdal.GetDriverByName("GTiff")
                        # export_data = driver.Create(f_name, 1760, 880, 1, gdal.GDT_Float32)
                        # # sets the extend
                        # export_data.SetGeoTransform(temp_grib_dataset.GetGeoTransform())
                        # # sets projection
                        # export_data.SetProjection(projection.ExportToWkt())
                        # export_data.GetRasterBand(1).WriteArray(df.values)
                        # # allcorners = self.get_extent(export_data.GetGeoTransform(), transform[1][1], transform[1][0])7
                        # export_data.FlushCache()
                        # # if bbox is not None and extension is 'GTiff':
                        # #     gdal.Translate(out_f_name, export_data, projWin=bbox)
                        df2 = pd.DataFrame(df.values[208:243, 134:206])
                        df2.to_excel(
                            writer, sheet_name = (Start_date + datetime.timedelta(hours=CC)).strftime("%Y%m%d_%H%M"),
                            startcol=1,
                            startrow=1
                        )
                        writer.close()

                        # fig = plt.figure()
                        # plt.imshow(temp_grib_dataraster.ReadAsArray())
                        # plt.savefig(os.path.join(os.path.splitext(file_)[0] + "__" + str(raster) + ".png"))
                        print(datetime.datetime.now() - st)
                        # plt.clf()
                        # plt.close('all')
                        # del fig
            # writer.close()




if __name__ == '__main__':
    gribing = grib_reader()
    grib_reader.process_path
    gribing.run()


#
# counter = 0
# for i, reo  in enumerate(range(50
#                                )):
#     counter +=1
#     if 7<=counter<9:
#         if counter ==8:
#             counter = 0
#         print i, i, i, i, i, i, i
#     else:
#         print i, 771+reo
