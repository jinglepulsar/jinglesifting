import pandas as pd
pd.options.mode.chained_assignment = None
import argparse
import datetime
import os
from tqdm import tqdm
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import libsift

def main():
    # import matplotlib
    # matplotlib.use('Agg')
    # print (matplotlib.rcParams['backend'])
    # Arguments setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--hdfpath", \
                        help = "The path of candidates list in HDF format, str value", \
                        type = str, \
                        required = True)
    parser.add_argument("--ndecimals", \
                        help = "Number of digits used for grouping, int value", \
                        type = int, \
                        required = False, \
                        default = 6)
    parser.add_argument("--minpts", \
                        help="Threshold for to draw figures > minpts, int value", \
                        type = int, \
                        required = False, \
                        default = 3)
    parser.add_argument("--maxp", \
                        help = "Threshold for to draw figures < maxp max period, float value", \
                        type = float, \
                        required = False, \
                        default = 10000.)                        
    parser.add_argument("--cmdpath", \
                        help = "Number of digits used for grouping, str value", \
                        type = str, \
                        required = False, \
                        default = 1)
    parser.add_argument("--minsigma", \
                        help = "Number of digits used for grouping, str value", \
                        type = int, \
                        required = False, \
                        default = 1)
    # Internalize arguments
    args = parser.parse_args()
    hdf_path = args.hdfpath
    ndecimals = args.ndecimals
    cmd_path = args.cmdpath
    min_points = args.minpts
    max_period = args.maxp/1000

    # cmd pattern in pyformat
    cmd_pattern  = "prepfold -topo -nosearch -noxwin -npart 256 -mask all_rfifind.mask -nsub 256 -p {} -dm {:.2f} $a"
    #cmd_acc_pattern = "prepfold -topo -nosearch -noxwin -npart 256 -mask all_rfifind.mask -nsub 256 -p {} -dm {:.2f} -accelfile {} -accelcand {} $a"
    cmd_acc_pattern = "prepfold -topo -nosearch -noxwin -npart 256 -mask  /data1/rfifind_result/{}_rfifind.mask -nsub 256 -dm {:.2f} -accelfile /data1/all_tmp/{}_DM{:2.2f}_ACCEL_0.cand -accelcand {} /data1/filterbank/{}.dat.fil"
                     #"prepfold -topo -nosearch -noxwin -npart 256 -mask  /data1/rfifind_result/47T078_0031_rfifind.mask -nsub 256 -p 0.00144361670547 -dm 23.50 -accelfile /data1/all_tmp/47T078_0031_DM23.50_ACCEL_0.cand -accelcand 304 /data1/filterbank/47T078_0031.dat.fil"
    cmd_pattern_mask = "prepfold -topo -nosearch -noxwin -npart 256 -mask  {}_rfifind.mask -nsub 256 -dm {:.2f} -accelfile /{}_DM{:2.2f}_ACCEL_{}.cand -accelcand {} /{}.fits -o ./{}"

    # TEST
    # Read in HDF5 Candidates list
    df = libsift.read_in_hdf(hdf_path)
    # sift into group
    gp = libsift.bin_sift(df[df["p"] < max_period], ndecimals)
    # generate prepfold cmd of candidates with highest sigma in each group
    #generate_prepfold_cmd(gp.first(), cmd_pattern, cmd_path)
    # generate prepfold acc cmd of candidates with highest sigma in each group
    #generate_prepfold_acc_cmd(gp.first(), cmd_acc_pattern, "acc" + cmd_path, "200")
    # draw distribution of each group
    libsift.draw_group_xy(gp, min_points) # groups less than 20 will 

#############################################
if __name__ == "__main__":
    main()