# python imports
import math
import logging
import datetime

logger = logging.getLogger(__name__)


def calculate_radial_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Source: https://gis.stackexchange.com/a/56589/15183
    """
    # convert decimal degrees to radians
    try:
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        km = 6367 * c
        meters = km * 1000
        return meters
    except Exception:
        logger.error("calculate_radial_distance failed", exc_info=True)
        return 0


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        func_response = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        logger.info("{} : Time taken - {} (in seconds)".format(
            func.__name__,
            (end_time-start_time).microseconds / pow(10, 6)
        ))
        return func_response
    return wrapper
