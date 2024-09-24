***************
parseHeaders.py
***************
Uses a recursive parsing method to parse the headers in each file and implement their names so that from left to right the header goes parent->child, similar to a class. Parses all of the files to make sure that every header possible is accounted for.

Ex: GrandparentHeader.ParentHeader.ChildHeader

******************
pandasEpochToDT.py
******************
Converts the Epoch times to datetime using the pandas library, then returns these in a text file with each dataframe value on a new line. Easy to export this text file to an Excel column.

Epoch time(in microseconds) -> Year-Month-Day Hour-Minute-Second

********************
parseDeviceCoords.py
********************
Parses all of the "DeviceAdds" data files, grabbing specific columns of interest and outputting the values for these keys to a csv that can be exported to Excel.

********************
parseThreatCoords.py
********************
Parses all of the "ThreatInfo","_Adds" data files, grabbing specific columns of interest and outputting the values for these keys to a csv that can be exported to Excel.

*************
getalldata.py
*************
Using the list of headers from parseHeaders.py, creates an empty list of the same size for each file and retrieves the value for each key in the headers, placing this value in the same index that the key appears in the list of headers. If the header is not in a file, the value is defaulted to '' for that line. Each list of values is written as a line in an output csv file, which can be exported to Excel.