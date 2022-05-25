#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importacion de librerias
import shapefile
import os


class ShapeBUILD(object):
    def __init__(self, outpath):
        self.outpath = outpath
        self.shp = shapefile.Writer(shapefile.POLYGON)
        self.area = 'AREA'
        self.shp.field('CODIGOU', 'C', '50')
        self.shp.field('ZONA', 'N', decimal=0)
        self.shp.field('ESTADO', 'C', '10')
        self.shp.field(self.area, 'N', decimal=4)

    def set_coords(self, value):
        self.shp.poly(parts=value)

    def set_records(self, codigo, zona, estado):
        self.shp.record(codigo, zona, estado, 0)

    def get_name(self):
        res = os.path.basename(self.outpath).split('.')[0]
        return res
    
    # def set_cpg(self):
    #     cpg_path = "{}.cpg".format(self.get_name())
    #     with open(cpg_path,'w') as f:
    #         f.write('UTF-8')

    def save_shapefile(self):
        # self.set_cpg()
        self.shp.save(self.outpath)
