#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importacion de librerias
from app_getrowdata import *
from app_creategeom import *
from app_writelogfile import *
import shutil
import sys
import arcpy

arcpy.env.overwriteOutput = True

# # Product mode
codes = sys.argv[1]

# Debug mode
# codes = '010014117'

# Se obtienen todos los codigos de derechos mineros
# de la base de datos
if codes:
    codigous = codes.split('_')
else:
    codigous = get_codigout_from_database()

# Se estable el directorio de salida de los archivos
# shapefile
if codes:
    folder = Statics().shp_query
else:
    folder = Statics().shp

prj_folder = Statics().prj

log = LogFile()
log.log_write_row('start', '...')

# Se generan las rutas de salidad para cada archivo
# shapefile en diferentes sistemas de coordenadas

# Shapefile en Coordenadas Geograficas
gcs = os.path.join(folder, gpo_cmi_catastro_minero_gcs().name + '.shp')

# Shapefile en PSAD56, zona 17
psad_17 = os.path.join(folder, gpo_cmi_catastro_minero_psad(17).name + '.shp')

# Shapefile en PSAD56, zona 18
psad_18 = os.path.join(folder, gpo_cmi_catastro_minero_psad(18).name + '.shp')

# Shapefile en PSAD56, zona 19
psad_19 = os.path.join(folder, gpo_cmi_catastro_minero_psad(19).name + '.shp')

# Shapefile en WGS84, zona 17
wgs_17 = os.path.join(folder, gpo_cmi_catastro_minero_wgs(17).name + '.shp')

# Shapefile en WGS84, zona 18
wgs_18 = os.path.join(folder, gpo_cmi_catastro_minero_wgs(18).name + '.shp')

# Shapefile en WGS84, zona 19
wgs_19 = os.path.join(folder, gpo_cmi_catastro_minero_wgs(19).name + '.shp')

# Diccionario que contiene los objetos shapefiles
# en diferentes sistemas, que recibiran la informacion
# desde la clase MiningConcessionINFO()
shapes = {1: dict(), 2: dict()}

# Objeto shapefile en PSAD56 | 17
shapes[1][17] = ShapeBUILD(psad_17)

# Objeto shapefile en PSAD56 | 18
shapes[1][18] = ShapeBUILD(psad_18)

# Objeto shapefile en PSAD56 | 19
shapes[1][19] = ShapeBUILD(psad_19)

# Objeto shapefile en WGS84 | 17
shapes[2][17] = ShapeBUILD(wgs_17)

# Objeto shapefile en WGS84 | 18
shapes[2][18] = ShapeBUILD(wgs_18)

# Objeto shapefile en WGS84 | 19
shapes[2][19] = ShapeBUILD(wgs_19)


def projections(name, code):
    """
    Definir la proyeccion espacial de los shapefiles
    :param name: nombre del feature a quien se asignara el src
    :param code: Codigo EPSG
    :return: None
    """
    # Obtener el prj segun la variable 'wkid'
    prj_old = os.path.join(prj_folder, '%s.prj' % code)
    # Generar la ruta de salida del prj
    prj_new = os.path.join(folder, '%s.prj' % name)
    # Copiar el prj en la ubicacion adecuada
    shutil.copy(prj_old, prj_new)


def deletefiles():
    """
    Eliminar archivos existentes
    :return: None
    """
    try:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    except Exception as e:
        log.log_write_row('delete files', e.message)
        print e.message


def createFeatures():
    """
    Funcion principal que realiza la generacion de
    geometrias
    :return:
    """
    # Iterando la lista de codigou
    global shp18
    for i, x in enumerate(codigous, 1):
        # Imprimiendo en consola el codigo actual
        print i, x
        # Intenta
        try:
            poo = MiningConcessionINFO(x)
            poo.main()
            for v in poo.data:
                m = shapes[v['src']][int(v['zona_load'])]
                m.set_coords(v['coords'])
                m.set_records(x, v['zona'], v['estado'])
        # En caso de error
        except Exception as e:
            log.log_write_row(x, e.message)  # Registro archivo log
            print e.message  # Imprime en consola

    try:
        # Graficar shapefile en PSAD56 | 17
        shp = shapes.get(1).get(17)
        shp.save_shapefile()
        projections(shp.get_name(), 24877)
        arcpy.RepairGeometry_management(shp.outpath)
        arcpy.CalculateField_management(shp.outpath, shp.area, '!SHAPE.area@HECTARES!', "PYTHON")
    except Exception as e:
        log.log_write_row('ERROR: Graficar shapefile en PSAD56 17s', e)
        print e
    try:
        # Graficar shapefile en PSAD56 | 18
        shp = shapes.get(1).get(18)
        shp.save_shapefile()
        projections(shp.get_name(), 24878)
        arcpy.RepairGeometry_management(shp.outpath)
        arcpy.CalculateField_management(shp.outpath, shp.area, '!SHAPE.area@HECTARES!', "PYTHON")
    except Exception as e:
        log.log_write_row('ERROR: Graficar shapefile en PSAD56 18s', e)
        print e
    try:
        # Graficar shapefile en PSAD56 | 19
        shp = shapes.get(1).get(19)
        shp.save_shapefile()
        projections(shp.get_name(), 24879)
        arcpy.RepairGeometry_management(shp.outpath)
        arcpy.CalculateField_management(shp.outpath, shp.area, '!SHAPE.area@HECTARES!', "PYTHON")
    except Exception as e:
        log.log_write_row('ERROR: Graficar shapefile en PSAD56 19s', e)
        print e
    try:
        # Graficar shapefile en WGS84 | 17
        shp = shapes.get(2).get(17)
        shp.save_shapefile()
        projections(shp.get_name(), 32717)
        arcpy.RepairGeometry_management(shp.outpath)
        arcpy.CalculateField_management(shp.outpath, shp.area, '!SHAPE.area@HECTARES!', "PYTHON")
    except Exception as e:
        log.log_write_row('ERROR: Graficar shapefile en WGS84 17s', e)
        print e
    try:
        # Graficar shapefile en WGS84 | 18
        shp18 = shapes.get(2).get(18)
        shp18.save_shapefile()
        projections(shp18.get_name(), 32718)
        arcpy.RepairGeometry_management(shp18.outpath)
        arcpy.CalculateField_management(shp18.outpath, shp18.area, '!SHAPE.area@HECTARES!', "PYTHON")
    except Exception as e:
        log.log_write_row('ERROR: Graficar shapefile en WGS84 18s', e)
        print e
    try:
        # Graficar shapefile en WGS84 | 19
        shp = shapes.get(2).get(19)
        shp.save_shapefile()
        projections(shp.get_name(), 32719)
        arcpy.RepairGeometry_management(shp.outpath)
    except Exception as e:
        log.log_write_row('ERROR: Graficar shapefile en WGS84 19s', e)
        print e
    try:
        arcpy.Project_management(shp18.outpath, gcs, arcpy.SpatialReference(4326))
        arcpy.RepairGeometry_management(gcs)
        arcpy.CalculateField_management(gcs, shp18.area, '!SHAPE.area@HECTARES!', "PYTHON")
    except Exception as e:
        log.log_write_row('ERROR: Graficar shapefile en GCS', e)
        print e

    log.log_write_row('end', '...')


# Si se ejecuta el archivo actual
if __name__ == '__main__':
    deletefiles()
    createFeatures()
    log.log_save()
