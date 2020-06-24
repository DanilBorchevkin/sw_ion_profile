# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 21:55:17 2019

@author: Danil Borchevkin
"""

import xarray as xr
import glob
import os
import math

def process_file(filepath):
    '''
    Process nc input file

    Find fmax from each file and recalculate it by specific formula
    '''
    
    # [lon, lat, f, ne]
    data = [0, 0, 0, 0]

    ds = xr.open_dataset(filepath)
    
    for alt in ds.coords['MSL_alt'].data:
        dsloc = ds.sel(MSL_alt=alt)

        if data[3] < dsloc.data_vars['ELEC_dens'].data.item():
            data[0] = dsloc.data_vars['GEO_lon'].data.item()
            data[1] = dsloc.data_vars['GEO_lat'].data.item()
            data[3] = dsloc.data_vars['ELEC_dens'].data.item()

    # Calc critical freq F2
    data[2] = math.sqrt(data[3] / (1.24 * 10000))

    return data

def save_to_ascii_file(data_list, out_filepath, header=[]):
    write_list = []

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w") as f:
        f.writelines(write_list)

def main():
    print("Script is started")

    # Change output and filename here
    out_filepath = "./output/out_fmax.dat"

    files = glob.glob("./input/*.*")
    data_to_save = list()   

    for filepath in files:
        print("Process >> " + filepath)
        try:
            data_to_save.append(process_file(filepath))
        except:
            print("Cannot process file >> ", filepath)
        finally:
            pass
    
    print("Saved to >> " + out_filepath)
    save_to_ascii_file(data_to_save, out_filepath)

    print("Script is finished")

if __name__ == "__main__":
    main()