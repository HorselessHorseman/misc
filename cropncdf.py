#!/usr/bin/env python3
from netCDF4 import Dataset
import argparse
import re
import sys
import numpy as np

for i, arg in enumerate(sys.argv):      # workaround to parse negative numbers
    if (arg[0] == "-") and arg[1].isdigit(): sys.argv[i] = " " + arg

#describe and parse arguments
parser = argparse.ArgumentParser(description="Crop ncdf files and export to plain text.")
parser.add_argument("path", nargs="+", help="paths to ncdf files")
parser.add_argument("--ds", help="decimal separator(default: comma)")
parser.add_argument("--lon", help="longitude")
parser.add_argument("--lat", help="latitude", type=str)
parser.add_argument("-t", "--time", help="time in the same format as in the dataset")
parser.add_argument("-o", "--output", help="output file")
parser.set_defaults(ds=",") 
args = parser.parse_args()


for i in args.path:
    print(i)
    nc = Dataset(i)
    for i in nc.dimensions:
        print(str(i))
        print("["+str(nc.variables[str(i)][0])+" - "+str(nc.variables[str(i)][-1])+"]")
    print()

def find_nearest(array, value):
    array = np.asarray(array)
    idx = np.abs(array - value).argmin()
    return idx

def weirdIndices(index, variable, nc):
    return find_nearest(nc.variables[variable][:], (min(nc.variables[variable][:], key=lambda x:abs(x-index))))

nc = Dataset(args.path[0])
#print(str(weirdIndices(20080000, "time", nc = Dataset(args.path[0]))))
# make slice objects for convenience
def parse_arg(arg, dimension, regex="\d+"):
    global nc
    if arg:
        if len(re.findall(regex, arg)) == 2:
            return np.s_[weirdIndices(int(re.findall(regex, arg)[0]), dimension, nc):weirdIndices(int(re.findall(regex, arg)[1]), dimension, nc)]
        elif len(re.findall(regex, arg)) == 1:
            return np.s_[weirdIndices(int(re.findall(regex, arg)[0]), dimension, nc):weirdIndices(int(re.findall(regex, arg)[0]), dimension, nc)+1]
    else:
        return slice(None)
lon = parse_arg(args.lon, "lon")
lat = parse_arg(args.lat, "lat", r"-?\d+")
time = parse_arg(args.time, "time")

items_written = 0
if args.output:
    with open(args.output, "w") as output:
        for i in args.path:
            nc = Dataset(i)
            output.write(i+"\n")
            for ii in nc.variables.keys()-nc.dimensions.keys():
                print(nc.variables[ii][time, lat, lon])
                for k in nc.variables[ii][time, lat, lon]:
                    for j in k:
                        output.write(" ".join(str(l).replace(".", args.ds) for l in j)+"\n")
                        items_written += 1
                    output.write("\n")
                output.write("\n")
print(items_written)
