# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
# https://en.wikipedia.org/wiki/Haversine_formula
# units are currently km
# might need to change to yards?
# r is radius of earth at 44 degrees N

import math

def haversine (lat1, lon1, lat2, lon2):
    r = 6367.862
    p = math.pi/180

    a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p) * math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p))/2

    return 2 * r * math.asin(math.sqrt(a))


print(haversine(40.033925, -75.340412, 38.817058, -77.269905))