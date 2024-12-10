import os, pandas as pd, numpy as np

def parseInfile(filename):
    datafile = open(filename, "r")
    data = datafile.read()
    datafile.close()

    headers_list = ['ThreatId', 'SourceSystem', 'ThreatName', 'Priority', 'Description', 'Affiliation', 'Location', 'Location.Latitude', 'Location.Longitude', 'Location.Altitude', 'PredictedLocation', 'PredictedLocation.Latitude', 'PredictedLocation.Longitude', 'PredictedLocation.Altitude', 'DetectionTime', 'IsEndThreat', 'Heading', 'Heading.Type', 'Heading.Polar', 'Heading.Vector', 'Heading.DataCase', 'Speed', 'Eta', 'GroupId', 'SignalConfidence', 'SourceTypes', 'SourceTypes.IsNinjaThreat', 'SourceTypes.IsCoyoteInterceptorThreat', 'SourceTypes.IsCoyoteTargetThreat', 'OverallClassType', 'Ninja', 'SymbolCode', 'Tracks.TrackId', 'Tracks.Timestamp', 'Tracks.SourceSystem', 'Tracks.SourceDevice', 'Tracks.SymbolCode', 'Tracks.Affiliation', 'Tracks.TrackType', 'Tracks.IsBegin', 'Tracks.IsEnd', 'Tracks.Spatial', 'Tracks.Spatial.Position', 'Tracks.Spatial.Position.Lla', 'Tracks.Spatial.Position.Ecef', 'Tracks.Spatial.Position.Ecef.X', 'Tracks.Spatial.Position.Ecef.Y', 'Tracks.Spatial.Position.Ecef.Z', 'Tracks.Spatial.Position.DataCase', 'Tracks.Spatial.Velocity', 'Tracks.Spatial.Velocity.X', 'Tracks.Spatial.Velocity.Y', 'Tracks.Spatial.Velocity.Z', 'Tracks.Spatial.PositionCovariance', 'Tracks.Lob', 'Tracks.Lob.Azimuth', 'Tracks.Lob.Elevation', 'Tracks.Lob.AzimuthError', 'Tracks.Lob.ElevationError', 'Tracks.Lob.MinRange', 'Tracks.Lob.MaxRange', 'Tracks.Lob.OriginPosition', 'Tracks.Ballistics', 'Tracks.Ballistics.IsFinal', 'Tracks.Ballistics.Impact', 'Tracks.Ballistics.Origin', 'Tracks.Classification', 'Tracks.Classification.Type', 'Tracks.Classification.IsManMade', 'Tracks.Classification.Confidence', 'Discriminations.Confidence', 'Discriminations.Feature', 'Tracks.Acoustic', 'Tracks.Acoustic.SignalType', 'Tracks.Acoustic.SignalConfidence', 'Tracks.Acoustic.AbsoluteAmplitude', 'Tracks.Acoustic.RelativeAmplitude', 'Tracks.Acoustic.Frequency', 'Tracks.Acoustic.FundamentalFrequency', 'Tracks.Rf', 'Tracks.Rf.SignalType', 'Tracks.Rf.Approaching', 'Tracks.Rf.Bandwidth', 'Tracks.Rf.ChannelCount', 'Tracks.Rf.Density', 'Tracks.Rf.DetectionCount', 'Tracks.Rf.Frequency', 'Tracks.Rf.GroupId', 'Tracks.Rf.MacAddress', 'Tracks.Rf.NoiseStrength', 'Tracks.Rf.PulseWidth', 'Tracks.Rf.Pri', 'Tracks.Rf.SignalConfidence', 'Tracks.Rf.SignalStrength', 'Tracks.Rf.Video', 'Tracks.Feature', 'Tracks.Feature.Countermeasures', 'Tracks.Feature.Coyote', 'Tracks.Feature.Importance', 'Tracks.Feature.DataCase', 'Ninja.MacAddress', 'Ninja.OverallSignalType', 'Ninja.DroneModel', 'Tracks.Lob.OriginPosition.Lla', 'Tracks.Lob.OriginPosition.Lla.Latitude', 'Tracks.Lob.OriginPosition.Lla.Longitude', 'Tracks.Lob.OriginPosition.Lla.Altitude', 'Tracks.Lob.OriginPosition.Ecef', 'Tracks.Lob.OriginPosition.DataCase', 'Tracks.Feature.Importance.Importance', 'Countermeasures.DeviceId', 'Countermeasures.Countermeasure', 'Countermeasures.State', 'Tracks.Feature.Countermeasures.DroneModel', 'Countermeasures.DroneModel', 'DetectionTimeInDT']

    data = data.replace("[","{")
    data = data.replace("]","}")
    data = data.replace("{","")
    data = data.replace("}","")
    values = [''] * (len(headers_list))

    for header in headers_list:
        value = ''
        if header.find(".") != -1:
            item = header.split('.')
            if len(item) == 2:
                start = data.find(":",data.find(item[1],data.find(item[0]))) + 1
                if start != 0:
                    value = data[start:data.find(",",start)]
            elif len(item) == 3:
                start = data.find(":",data.find(item[2],data.find(item[1],data.find(item[0])))) + 1
                if start != 0:
                    value = data[start:data.find(",",start)]
            elif len(item) == 4:
                start = data.find(":",data.find(item[3],data.find(item[2],data.find(item[1],data.find(item[0]))))) + 1
                if start != 0:
                    value = data[start:data.find(",",start)]
            elif len(item) == 5:
                start = data.find(":",data.find(item[4],data.find(item[3],data.find(item[2],data.find(item[1],data.find(item[0])))))) + 1
                if start != 0:
                    value = data[start:data.find(",",start)]
        else:
            start = data.find(":",data.find(header)) + 1
            if start != 0:
                value = data[start:data.find(",",start)]
        if str(value).find(":") == -1:
            values[headers_list.index(header)] = str(value)

    values[len(values)-1] = str(pd.to_datetime(float(values[headers_list.index('DetectionTime')]),unit='us', errors='coerce'))

    df = pd.DataFrame([values], columns=headers_list)
    df.columns = df.columns.str.strip() #There's extra white space in the data
    df.columns = df.columns.str.replace("'", "") #The columns already contain quotes we need to remove 

    return df

