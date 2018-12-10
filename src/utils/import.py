
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.co2Entry import *
from model.Entry import *

import pandas as pd
import numpy as np
from tabulate import tabulate
import glob, os, pickle



print("WOOHOO")

e = Entry({'a':'1','b':'2'})
e.printEntry()

ce = co2Entry({'c':'3','d':'4'})
ce.printco2Entry()

def PrintData(data):
    print(tabulate(data, headers='keys', tablefmt='fancy_grid'))

def CsvToDataset(filename):
    return pd.read_csv(filename, header=0).dropna()

from pathlib import Path
project_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent
co2_per_person = str(project_dir)+"/data/co2_emissions_tonnes_per_person.csv"
#print(os.path.dirname(os.path.dirname(os.path.abspath())))

dataset = CsvToDataset(co2_per_person)

PrintData(dataset)


