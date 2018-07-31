#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Desarrollo que almacena informacion de las
 tablas utilizadas para los fines de esta app
 Tablas:
    # * SC_V_COORDENADADET
    # * SC_D_LIBREDENUNCIACOOR
    * GPO_CMI_CATASTRO_MINERO_PSAD {17, 18, 19}
    * GPO_CMI_CATASTRO_MINERO_WGS {17, 18, 19}
    * GPO_CMI_CATASTRO_MINERO_GCS
"""

from config import *


class gpo_cmi_catastro_minero_psad(object):
    def __init__(self, zone=None):
        self.codigou = 'CODIGOU'
        self.estado = 'ESTADO'
        self.zona = "ZONA"
        self.zone = zone

    def setzone(self, value):
        self.zone = value

    @property
    def name(self):
        res = self.__class__.__name__
        res = res + '_%s' % self.zone
        return res.upper()

    def __str__(self):
        return self.name


class gpo_cmi_catastro_minero_wgs(gpo_cmi_catastro_minero_psad):
    def __init__(self, zone):
        super(self.__class__, self).__init__()
        self.zone = zone


class gpo_cmi_catastro_minero_gcs(gpo_cmi_catastro_minero_psad):
    def __init__(self):
        super(self.__class__, self).__init__()
        del self.zone, self.zona

    @property
    def name(self):
        res = self.__class__.__name__
        return res.upper()
