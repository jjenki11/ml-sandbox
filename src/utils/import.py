
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.co2Entry import *
from model.Entry import *
import pandas as pd
import numpy as np
#from tabulate import tabulate
import glob, os, pickle
import csv
from pprint import pprint
from pathlib import Path

project_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent
data_dir = str(project_dir)+"/data/"
merged_output_file = data_dir+"final_merged_dataset.csv"
temp_output_file = data_dir+"temperature_formatted.csv"

# global defs
big_dataset = {}
start_year = '1970'
end_year = '2012'

merged_years = list(range(int(start_year), int(end_year))) #since second number is exclusive
merged_header='country,year,co2_person,forest_coverage_pct,forest_coverage_km,land_coverage_km,total_greenhouse,total_population,global_temperature'
merged_and_formatted = []

### <<< USE TO FORMAT THE TEMPERATURE DATASET >>>
#global_temp=data_dir+'global_temperatures.csv'
#formatTemperatureData(global_temp)

def formatTemperatureData(filename):
    items = []
    row_count = 0
    for line in open(filename):
        if(row_count == 0):
            pass
        else:
            data_line = line.rstrip()
            items.append(data_line)
        row_count = row_count + 1
    # this code supports formatting of the global temperature dataset.
    temp_dict = {}
    last_entry = len(items[0].split(','))-1
    countries =[]
    formatted_temp_dict = {}
    # build unique country list and form year list
    years = []
    for item in items:        
        item_array = item.split(',')
        year = item_array[0].split('-')[0]    
        years.append(year)
        country = item_array[last_entry]
        countries.append(country)        
    # sort years
    uYears = list(set(years))
    nYears = np.array(uYears)
    nYears.sort()
    header = 'country,'+(",".join(nYears ))
    unique_countries = list(set(countries))
    for c in unique_countries:
        formatted_temp_dict[c] = [-100.0] * len(nYears)
        formatted_temp_dict[c].append(-100.0)
    for item in items:
        item_array = item.split(',')
        country = item_array[last_entry]
        date_idx = getIndexByYear(header.split(','), item_array[0].split('-')[0])
        # get index to put the data into
        set_list(formatted_temp_dict[country], date_idx, item_array[1])    
    with open(temp_output_file, 'a') as the_file:
        the_file.write(header+'\n')
        for c in unique_countries:            
            temp_entry = c+','+(",".join(str(i) for i in formatted_temp_dict[c]))
            the_file.write(temp_entry+'\n')
    print("Done converting data.")

def getIndexByYear(row, year):
    idx = 0
    for entry in row:
        if(entry == year):
            return idx
        idx = idx + 1

def set_list(l, i, v):
    try:
        l[i] = v
    except IndexError:
        for _ in range(i-len(l)+1):
            l.append(None)
        l[i] = v

def getDataByCountryAndYear(data, country, year):
    year_strings = map(str, merged_years)
    arr_idx = getIndexByYear(year_strings, year)
    dkeys = data.keys()
    ret_str = country+','+year
    for dk in dkeys:
        if(data[dk]):
            if(country in data[dk]):
                if(data[dk][country][arr_idx]):
                    cdata = data[dk][country][arr_idx]
                else:
                    cdata = '-100.0'
            else:
                cdata = '-100.0'
        else:
            cdata = '-100.0'
        ret_str = ret_str + ',' + cdata
    return ret_str

def performMapping(file_arr):
    bd = {}
    row_count = 0
    start_idx = 0
    end_idx = 0
    for mapping in file_arr:
        input_file = data_dir + mapping['filename']
        print('now working on input file >> ', input_file)
        for line in open(input_file):
            # get a line and convert to array
            data_line = line.rstrip().split(',')
            # get first row
            if(row_count == 0):
                start_idx = getIndexByYear(data_line, start_year)
                end_idx   = getIndexByYear(data_line, end_year)
            else:
                mapping['dict'][data_line[0]] = data_line[start_idx:end_idx+1]
                # sanity check for row length
                #print(len(data_line[start_idx:end_idx]))
            row_count = row_count + 1
        bd[mapping['label']] = mapping['dict']
        row_count = 0
    return bd

def getUniqueCountries(data):
    # eval all unique countries to normalize them
    all_countries = []
    bd_keys = data.keys()
    for k in bd_keys:
        country_keys = data[k].keys()
        for c in country_keys:
            all_countries.append(c)
    to_return = list(set(all_countries))
    to_return.sort()
    return to_return

def mergeDatasets(data, countries):
    # loop thru years.
    for my in merged_years:
        # loop thru countries
        for uc in countries:
            yr = str(my)
            new_pt = getDataByCountryAndYear(data, uc, yr)
            merged_and_formatted.append(new_pt)

    # if file exists, delete it and start over. otherwise, create one
    if os.path.exists(merged_output_file):
        print("The merged file exists... overwriting")
        os.remove(merged_output_file) 
    else: 
        print("The merged file does not exist... creating now")

    with open(merged_output_file, 'a') as the_file:
        the_file.write(merged_header+'\n')
        for c in merged_and_formatted:
            the_file.write(c+'\n')


###########################################################################################
###########################################################################################

# Define our data files and what their labels will be
data_info = [
    {'filename': "co2_emissions_tonnes_per_person.csv", 'dict' : {}, 'label': 'co2_person'},
    {'filename': "forest_percent_coverage.csv", 'dict' : {}, 'label': 'forest_coverage_pct'},
    {'filename': "forest_km_coverage.csv", 'dict' : {}, 'label': 'forest_coverage_km'},
    {'filename': "land_km_coverage.csv", 'dict' : {}, 'label': 'land_coverage_km'},
    {'filename': "greenhouse_gas_totals.csv", 'dict' : {}, 'label': 'total_greenhouse'},
    {'filename': "population_totals.csv", 'dict' : {}, 'label': 'total_population'},
    {'filename': "temperature_formatted.csv", 'dict' : {}, 'label': 'global_temperature'},
]

# Define a big 'json' dataset from multiple files which have same structure (rougly)
big_dataset = performMapping(data_info)

# Form a list of unique countries found in all files (need to make sure we normalize the names)
all_unique_countries = getUniqueCountries(big_dataset)

# NOW we merge all of these dicts into the same file!
mergeDatasets(big_dataset, all_unique_countries)

print("DONE!")
print("The resulting merged dataset is located > ", merged_output_file)
exit()