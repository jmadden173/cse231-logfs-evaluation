#!/usr/bin/env python

import matplotlib.pyplot as plt

ext4 = {
    "name": "ext4",
    "write_speed": 1.0,
    "create_time": 0.565,
    "close_time": 0.030,
    "size": 28038616,
}

nilfs2 = {
    "name": "nilfs2",
    "write_speed": 1.1,
    "create_time": 0.424,
    "close_time": 0.016,
    "size": 28680192,
}

vfat = {
    "name": "vfat",
    "write_speed": 0.1,
    "create_time": 8.531,
    "close_time": 0.031,
    "size": 30201408,
}

fs_stats = [ext4, vfat, nilfs2]
colors = ["b", "g", "r"]

def stat_arr(key : str):
    """Convert list of dictionaries to arrays of keys"""
   
    arr = []
    
    for s in fs_stats:
        arr.append(s[key])
        
    return arr

def plot_bar(key : str, ylabel : str, path : str):
    """Plots a bar graph based on provided key"""
    
    plt.figure()
    data = stat_arr(key)
    names = stat_arr("name")
    for i in range(len(data)):
        plt.text(i, data[i], str(data[i]), ha='center', va='bottom')
    plt.bar(names, data, align="center", color=colors, alpha=0.8) 
    plt.ylabel(ylabel)
    plt.savefig(path)
    plt.show(block=False)
    

if __name__ == "__main__":
    if len(colors) != len(fs_stats):
        raise UserWarning("Length of colors does not match length of stats!")
   
    # apply offset 
    for s in fs_stats:
        s["size"] = s["size"] / 1e6
 
    # plot
    plot_bar("write_speed", "Write speed (MB/s)", "seqwrite.png")
    plot_bar("create_time", "File create time (ms)", "seqcreate.png")
    plot_bar("close_time", "File close time (ms)", "seqclose.png")
    plot_bar("size", "Max Capacity (GB)", "size.png") 
    
    
    input()