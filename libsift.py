import pandas as pd
import argparse
import datetime
import os
from tqdm import tqdm
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm

# class libsift(object):
#     def __init__(self, ):
#         self.hdf_path 
def read_in_hdf(hdf_path):
    # TODO Exception dealing

    # Print start
    print ("Reading HDF5 Candidate List...")
    # Timing starts
    start = datetime.datetime.now()
    # Read the HDF5
    df = pd.read_hdf(hdf_path, "df")
    # Timeing ends
    end = datetime.datetime.now()
    # Delta T
    time_consummed = end-start
    # Print time consumed
    print ("done within {} seconds".format(time_consummed.seconds))
    
    return df

def bin_sift(cand_df, num_of_decimals):
    n = num_of_decimals
    cand_df["P0r"] = cand_df["p"].map(lambda x: round(x * 10 ** int(n)) / 10 ** int(n))
    gp = cand_df.sort_values('sigma', ascending = False).groupby(['P0r'])
        
    return gp #groupby_obj

def group_log(idx):
    return idx
    pass

def bin_sift_relative(cand_df, num_of_decimals):
    n = num_of_decimals
    cand_df["P0r"] = cand_df["p"].map(lambda x: round(x * 10 ** int(n)) / 10 ** int(n))
    gp = cand_df.sort_values('sigma', ascending = False).groupby(['P0r'])
        
    return gp #groupby_obj

def draw_group_xy(sifted_gp, min_num_points = 20):
    # Just don't like this warning ;P
    import warnings
    warnings.filterwarnings("ignore")
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 28})
    plt.rcParams.update({'figure.subplot.hspace': 0.3})
    plt.rc('font', family='serif')
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    #plt.rc('text', usetex=True)

    path = "./figs/"
    # Create dir
    try:  
        os.mkdir(path)
    except OSError:  
        print ("Directory {} exists".format(path))
    else:  
        print ("Successfully created the directory {} ".format(path))
    
    # Print start
    print ("Drawing figs into ./figs dir...")
    # Timing starts
    start = datetime.datetime.now()
    # Draw!
    fig_count = 0
    for name, group in sifted_gp:
        if group.count()["sigma"] < min_num_points:
            continue
        p = group['p'].iloc[0]
        filename = group['filename'].iloc[0]
        candnum = group['candnum'].iloc[0]
        #fig = group[["DM", "sigma"]].plot.scatter(x='DM', y='sigma', c='DarkBlue', title='p(max sigma): {:2.10f}\n {} | {}'.format(p, filename, candnum)).get_figure()
        fig = plt.figure(figsize = (20, 20))
        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2)
        plt.rcParams.update({'axes.titlepad': 50})
        plt.rcParams.update({'axes.formatter.useoffset': False})
        plt.rcParams.update({'axes.linewidth': 0.8})
        #from sigfig import round 
        #group[["DM", "sigma"]].plot.scatter(x='DM', y='sigma', c='DarkBlue', title='p(max sigma): {:2.10f}\n {} | {}'.format(p, filename, candnum), ax = ax1)
        #group[["DM", "sigma", "p"]].plot.scatter(x='DM', y='sigma', c='p', s = 100, colormap=cm.get_cmap("jet"), title='p(max sigma): {:2.10f}\n {} | {}'.format(p, filename, candnum), ax = ax1)
        group["Period (ms)"] = group["p"].map(lambda x: x*1000)
        group[["DM", "sigma", "Period (ms)"]].\
            plot.scatter(x='DM', \
                            y='sigma', \
                            c='Period (ms)', \
                            s = 100, \
                            colormap=cm.get_cmap("Greys"), \
                            #colormap=cm.get_cmap("jet"), \
                            edgecolor="black", \
                            title='Period (max sigma): {:.5g} ms\n FILE: {} | CAND#: {}'.format(p*1000, filename, candnum), \
                            #label = "test", \
                            ax = ax1 \
                        )
        ax1.set_xlabel("DM (pc cm-3)")
        ax1.set_ylabel("Sigma")
        #cb = ax1.get_legend_handles_labels()
        #cb.set_label("test")
        #ax1.rcParams.update({'axes.titlepad': 10})
        #ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        group[["Period (ms)"]].plot.hist(bins = 40, ax = ax2, legend = None, color = "black")
        ax2.set_xlabel("Period (ms)")
        ax2.set_ylabel("Candidate count")
        for label in ax2.xaxis.get_ticklabels():
            # label is a Text instance
            label.set_rotation(45)
            label.set_fontsize(24)
        #ax2.get_legend().remove()
        fig.savefig("./figs/scatter_{}.png".format(name))
        fig.savefig("./figs/scatter_{}.eps".format(name))
        plt.close(fig)
        #save a table of the group
        group[["path", "filename", "candnum", "p", "sigma", "DM"]].to_csv("./figs/scatter_{}.txt".format(name), header=True, index=False, sep='\t', mode='w')
        fig_count += 1
    # Timeing ends
    end = datetime.datetime.now()
    # Delta T
    time_consummed = end-start
    # Print time consumed
    print ("{} figures done in {} seconds".format(fig_count, time_consummed.seconds))
    return time_consummed # TODO Redesign needed

def generate_prepfold_cmd(df, cmd_pattern, cmd_path):
    # Init cmd content
    content = ""
    # Print start
    print ("Generating prepfold cmd...")
    # Timing starts
    start = datetime.datetime.now()
    # Generate prepfold TODO Performance optimization
    for row in df.iterrows():
        p = row[1]["p"]
        dm = row[1]["DM"]
        content += cmd_pattern.format(p, dm) + "\n"
    # Timeing ends
    end = datetime.datetime.now()
    # Delta T
    time_consummed = end-start
    # Print time consumed
    print ("done within {} seconds".format(time_consummed.seconds))

    # Print start
    print ("Writing prepfold into file...")
    # Timing starts
    start = datetime.datetime.now()
    # Write into file
    with open(cmd_path, "w") as f:
        f.write(content)
    # Timeing ends
    end = datetime.datetime.now()
    # Delta T
    time_consummed = end-start
    # Print time consumed
    print ("done within {} seconds".format(time_consummed.seconds))
    
    return True

def generate_prepfold_acc_cmd(df, cmd_pattern, cmd_path, acc):
    # Init cmd content
    content = ""
    # Print start
    print ("Generating prepfold acc cmd...")
    # Timing starts
    start = datetime.datetime.now()
    # Generate prepfold TODO Performance optimization
    #for row in df[["path", "filename", "DM", "p", "candnum"]].iterrows():
    for row in df.iterrows():
        path = row[1]["path"]
        p = row[1]["p"]
        dm = row[1]["DM"]
        filename = row[1]["filename"]
        filelabel = filename[:11]
        candnum = row[1]["candnum"]
        content += cmd_pattern.format(filelabel, dm, filelabel, dm, acc, candnum, filelabel) + "\n"
    # Timeing ends
    end = datetime.datetime.now()
    # Delta T
    time_consummed = end-start
    # Print time consumed
    print ("done within {} seconds".format(time_consummed.seconds))

    # Print start
    print ("Writing prepfold into file...")
    # Timing starts
    start = datetime.datetime.now()
    # Write into file
    with open(cmd_path, "w") as f:
        f.write(content)
    # Timeing ends
    end = datetime.datetime.now()
    # Delta T
    time_consummed = end-start
    # Print time consumed
    print ("done within {} seconds".format(time_consummed.seconds))
    
    return True

#############################################
#if __name__ == "__main__":
#    main()