def getData(input_directory):

    outpfile = "output.txt"
    headers_list = ['ThreatId', 'SourceSystem', 'ThreatName', 'Priority', 'Description', 'Affiliation', 'Location', 'Location.Latitude', 'Location.Longitude', 'Location.Altitude', 'PredictedLocation', 'PredictedLocation.Latitude', 'PredictedLocation.Longitude', 'PredictedLocation.Altitude', 'DetectionTime', 'IsEndThreat', 'Heading', 'Heading.Type', 'Heading.Polar', 'Heading.Vector', 'Heading.DataCase', 'Speed', 'Eta', 'GroupId', 'SignalConfidence', 'SourceTypes', 'SourceTypes.IsNinjaThreat', 'SourceTypes.IsCoyoteInterceptorThreat', 'SourceTypes.IsCoyoteTargetThreat', 'OverallClassType', 'Ninja', 'SymbolCode', 'Tracks.TrackId', 'Tracks.Timestamp', 'Tracks.SourceSystem', 'Tracks.SourceDevice', 'Tracks.SymbolCode', 'Tracks.Affiliation', 'Tracks.TrackType', 'Tracks.IsBegin', 'Tracks.IsEnd', 'Tracks.Spatial', 'Tracks.Spatial.Position', 'Tracks.Spatial.Position.Lla', 'Tracks.Spatial.Position.Ecef', 'Tracks.Spatial.Position.Ecef.X', 'Tracks.Spatial.Position.Ecef.Y', 'Tracks.Spatial.Position.Ecef.Z', 'Tracks.Spatial.Position.DataCase', 'Tracks.Spatial.Velocity', 'Tracks.Spatial.Velocity.X', 'Tracks.Spatial.Velocity.Y', 'Tracks.Spatial.Velocity.Z', 'Tracks.Spatial.PositionCovariance', 'Tracks.Lob', 'Tracks.Lob.Azimuth', 'Tracks.Lob.Elevation', 'Tracks.Lob.AzimuthError', 'Tracks.Lob.ElevationError', 'Tracks.Lob.MinRange', 'Tracks.Lob.MaxRange', 'Tracks.Lob.OriginPosition', 'Tracks.Ballistics', 'Tracks.Ballistics.IsFinal', 'Tracks.Ballistics.Impact', 'Tracks.Ballistics.Origin', 'Tracks.Classification', 'Tracks.Classification.Type', 'Tracks.Classification.IsManMade', 'Tracks.Classification.Confidence', 'Discriminations.Confidence', 'Discriminations.Feature', 'Tracks.Acoustic', 'Tracks.Acoustic.SignalType', 'Tracks.Acoustic.SignalConfidence', 'Tracks.Acoustic.AbsoluteAmplitude', 'Tracks.Acoustic.RelativeAmplitude', 'Tracks.Acoustic.Frequency', 'Tracks.Acoustic.FundamentalFrequency', 'Tracks.Rf', 'Tracks.Rf.SignalType', 'Tracks.Rf.Approaching', 'Tracks.Rf.Bandwidth', 'Tracks.Rf.ChannelCount', 'Tracks.Rf.Density', 'Tracks.Rf.DetectionCount', 'Tracks.Rf.Frequency', 'Tracks.Rf.GroupId', 'Tracks.Rf.MacAddress', 'Tracks.Rf.NoiseStrength', 'Tracks.Rf.PulseWidth', 'Tracks.Rf.Pri', 'Tracks.Rf.SignalConfidence', 'Tracks.Rf.SignalStrength', 'Tracks.Rf.Video', 'Tracks.Feature', 'Tracks.Feature.Countermeasures', 'Tracks.Feature.Coyote', 'Tracks.Feature.Importance', 'Tracks.Feature.DataCase', 'Ninja.MacAddress', 'Ninja.OverallSignalType', 'Ninja.DroneModel', 'Tracks.Lob.OriginPosition.Lla', 'Tracks.Lob.OriginPosition.Lla.Latitude', 'Tracks.Lob.OriginPosition.Lla.Longitude', 'Tracks.Lob.OriginPosition.Lla.Altitude', 'Tracks.Lob.OriginPosition.Ecef', 'Tracks.Lob.OriginPosition.DataCase', 'Tracks.Feature.Importance.Importance', 'Countermeasures.DeviceId', 'Countermeasures.Countermeasure', 'Countermeasures.State', 'Tracks.Feature.Countermeasures.DroneModel', 'Countermeasures.DroneModel','DetectionTimeInDT']
    line = ','.join(headers_list)
    outfile = open(outpfile, "a")
    outfile.write(line + '\n')
    outfile.close()

    for file in os.listdir(input_directory):
        filename = input_directory + os.fsdecode(file)
        if filename.endswith("_Adds"):
            datafile = open(filename, "r")
            data = datafile.read()
            datafile.close()

            data = data.replace("[","{")
            data = data.replace("]","}")
            data = data.replace("{","")
            data = data.replace("}","")
            values = [''] * (len(headers_list))

            for header in headers_list:
                value = ''
                if header.find(".") != -1:
                    item = header.split('.')
                    if len(item) == 2:
                        start = data.find(":",data.find(item[1],data.find(item[0]))) + 1
                        if start != 0:
                            value = data[start:data.find(",",start)]
                    elif len(item) == 3:
                        start = data.find(":",data.find(item[2],data.find(item[1],data.find(item[0])))) + 1
                        if start != 0:
                            value = data[start:data.find(",",start)]
                    elif len(item) == 4:
                        start = data.find(":",data.find(item[3],data.find(item[2],data.find(item[1],data.find(item[0]))))) + 1
                        if start != 0:
                            value = data[start:data.find(",",start)]
                    elif len(item) == 5:
                        start = data.find(":",data.find(item[4],data.find(item[3],data.find(item[2],data.find(item[1],data.find(item[0])))))) + 1
                        if start != 0:
                            value = data[start:data.find(",",start)]
                else:
                    start = data.find(":",data.find(header)) + 1
                    if start != 0:
                        value = data[start:data.find(",",start)]
                if str(value).find(":") == -1:
                    values[headers_list.index(header)] = str(value)

            values[len(values)-1] = str(pd.to_datetime(float(values[headers_list.index('DetectionTime')]),unit='us', errors='coerce'))
            # parsed_data.append(values)
    
            line = ','.join(values)
            outfile = open(outpfile, "a")
            outfile.write(line + '\n')
            outfile.close()


    df = pd.read_csv(outpfile, engine='python')
    os.remove(outpfile)
    df.columns = df.columns.str.strip() #There's extra white space in the data
    df.columns = df.columns.str.replace("'", "") #The columns already contain quotes we need to remove 

    return df