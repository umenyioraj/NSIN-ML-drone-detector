import os, pandas as pd, numpy as np
from datetime import datetime
from distance import distance
from math import ceil
from metric2 import m2
from metric1 import m1
from math import floor
import numpy as np
import math as math
from statistics import mean
from scipy.interpolate import BSpline
from scipy.interpolate import splrep, splev,CubicSpline
import matplotlib.pyplot as plt

def FeatureEngineer(data):
    ThreatId = data['ThreatId'].to_numpy()
    Altitude = data['Location.Altitude'].to_numpy()
    DetectionTime = data['DetectionTimeInDT'].to_numpy()

    Detection_times = {}

    # Fill detection_times dictionary to show,  {id: array_of_time_change_in_seconds}
    for i, threat in enumerate(ThreatId):
        id = ThreatId[i]
        date = DetectionTime[i]
        
        date_split = date.split(':')
        seconds = date_split[2]
        if id not in Detection_times:
            Detection_times[id] = [float(seconds)]
        else:
            Detection_times[id].append(float(seconds))
    #create new feature if Signal is persistent (detected frequently within 6 seconds)

    data['Signal Persistence'] = False
    signal_pers = []
    #check if there is an time when the diff is less than or equal to 6 seconds, if so change feature to True
    for id, seconds in Detection_times.items():
        for left in range(len(seconds)-5):
            right = left + 5
            diff = seconds[right] - seconds[left]
            if diff <= 6.0:
                if id not in signal_pers:
                    signal_pers.append(id)
                data.loc[data['ThreatId'] == id, "Signal Persistence"] = True
                break
    
    Detection_heights = {}

    for i, threat in enumerate(ThreatId):
        id = ThreatId[i]
        altitude = Altitude[i]

        if id not in Detection_heights:
            Detection_heights[id] = [float(altitude)]
        else:
            Detection_heights[id].append(float(altitude))

    data['Altitude Consistent'] = False

    altitude_const = []
    for id, heights in Detection_heights.items():
        for left in range(len(heights)-5):
            right = left +5
            if diff <= 6.0:
                if id not in altitude_const:
                    altitude_const.append(id)
                data.loc[data['ThreatId'] == id, "Altitude Consistent"] = True
                break
    
    data["Speed"] = data["Speed"] * 2.237

    ninja_ids = []

    data["Drone"] = 0

    for id in ThreatId:
        ninja_status = data.loc[data["ThreatId"] == id, "Ninja"]
        if any(ninja_status) == True:
            data.loc[data["ThreatId"] == id, "Drone"] = 1
            if id not in ninja_ids:
                ninja_ids.append(id)

    return data

def GenerateSmoothnessMetric(data):
    ThreatId = data['ThreatId'].to_numpy()
    Latitude = data['Location.Latitude'].to_numpy()
    Longitude = data['Location.Longitude'].to_numpy()
    Altitude = data['Location.Altitude'].to_numpy()
    DetectionTime = data['DetectionTimeInDT'].to_numpy()

    ThreatsXY = {}
    ThreatsHT = {}

    for i, threat_num in enumerate(ThreatId):


        latitude = Latitude[i]
        longitude = Longitude[i]
        altitude = Altitude[i]
        detection_time = DetectionTime[i] # string value 


        new_coordinate_xy = [latitude, longitude, detection_time] # first graph 
        new_coordinate_ht = [altitude, detection_time] # second graph 


        # populating dictionary for longitude vs latitude graph 
        # eliminating duplicates in dictionary without using a series  
        if threat_num in ThreatsXY: 
            if (new_coordinate_xy not in ThreatsXY[threat_num]):
                ThreatsXY[threat_num].append(new_coordinate_xy)
        
        else:
            ThreatsXY[threat_num] = [new_coordinate_xy]


        # populating dictionary for height vs time graph 
        # eliminating duplicates in dictionary without using a series  
        if threat_num in ThreatsHT: 
            if new_coordinate_ht[0] == 0.0:
                continue
            elif new_coordinate_ht not in ThreatsHT[threat_num]:
                ThreatsHT[threat_num].append(new_coordinate_ht)


        else: 
            ThreatsHT[threat_num] = [new_coordinate_ht]


    for IDofInterest in set(ThreatId):
        graph_data = {"Height":[], "DeltaT":[], "Lat":[], "Lon":[], "Distance":[]}
        try:
            t0 = datetime.strptime(ThreatsHT[IDofInterest][0][1],"%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            next
        for i in range(len(ThreatsHT[IDofInterest])):
            # append coordinates to the dictionary lists
            try:
                ti = datetime.strptime(ThreatsHT[IDofInterest][i][1],"%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                next
            #print(t0)

            time_diff = ti - t0
            deltat = time_diff.total_seconds()
            # print(deltat)

            if deltat not in graph_data["DeltaT"]:
                graph_data["DeltaT"].append(deltat)
                graph_data["Height"].append(ThreatsHT[IDofInterest][i][0])
                graph_data["Lat"].append(ThreatsXY[IDofInterest][i][0])
                graph_data["Lon"].append(ThreatsXY[IDofInterest][i][1])
                graph_data["Distance"].append(distance(42, -70, ThreatsXY[IDofInterest][i][0], ThreatsXY[IDofInterest][i][1], ThreatsHT[IDofInterest][i][0]))

            else:
                next


        # corner case where the times are not in order already
        Coords = []
        for i in range(0,len(graph_data["DeltaT"])):
            Coords.append([graph_data["DeltaT"][i],graph_data["Height"][i],graph_data["Lat"][i], graph_data["Lon"][i]])
        
        sorted_coords = sorted(Coords)

        graph_data = {"Height":[], "DeltaT":[],"Lat":[],"Lon":[],"Distance":[]}
        for i in range(0, len(sorted_coords)):
            graph_data["DeltaT"].append(sorted_coords[i][0])
            graph_data["Distance"].append(distance(42, -70, sorted_coords[i][2], sorted_coords[i][3], sorted_coords[i][1]))

        # Find spline representation of each point's height vs. time graph

        x = graph_data["DeltaT"]
        y = graph_data["Distance"]

        if len(y) > 3:
            dist = splrep(x, y)

            # Evaluate spline at new points
            xnew = np.linspace(0, max(x), ceil(max(x)*60))

            distnew = splev(xnew, dist)
            xnew = list(xnew)
            distnew = list(distnew)

            T = 50

            m2s = []

            delta = xnew[1]

            for j in range((floor(len(xnew)/6))-(T+1)):
                m2s.append(m2(distnew,j,T,6))

            if len(m2s) > 0:
                if(np.isnan(m2s[0]) == False):
                    average_metric = mean(m2s)
                    if (average_metric < 0.5) & (average_metric > 0.2):
                        data.loc[data['ThreatId'] == IDofInterest, "Drone"] = 1
                        print(IDofInterest)
        else:
            print(f"Error from: {IDofInterest}")
            continue

    return data
