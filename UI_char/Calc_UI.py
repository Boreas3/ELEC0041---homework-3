from subprocess import call
import numpy as np
import csv
import pandas as pd
import matplotlib.pylab as plt
import math

if __name__ == "__main__":
    N = 10
    r_load = np.linspace(1e-3,1e3,N)
    U = np.zeros([N,1])
    I = np.zeros([N,1])

    for j in range(0,N):
        call(["gmsh", "-2", "transfo.geo",  "-v", "1"])
        call(["getdp", "transfo.pro", "-v", "1", "-solve", "Magnetodynamics2D_av", "-pos", "UI_Char", 
                                                                "-setnumber", "r_load", "{}".format(r_load[j])])
        temp_res = np.empty([6,1])     
        i = 0               
        with open('UI3_B_shell.txt', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for row in spamreader:
                temp_res[i] = row[2]
                i +=1
        U[j] = np.mean(temp_res[0:3])
        I[j] = np.mean(temp_res[4:6])

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    B = U*np.sqrt(3)/np.sqrt(2)
    A = I/np.sqrt(2)

    ax.plot(A,B, '-b')
    ax.set_xlabel('Current [A] (RMS value)')
    ax.set_ylabel('Phase-to-Phase Voltage [kV] (RMS value)')
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
        item.set_fontsize(15)
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):  
        item.set_fontsize(12) 
    plt.grid()
    plt.savefig('UI_char_B_shell.png')
                    