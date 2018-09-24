from datetime import datetime, timedelta


def decimalDOY2datetime(dDOY, year=2017):
    """"
    Esta funcion convierte la fecha de formato DOY con decimales a formato 'datetime'.
    """
    epoch = datetime(year - 1, 12, 31)

    # list(map(float, dDOY)) -> Convierto la la lista de str's a lista de float's.
    # map(lambda x: epoch+timedelta(days=x) -> convierto el DOY decimal a dateime
    try:
        result = list(map(lambda x: epoch+timedelta(days=x), list(map(float, dDOY))))
    except TypeError:
        result = epoch + timedelta(days=dDOY)

    return result
