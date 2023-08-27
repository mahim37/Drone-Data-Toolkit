import csv

import simplekml


def generate_kml_from_csv(csv_filename, kml_filename):
    # Create a KML object

    # install simplekml module using command "pip install simplekml"
    # to run script: > python ./convert2kml.py

    # Specify file names (input: CSV format)
    fileIN = csv_filename
    fileOUT = kml_filename
    delimiterIN = ','
    headerlines = 8

    kml = simplekml.Kml()

    with open(fileIN, 'r') as csvfile:

        csvreader = csv.reader(csvfile, delimiter=delimiterIN)
        for index in range(headerlines):
            next(csvreader)  # skip header

        for row in csvreader:
            # nameIN = row[0]  #zero indexing
            # print(row)
            nameIN = ''
            latIN = row[0]
            # print(row[1])
            longIN = row[1]
            pnt = kml.newpoint(name=nameIN, coords=[(longIN, latIN)])
            pnt.style.iconstyle.scale = 1

    kml.save(fileOUT)
