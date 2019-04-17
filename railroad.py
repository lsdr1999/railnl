from station import Station
import csv

class Railroad(object):
    """
    Class that connects the stations with each other, forming the foundation
    for different tracks
    """

    def __init__(self):
        self.station_dict = {}
        self.connections = {}
        self.totalCritical = []

    def loadStations(self):
        # Open the Stations file and create empty station dictionaryd
        with open("csv_bestanden/StationsHolland.csv") as f:
            stations = {}
            # Iterate over the lines
            for line in f:

                # Split the lines into words and save them into seperate variables
                station_data = (line.split(','))
                name = station_data[0]
                xcoordinate = station_data[1]
                ycoordinate = station_data[2]

                # If the station is critical save "Kritiek" as a boolean
                if station_data[3] == "Kritiek\n":
                    critical = True
                else:
                    critical = False

                # Initialize a station object and save it in a dictionary with
                # its name as the key
                station = Station(name, xcoordinate, ycoordinate, critical)
                self.addStation(name, critical)
                stations[name] = station
        # Close the file
        f.close()

        # Open the the connections files
        with open("csv_bestanden/ConnectiesHolland.csv") as g:
            ID_counter = 0
            # Iterate over the lines
            for line in g:

                # Split the words on each lines and save them in seperate variables
                connection_data = line.split(',')
                station1 = connection_data[0]
                station2 = connection_data[1]
                time = int(connection_data[2])
                Connection_ID = int(ID_counter)
                ID_counter += 1

                # If one of the stations in the connection is critical, save the
                # connection as a critical connection
                if stations[station1].critical or \
                    stations[station2].critical:
                    stations[station1].addConnection(station2, time, True)
                    stations[station2].addConnection(station1, time, True)

                    self.addConnection(Connection_ID, station1, station2, time, True)

                # If neither station is critical, save it as a non-critical connection
                else:
                    stations[station1].addConnection(station2, time, False)
                    stations[station2].addConnection(station1, time, False)

                    self.addConnection(Connection_ID, station1, station2, time, False)

        for key, value in self.connections.items():
            print(key, value)

        # Close the file
        g.close()

    def addStation(self, stationname, critical):
        self.station_dict[stationname] = [stationname, critical]

    def addConnection(self, ID, station1, station2, time, critical):
        self.connections[ID] = [station1, station2, time, critical]

    def addTotalCritical(self):
        print(len(self.connections))
        for key,value in self.connections.items():
            if value[3]:
                self.totalCritical.append([value[0], value[1]])
        print(len(self.totalCritical))
        return len(self.totalCritical)
        # Als een unit in connecties dictionary kritiek is, dan voeg em toe aan lijst total criticalConnection
        # return volledige lijst (naar Dienstregeling)

if __name__ == "__main__":
    railroad = Railroad()
    railroad.loadStations()
    railroad.addTotalCritical()
