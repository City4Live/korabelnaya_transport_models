import subprocess
import pandas as pd

from xml.sax import make_parser
from statisticsElements import VehInformationReader

def run_process(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return (stdout, stderr)

def read_tripinfo_file(filename, vehicles):
    parser = make_parser()
    parser.setContentHandler(VehInformationReader(vehicles))
    parser.parse(filename)

def get_stats(filename):
    vehicles = []
    read_tripinfo_file(filename, vehicles)

    ids = []
    flow_values = []
    depart_time_values = []
    arrival_time_values = []
    travel_time_values = []
    wait_time_values = []

    for v in vehicles:
        f = v.label.split('.')[0]
        if '-' in f:
            f = f.split('-')[0]

        ids.append(v.label)
        flow_values.append(f)
        depart_time_values.append(v.depart)
        arrival_time_values.append(v.arrival)
        travel_time_values.append(v.traveltime)
        wait_time_values.append(v.waittime)

    return pd.DataFrame(
        {
            "id": pd.Series(ids),
            "flow": pd.Categorical(flow_values),
            "departTime": pd.Series(depart_time_values),
            "arrivalTime": pd.Series(arrival_time_values),
            "travelTime": pd.Series(travel_time_values),
            "waitTime": pd.Series(wait_time_values)
        }
    )