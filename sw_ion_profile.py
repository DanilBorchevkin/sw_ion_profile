# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 21:55:17 2019

@author: Danil Borchevkin
"""

import xarray as xr
import glob
import os

def process_file(filepath):
    data = []

    ds = xr.open_dataset(filepath)
    
    for alt in ds.coords['MSL_alt'].data:
        dsloc = ds.sel(MSL_alt=alt)
        buffer = "{}\t{}\t{}\t{}\n".format(

        data.append([
            alt, 
            dsloc.data_vars['ELEC_dens'].data, 
            dsloc.data_vars['GEO_lat'].data, 
            dsloc.data_vars['GEO_lon'].data)
        ])

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

    files = glob.glob("./input/*.*")    

    for filepath in files:
        print("Process >> " + filepath)

        data_to_save = process_file(filepath)
        out_filepath = "./output/" + os.path.basename(filepath) + ".dat"

        save_to_ascii_file(data_to_save, out_filepath)
        print("Saved to >>" + out_filepath)
        print()

    print("Script is finished")

if __name__ == "__main__":
    main()