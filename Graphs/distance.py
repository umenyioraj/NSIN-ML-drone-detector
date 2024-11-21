# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
# https://en.wikipedia.org/wiki/Haversine_formula
# units of conversion are km, return is converted to m
# might need to change to yards?
# r is radius of earth at 44 degrees N

from math import pow, sqrt, cos, asin, pi

def haversine (lat1, lon1, lat2, lon2):
    r = 6367.862
    p = pi/180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2

    hav = 2 * r * asin(sqrt(a))
    # convert km to m
    return hav * 1000 

def distance(lat1, lon1, lat2, lon2, alt):
    distance = sqrt(pow(haversine(lat1, lon1, lat2, lon2),2) + pow(alt,2))
    return distance