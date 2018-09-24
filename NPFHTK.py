import struct
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utools import decimalDOY2datetime


def _write_header(fo, data):
    """
    This function writes the header of the HTK parameters binary file.
    """
    nSamples = data.__len__()-1             # Calculo la cantidad de muestras que va a contener el archivo.
    numberOfFeatures = 25                   # Number of sizes of DMPS.
    sampPeriod = int(600 / 100e-9 / 1e6)    # HTK toma como si fuesen 600 us pero en realidad son 600 segundos. Esto se
                                            # se debe a que no es posible representar el periodo de 600 segundos con un
                                            # int de 4 bytes. Es decir que los tiempos se dividen por 1e6.
    sampSize = 4 * numberOfFeatures         # Tamaño del float
    parmKind = 9                            # USER (user defined sample kind)
    fo.write(nSamples.to_bytes(4, byteorder='big', signed=False))
    fo.write(sampPeriod.to_bytes(4, byteorder='big', signed=False))
    fo.write(sampSize.to_bytes(2, byteorder='big', signed=False))
    fo.write(parmKind.to_bytes(2, byteorder='big', signed=False))


def cle2bin(file):
    out_file = 'test.bin'
    num_lines = sum(1 for line in open(file))

    fi = open(file, 'r')
    fo = open(out_file, 'wb')

    # Leo la primera linea que es la que tiene los nombres
    fi.readline()

    # Escribo el header del arhivo
    _write_header(fo, num_lines - 1)

    for line in fi:
        # Leo una linea y la convierto a "float". Me quedo solo con los datos, no con la fecha ni la concentracion total
        temp_line = list(map(float, line.split()))[2:]

        # Convierto los datos a binario y los guardo
        for value in temp_line:
            fo.write(struct.pack('>f', value))
    fo.close()


def cle2bin2(file):
    """


    """
    data = pd.read_csv(file, sep=r'\s+', date_parser=decimalDOY2datetime, parse_dates=[0], index_col=0)
    data = data.resample('10t').mean()

    out_file = 'test.bin'
    fo = open(out_file, 'wb')

    _write_header(fo, data)

    # Borro las 2 primeras columnas, que tienen el N° total de particulas, y el primer tamaño que funciona mal.
    data.drop(data.columns[[0, 1]], axis=1, inplace=True)

    # Guardo el DataFrame a binario.
    # Recorro cada linea
    for index, line in data.iterrows():
        # Recorro cada elemento de la linea
        for value in line.values:
            # Guardo el valor como binario
            fo.write(struct.pack('>f', value))

    return data


def nuk2lab(data_file, nuk_file):
    """
    TODO:  ¿Tiene sentido esta funcion? ¿Como voy a hacer el etiquedato de los archivos? Creo que esto solo tendria
    sentido si trabajo con todos los datos juntos, y no con uno, dos o tres eventos por archivo.

    This function convert the *.nuk file to *.lab file.

    Parameters:
    -----------

    Returns:
    --------

    LAB File:
    ------------
    The *.lab file is a text based HTK label format.
    Each  line  of  a  HTK  label  file  contains  the  actual  label  optionally  preceded  by  start  and  end times,
    and optionally followed by a match score:

    [start [end] ] name [score] { auxname [auxscore] } [comment]

    For more information see HTK book section 6.2.
    """

    nukdata = pd.read_csv(nuk_file, sep=r'\s+')
    nukdata = nukdata.replace(np.nan, -1)
    nukdata.iloc[:, 2] = nukdata.iloc[:, 2].apply(decimalDOY2datetime)
    nukdata.iloc[:, 3] = nukdata.iloc[:, 3].apply(decimalDOY2datetime)
    nukdata.iloc[:, 5] = nukdata.iloc[:, 5].apply(decimalDOY2datetime)
    nukdata.iloc[:, 6] = nukdata.iloc[:, 6].apply(decimalDOY2datetime)

    # Cargo los datos del DMPS.
    data = pd.read_csv(data_file, sep=r'\s+', date_parser=decimalDOY2datetime, parse_dates=[0], index_col=0)

    # Borro las 2 primeras columnas, que tienen el N° total de particulas, y el primer tamaño que funciona mal.
    # TODO: Probar de usar el N° total de particulas como un parametro mas para ver como da el reconocedor.
    data.drop(data.columns[[0, 1]], axis=1, inplace=True)

    # Promedio los datos cada 10 minutos para homogeneizar los datos temporalmente.
    # TODO: ver como promediar los datos. Esta interpolando? Funciona bien esto? Conviene usar los datos sin hacer nada?
    data = data.resample('10t').mean()

    # Agrgo una columna donde va a ir la clasificacion de esa muestra
    data['event'] = 'NE'

    d = {0.0: 'NE',
         1.0: 'c1',
         2.0: 'c2',
         3.0: 'c3',
         4.0: 'BD'}

    # Clasifico los datos segun el etiquetado echo en el archivo *.nuk
    for i in range(nukdata.__len__()):
        data.loc[(data.index > nukdata.iloc[i, 2]) & (data.index < nukdata.iloc[i, 3]), 'event'] = d.get(nukdata.iloc[i, 1])
    for i in range(nukdata.__len__()):
        data.loc[(data.index > nukdata.iloc[i, 5]) & (data.index < nukdata.iloc[i, 6]), 'event'] = d.get(nukdata.iloc[i, 4])

    # Creo un nuevo dataframe con 2 niveles de indices. El primero es el evento, y el segundo es el tiempo.
    data = pd.DataFrame(index=[data.event.values, data.index.values], data=data.iloc[:, 2:-1].values)

    print('a')


path = 'C:\\Users\\Ger\\Desktop\\GERMAN\\datos_2017\\DM20170202.cle'
nuk_file = 'C:\\Users\\Ger\\Desktop\\GERMAN\\clasification_eventos.nuk'
data2017 = 'C:\\Users\\Ger\\Desktop\\GERMAN\\datos_2017\\DMPSmara_2017.dat'
data = nuk2lab(data2017, nuk_file)

