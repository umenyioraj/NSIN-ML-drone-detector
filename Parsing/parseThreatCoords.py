import os
import time

input_directory = ""
output_directory = ""

for file in os.listdir(input_directory):
    filename = input_directory + os.fsdecode(file)
    if filename.endswith("_Adds"):

        specs = []
        specs.append(filename)

        datafile = open(filename, "r")
        content = datafile.read()
        datafile.close()

        deviceName = content[(content.find("ThreatId") + 10):content.find(",",content.find("ThreatId"))]
        specs.append(deviceName)

        detectionTime = content[(content.find("DetectionTime") + 15):content.find(",",content.find("DetectionTime"))]
        specs.append(detectionTime)

        if content.find("Location\":{") != -1:
            startLocationStats = content.find("Location\":{") + 11
            endLocationStats = content.find("}",startLocationStats)
            locationStats = content[startLocationStats:endLocationStats].split(",")
            for item in locationStats:
               if item != "null":
                    specs.append(item.split(':')[1])

        if content.find("PredictedLocation\":{") != -1:
            startPredictedLocationStats = content.find("PredictedLocation\":{") + 20
            endPredictedLocationStats = content.find("}",startPredictedLocationStats)
            PredictedlocationStats = content[startPredictedLocationStats:endPredictedLocationStats].split(",")
            for item in PredictedlocationStats:
                if item != "null":
                    specs.append(item.split(':')[1])

        outfile = open(output_directory, "a")
        outfile.write(','.join(specs)+"\n")
        outfile.close()