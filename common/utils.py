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
