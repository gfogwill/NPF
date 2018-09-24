class StationMetadata:
    def __init__(self):
        self.name = ''
        self.latitude = 0
        self.longitude = 0
        self.altitude = ''
        self.instruments = []

    def load_from_gawsis(self):
        """
        Funcion que carga los datos de la estacion desde GAWSIS.
        :return:
        """
        # TODO: Completar esta funcion.
