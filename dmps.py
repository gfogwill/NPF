import pandas as pd
from statmeta import StationMetadata
from utools import decimalDOY2datetime
import numpy as np


class DMPS:
    """ This class contains DMPS data. """
    def __init__(self):
        self.data = pd.DataFrame()
        self.station = StationMetadata()

    def load_data_with_labels(self, nukfile='', datafile=''):
        """
        NUK File:
        ------------
        :param nukfile: Path to the file where the labels are stored.

        This file contains the labels of the human classified events pf NPF from DMPS instrument. This file contains lines
        with the following structure:

        DOY  Class_first_event  Start_time  End_time  Class_Second_event  Start_time  End_time

        * Example of content:
        ...
        2.3000000e+001  2.0000000e+000  2.3427063e+001  2.3690019e+001             NaN             NaN             NaN
        2.4000000e+001  3.0000000e+000  2.4784069e+001  2.4832054e+001  3.0000000e+000  2.4891555e+001  2.5014395e+001
        ...

        NOTE: If an event starts one day and it ends on the next day, the End_time of the event is grater than the DOY.


        CLE File:
        ---------
        :param datafile: Path to the *.cle file where the procesed DMPS data is stored.

        The structure of the file is:

        DOY  Tot_part  Size_1_concentration  Size_2_concentration ... Size_25_concentration

        * Example of content:
        ...
        2.0579514e+000  1.0384256e+003  0.0000000e+000  9.5281773e+002  1.0888169e+003  ...  \
        2.0620949e+000  1.0384537e+003  0.0000000e+000  1.1694859e+003  7.9377540e+002  ...  | --> Continues up to 27 col's
        2.0662384e+000  1.0772310e+003  0.0000000e+000  1.3906020e+003  1.0835656e+003  ...  /
        ...

        NOTE: Size_1_concentration is discarted because of malfunctioning of Marambio instrument for this size.



        :return: Returns a two level index DataFrame where the level 0 index is the classification of the events, and the
                 level 1 index is the time.

        * Example of content:
         NE 2017-01-01 00:00:00   2709.661350   763.653850   220.816925   611.118857  ...
            2017-01-01 00:10:00   1162.275400  3307.198700  3142.933600   663.416070  ...
            2017-01-01 00:20:00   2003.903070   604.363595  1634.514950  1066.618370  ...
         c1 2017-01-01 00:30:00    916.880200   840.689085  2961.959350  1579.489800  ...
            2017-01-01 00:40:00   2960.385800  2562.946900  2343.879750  1227.647295  ...
            2017-01-01 00:50:00   1850.210300  2328.736400  2006.664700   898.062500  ...

        """
        nukdata = pd.read_csv(nukfile, sep=r'\s+')
        nukdata = nukdata.replace(np.nan, -1)
        nukdata.iloc[:, 2] = nukdata.iloc[:, 2].apply(decimalDOY2datetime)
        nukdata.iloc[:, 3] = nukdata.iloc[:, 3].apply(decimalDOY2datetime)
        nukdata.iloc[:, 5] = nukdata.iloc[:, 5].apply(decimalDOY2datetime)
        nukdata.iloc[:, 6] = nukdata.iloc[:, 6].apply(decimalDOY2datetime)

        # Cargo los datos del DMPS.
        data = pd.read_csv(datafile, sep=r'\s+', date_parser=decimalDOY2datetime, parse_dates=[0], index_col=0)

        # Borro las 2 primeras columnas, que tienen el N° total de particulas, y el primer tamaño que funciona mal.
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
        self.data = pd.DataFrame(index=[data.event.values, data.index.values], data=data.iloc[:, 2:-1].values)

    def to_htk_format(self, outdir='', level=0):
        """
        Esta funcion toma una estructura DMPS y genera los archivos de binarios de HTK donde estan guardados los
        parametros.

        :param outdir:
        :param level:
        :return:
        """
        # TODO: Completar la funcion

    def gen_htk_labels(self, outdir=''):
        """

        :param outdir:
        :return:
        """
        # TODO: Completar la funcion

