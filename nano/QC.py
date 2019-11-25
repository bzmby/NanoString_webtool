#!/usr/bin/env python
#Author: Behzad Moumbeini
# this script has these  outputs:
# 1- vsc file with 2 QC criteria 
# 2- plots with 2 lines
# usage: python3 QC.py
# to merge all RCC files and make csv file:
'''
put all the .RCC files in the same directory

'''


import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from numpy import array
import numpy
import csv
import os
import time

import os
def files(path):
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith( ('.RCC') ):
            filenames.append(filename)
            filenames.sort()
    return filenames


#------------------works---------------------

def QC(f):
    for line in f:
        line = str(line)
        segments = line.split(",")
        if segments[0] == "b'FovCount":
            FC = segments[1].replace("\\r\\n'", "")
        elif segments[0] == "b'FovCounted":
            FCed = segments[1].replace("\\r\\n'", "")
            criteria = int(FC)/int(FCed)
        elif segments[0] == "b'BindingDensity":
            BD = segments[1].replace("\\r\\n'", "")
    return [criteria, BD]


#---------------works------------


def QC2(fl):
    Di = {}
    Pos = []
    Neg = []
    for line in fl:
        line = str(line)
        seg = line.split(",")
        if seg[0] == "b'Positive":
            value = seg[3].replace("\\r\\n'", "")
            Pos.append(value)
        elif seg[0] == "b'Negative":
            value = seg[3].replace("\\r\\n'", "")
            Neg.append(value)
        Di["Positive"] = Pos
        Di["Negative"] = Neg
    return Di


def pre_plot(fi):
    num = dict()
    Pos = []
    for row in fi:
        row = str(row)
        a = ' '.join(str(row).splitlines()).split(',')
        if str(a[0]) == "b'Positive":
            num[str(a[1][4])] = int(a[3].replace("\\r\\n'", ""))
    return num



def QC_seg(file):
    main = {}
    for i in file:
        main[i] = QC(i)
    return main

#------------works-----------------------------

def QC_plot(file):
    main2 = {}
    for i in file:
        main2[i] = QC2(i)
    return main2



def plot(file_list):
    nums = []
    Dis = []
    for f in file_list:
        nums.append(pre_plot(f.upload_file))
        Dis.append(QC2(f.upload_file))

    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.set_palette('Set1')
    # concentration = np.log2(np.array([0.125, 0.5, 2, 8, 32, 128]))
    concentration = np.log2(np.array([128, 32, 8, 2, 0.5, 0.125]))
    Pos = [ [i[e] for e in sorted(i.keys())] for i in nums ]
    Pos_log = numpy.log2(numpy.array(Pos))
    Neg = [np.mean(np.log2(np.array(i['Negative'],np.float64)))+2*np.std(np.log2(np.array(i['Negative'],np.float64))) for i in Dis] 
    fig = plt.figure()
    files = []
    for i in range(len(Neg)):
        plt.plot(concentration, Pos_log[i], label='_'.join(str(file_list[i].upload_file).split('/')[-1].split('.')[0].split('_')[:-1:]))
        plt.axhline(y=Neg[i], color='b', linestyle='-')
        plt.legend()
        plt.xlabel("log2 concentration")
        plt.ylabel("log2 raw counts")
        plt.ylim(0, 40)
        fig = plt.gcf()
        file_name_generator = f"{str(int(time.time()))+str(file_list[i].upload_file).split('/')[-1].split('.')[0]}.pdf"
        fig.savefig(file_name_generator)
        files.append(file_name_generator)
        plt.close('all')
    return files
#?????????????????????????????
#try the last line if it solved the problem or not


def Quality_measures(file_list):
    qc = []
    file_names = []
    for fi in file_list:
        file_names.append(str(fi.upload_file))
        qc.append(QC(fi.upload_file))
    new_dict = dict(zip(file_names, qc))
    return new_dict


def start(qc):
    #take the path
    #path = os.path.join(os.getcwd())

    #returns a list containing the RCC file names in the path.
    file_list = [f for f in qc.input_file.files.all() if 'metadata' not in f.upload_file.path]

    #returns the 12 figures for the quality control with 2 lines in the same plot
    pdf_files = plot(file_list)

    #this part retuns a dictionary for the quality measures
    QC_measure = Quality_measures(file_list)
    #    print(QC_measure)
    # d = Quality_measures(path)
    #this part exports the quality measures from the dictionary to a csv file
    file_name_csv = str(int(time.time())) + 'quality_control.csv'
    with open(file_name_csv, 'w') as f:
        header = ["file_name", "citeria1", "criteria2"]
        w = csv.writer(f)
        w.writerow(header)
        for key, lst in QC_measure.items():
            w.writerow([key] + lst)
    return pdf_files, file_name_csv
