#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importacion de librerias

# Modulo de configuracion (propio)
from model import *

# Conexion a la base de datos
conn = Connection().conn


def get_codigout_from_database():
    """
    Funcion que permite la captura de todos los derechos
    mineros (identificador: 'CODIGOU') necesarios para
    realizar su tranformacion a feature class
    :return:
    """
    cursor = conn.cursor()
    res = cursor.callfunc('DATA_CAT.PACK_DBA_SIGCATMIN.F_GET_CODECAT_TO_GRAPH_PYTHON', oracle.CURSOR)
    res = [x[0] for x in res]
    cursor.close()
    del cursor
    return res


class MiningConcessionINFO(object):
    """
    Objeto que permite la captura
    de coordenadas de la base de datos para
    su transformacion a un Feature Class
    (tipo de informacion con soporte espacial)
    """

    def __init__(self, codigou):
        self.codigou = codigou
        self.cursor = conn.cursor()
        self.overlap = dict()
        self.state = str()
        self.src = dict()

    def get_src_origin_and_equivalent(self):
        """
        Obtiene el sistema de referencia original y equivalente
        :return:
        """
        res = self.cursor.callfunc('SISGEM.PACK_DBA_SG_D_PETITORIO.CODDATUM@GAMMA', oracle.STRING, [self.codigou])
        self.src[1] = int(res)
        if self.src[1] == 1:
            self.src[2] = 2
        else:
            self.src[2] = 1

    def get_zone_origin(self):
        """
        Obtiene la zona original del derecho consultado
        :return:
        """
        self.overlap[0] = self.cursor.callfunc('DATA_CAT.PACK_DBA_SIGCATMIN.F_GET_ZONE_CURRENT', oracle.STRING,
                                               [self.codigou])

    def get_zone_overlap(self, n):
        """
        Obtiene la zona de traslape del derecho consultado
        Acepta un parametro 'n' el cual toma valores entre
        {1: traslape 1, 2: traslape 2}
        :param n:
        :return:
        """
        self.overlap[n] = self.cursor.callfunc('DATA_CAT.PACK_DBA_SIGCATMIN.F_GET_ZONE_OVERLAP',
                                               oracle.STRING, [self.overlap[0], n])

    def get_state(self):
        """
        Obtiene el estado del derecho minero consultado
        :return:
        """
        self.state = self.cursor.callfunc('SISGEM.PACK_DBA_SG_D_PETITORIO.ESTADO_GRAF@GAMMA', oracle.STRING,
                                          [self.codigou])

    def get_coordinates(self, n):
        """
        Obtiene las coordenadas originales y equivalentes
        :param n:
        :return:
        """
        sys_refcursor = self.cursor.var(oracle.CURSOR)
        self.cursor.callproc('DATA_CAT.PACK_DBA_SIGCATMIN.P_GET_COORDS_AS_CURSOR', [self.codigou, n, sys_refcursor])
        res = [list(x) for x in sys_refcursor.getvalue()]
        sys_refcursor.getvalue().close()
        return res

    def get_coordinates_overlap(self, src, n, coords):
        """
        Obtiene las coordenadas traslapadas tanto originales
        como equivalentes
        :param src:
        :param n:
        :param coords:
        :return:
        """
        array = list()
        if src == 1:
            function = 'SISGEM.PACK_DBA_SG_D_EVALGIS.P_PROYECCION_COORD_56_W@GAMMA'
        else:
            function = 'SISGEM.PACK_DBA_SG_D_EVALGIS.P_PROYECCION_COORD_84_W@GAMMA'
        for x in coords:
            res = self.cursor.callfunc(function, oracle.STRING, [x[-2], x[-1], self.overlap[0], self.overlap[n]])
            m = res.split(',')
            array.append([x[0], x[1], float(m[0]), float(m[1])])
        return array

    def set_coords(self, coords):
        """
        Establece el formato correcto de las coordenadas para ser graficadas
        :param coords:
        :return:
        """
        groups = set(map(lambda x: x[0], coords))
        coordinates = [[[m[-2], m[-1]] for m in coords if m[0] == x] for x in groups]
        # print coordinates
        return coordinates

    def make_dict_output(self):
        orig = self.get_coordinates(1)
        equi = self.get_coordinates(2)
        orig_overlap_01 = self.get_coordinates_overlap(self.src[1], 1, orig)
        orig_overlap_02 = self.get_coordinates_overlap(self.src[1], 2, orig)
        equi_overlap_01 = self.get_coordinates_overlap(self.src[2], 1, equi)
        equi_overlap_02 = self.get_coordinates_overlap(self.src[2], 2, equi)
        coord_ori = self.set_coords(orig)
        coord_equ = self.set_coords(equi)
        coord_ori_overlap_01 = self.set_coords(orig_overlap_01)
        coord_ori_overlap_02 = self.set_coords(orig_overlap_02)
        coord_equ_overlap_01 = self.set_coords(equi_overlap_01)
        coord_equ_overlap_02 = self.set_coords(equi_overlap_02)

        self.data = [{'src': self.src[1], 'estado': self.state, 'zona': self.overlap[0], 'zona_load': self.overlap[0],
                      'coords': coord_ori},
                     {'src': self.src[2], 'estado': self.state, 'zona': self.overlap[0], 'zona_load': self.overlap[0],
                      'coords': coord_equ},
                     {'src': self.src[1], 'estado': self.state, 'zona': self.overlap[0], 'zona_load': self.overlap[1],
                      'coords': coord_ori_overlap_01},
                     {'src': self.src[1], 'estado': self.state, 'zona': self.overlap[0], 'zona_load': self.overlap[2],
                      'coords': coord_ori_overlap_02},
                     {'src': self.src[2], 'estado': self.state, 'zona': self.overlap[0], 'zona_load': self.overlap[1],
                      'coords': coord_equ_overlap_01},
                     {'src': self.src[2], 'estado': self.state, 'zona': self.overlap[0], 'zona_load': self.overlap[2],
                      'coords': coord_equ_overlap_02}]

    def main(self):
        """
        Funcion principal que contiene toda la logica de
        procesamiento
        :return:
        """
        self.get_src_origin_and_equivalent()
        self.get_zone_origin()
        self.get_zone_overlap(1)
        self.get_zone_overlap(2)
        self.get_state()
        self.make_dict_output()
