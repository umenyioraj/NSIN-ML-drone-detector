import os

input_directory = ""
output_directory = ""

for file in os.listdir(input_directory):
    filename = input_directory + os.fsdecode(file)
    if filename.endswith("DeviceAdds") or filename.endswith("DeviceUpdates"):

        specs = []
        specs.append(filename)

        datafile = open(filename, "r")
        content = datafile.read()
        datafile.close()

        deviceName = content[(content.find("DeviceName") + 13):content.find(",",content.find("DeviceName"))-1]
        specs.append(deviceName)

        startLocationStats = content.find("Emplacement\":{") + 14
        endLocationStats = content.find("}",startLocationStats)
        locationStats = content[startLocationStats:endLocationStats].split(",")
        for item in locationStats:
            specs.append(item.split(':')[1])

        outfile = open(output_directory, "a")
        outfile.write(','.join(specs)+"\n")
        outfile.close()