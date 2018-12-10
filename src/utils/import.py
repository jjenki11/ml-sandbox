
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.co2Entry import *
from model.Entry import *

import pandas as pd
import numpy as np
#from tabulate import tabulate
import glob, os, pickle

import csv





print("WOOHOO")

e = Entry({'a':'1','b':'2'})
e.printEntry()

ce = co2Entry({'c':'3','d':'4'})
ce.printco2Entry()

from pathlib import Path
project_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent

data_dir = str(project_dir)+"/data/"

co2_per_person = data_dir + "co2_emissions_tonnes_per_person.csv"


f = open(co2_per_person)

co2_dict = {}

data = []
for line in f:
    data_line = line.rstrip().split(',')
    data.append(data_line)
    co2_dict[data_line[0]] = data_line[2:-1]

print(co2_dict)
