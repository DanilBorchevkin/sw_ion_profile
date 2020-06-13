# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 21:55:17 2019

@author: Danil Borchevkin
"""

import xarray as xr
import glob
import os

def process_file(filepath, use_coords=False, min_lat=0, max_lat=0, min_long=0, max_long=0):
    '''
    Process nc input file

    For get all data use use_coords=False

    For use min\max - set use_coords=True and set appritiate values
    '''

    data = []

    ds = xr.open_dataset(filepath)
    
    for alt in ds.coords['MSL_alt'].data:
        dsloc = ds.sel(MSL_alt=alt)
        
        current_lat = dsloc.data_vars['GEO_lat'].data.item()
        current_long = dsloc.data_vars['GEO_lon'].data.item()

        if use_coords == True:
            if (min_lat <= current_lat <= max_lat) and (min_long <= current_long <= max_long):
                pass
            else:
                continue

        data.append([
            alt, 
            dsloc.data_vars['ELEC_dens'].data.item(), 
            dsloc.data_vars['GEO_lat'].data.item(), 
            dsloc.data_vars['GEO_lon'].data.item()])

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

    # For save all data set use_coords = False
    # For restrict data by min\max set use_coords = True and fix needed ranges by min\max values
    use_coords = True
    min_lat = -20.0
    max_lat = -15.0
    min_long = 30.0
    max_long = 35.0

    files = glob.glob("./input/*.*")    

    for filepath in files:
        print("Process >> " + filepath)

        try:
            data_to_save = process_file(filepath, use_coords, min_lat, max_lat, min_long, max_long)
            out_filepath = "./output/" + os.path.basename(filepath) + ".dat"
            
            if (len(data_to_save) > 0):
                save_to_ascii_file(data_to_save, out_filepath)
                print("Saved to >> " + out_filepath)
            else:
                print("No data for saving. Ignoring")
            
        except:
            print("Cannot process >> ", filepath)
            
        finally:
            print()

    print("Script is finished")

if __name__ == "__main__":
    main()