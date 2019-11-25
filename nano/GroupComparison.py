#!/usr/bin/env python
#Author: Behzad Moumbeini
# this script has these 3 outputs:
# 1- normalized data
# 2- group comparison plot
# 3- heatmap
# usage: group_comparison.py [-h] -G GENE
# to merge all RCC files and make csv file:
'''
put all the .RCC files in the same directory

'''
#to print the file names in the path in a list:
import seaborn as sns
import os
# path = '/home/behzad/Desktop/nanostring/final/QC'
def files(path):
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith( ('.RCC') ):
            filenames.append(filename)
            filenames.sort()
    return filenames

#to merge the RCC files into a csv file:

# call the above function like this:  filenames = files(path)

import pandas as pd
from functools import reduce
from itertools import chain

def convert(filenames):
    dataframes = []
    # load all the dataframes in a list (dataframes)
    for filename in filenames:
        with open(filename.upload_file.path) as f:
            total = f.readlines()
        skip_value = total.index('CodeClass,Name,Accession,Count\n')
        df = pd.read_csv(filename.upload_file.path, skiprows=skip_value, skipfooter=5, sep=',')
        df = df.rename(columns={'Count': filename.upload_file.path})
        dataframes.append(df)
    # merge the dataframes
    df_merged = reduce(lambda x,y: pd.merge(x,y, on=['CodeClass', 'Name', 'Accession'], how='outer'), dataframes)
    df_merged.to_csv('nano/result15.csv')

#Normalization:

import subprocess

def normalization(script):
    subprocess.call(["/usr/bin/Rscript", "--vanilla", script])


#----------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def group_comparison(file1, file2, gene_name):
    print(file1)
    df1 = pd.read_csv(file1, sep = '\t')
    print(df1)
    df2 = pd.read_csv(file2, sep = '\t')
    print(df2)
    df4 = df2.drop(['CodeClass', 'Accession'], axis=1)
    print(df4)
    df5 = df4.set_index('Name').stack().reset_index().join(df1.set_index('sample'),on='level_1').rename(columns={'level_1': 'sample', 0: 'Value'})
    df5["expression log2"] = np.log(df5["Value"])
    print(df5, "df5")
    df6 = df5.loc[df5['Name'] == gene_name]
    sns.set(rc={"axes.facecolor":"#e6e6e6",
            "axes.grid":False,
            'axes.labelsize':30,
            'figure.figsize':(20.0, 10.0),
            'xtick.labelsize':25,
            'ytick.labelsize':20})
    p = sns.violinplot(data=df6,
                   x = 'group',
                   y = 'expression log2',
                   notch=True).set_title(gene_name)
    plt.xticks(rotation=45)
    l = plt.xlabel('')
    plt.ylabel('expression log2')
    plt.savefig(f'nano/{gene_name}.pdf')


import os
import pandas as pd
from bkheatmap import bkheatmap


def heatmap(normalzed_data_file):
    infile = normalzed_data_file
    prefix = os.path.splitext(infile)[0]
    df = pd.read_table(infile, index_col=0)
    df2 = np.log2(np.array(df.iloc[:, 3:]))
    df.iloc[:, 3:] = df2
    final = df
    final2 = final.iloc[:, 3:]
    bkheatmap(final2, prefix=prefix, scale="column")

def main(gene, metadata):
    group_comparison(metadata, "nano/data4.txt", gene) 

def start(qc, gene):
    files = [f for f in qc.input_file.files.all() if 'metadata' not in f.upload_file.path]
    metadata = [f for f in qc.input_file.files.all() if 'metadata' in f.upload_file.path][0]
    convert(files)
    normalization("nano/aval.r")

    comparison = main(gene, metadata.upload_file.path)
    heatmap("nano/data4.txt")
    return [f'nano/{gene}.pdf', 'nano/data4.txt', 'nano/data4.bkheatmap.html']

