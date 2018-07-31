#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Daniel Fernando Aguado Huaccharaqui'
__copyright__ = 'INGEMMET 2018'
__credits__ = ['Daniel Aguado', 'Cesar Egocheaga']
__version__ = '1.0.1'
__maintainer__ = 'Daniel Aguado H.'
__mail__ = 'daguado@ingemmet.gob.pe'
__status__ = 'Production'

# Modulo os (sistema operativo)
import os

# Modulo cx_Oracle (Acceso, manipulacion de base de datos)
import cx_Oracle as oracle

# Directorio principal del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Connection(object):
    """
    Establece la conexion a base de datos
    Si el proceso de conexion falla, devuelve un valor nulo
    e imprime en consola que no se efectuo.
    """

    def __init__(self):
        self.user = 'DESA_GIS'
        self.password = 'DESA_GIS'
        self.instance = '10.102.0.66/bdgeocat'
        self.state = 'Without connection'

    # Metodo de solo lectura; se comporta como un atributo
    # mas de la clase
    @property
    def conn(self):
        # Intenta
        try:
            # Almacena la conexion en la variable connect
            connect = oracle.connect(self.user, self.password, self.instance)
            # Configura el estado de conexion
            self.state = 'Connected'
            # Retorna la conexion
            return connect
        # Si falla
        except Exception as e:
            # Imprime el error
            print e.message
            # Devuelve un valor nulo
            return None

    # Impresion de la clase
    def __str__(self):
        # Retorna el estado de conexion
        return self.state


class Statics(object):
    """
    Sirve de elementos estaticos que son utilizados en la logica
    del procesamiento principal
    """

    def __init__(self):
        self.path = os.path.join(BASE_DIR, 'statics')
        self.log = r'U:\Temp\cataE\cmi_trigger\log'
        self.shp = r'U:\Temp\cataE\cmi_trigger\shp'
        self.shp_query = r'U:\Temp\cataE\cmi_trigger\shp_query'
        self.prj = os.path.join(self.path, 'prj')

    # Impresion de la clase
    def __str__(self):
        # Retorna la ubicacion del directorio 'statics'
        return self.path
