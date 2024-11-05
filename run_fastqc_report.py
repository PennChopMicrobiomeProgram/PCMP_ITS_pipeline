#!/usr/bin/env python
import pandas
import re
import os
import sys
from collections import OrderedDict
from io import StringIO
from typing import TextIO
# Folder Path
path = "/mnt/isilon/microbiome/analysis/danielsg/PCMP_ITS_pipeline/test/post_fastqc/reports"
# Change the directory
os.chdir(path)
# Read text File
def read_text_file(file_path):
    with open(file_path, 'r') as f:
        print(f.read())
def parse_fastqc_quality(filename: str) -> pandas.DataFrame:
    with open(filename) as f:
        report = f.read()
    try:
        tableString = re.search(
            "\>\>Per base sequence quality.*?\n(.*?)\n\>\>END_MODULE", report, re.DOTALL
        ).group(1)
        f_s = StringIO(tableString)
        df = pandas.read_csv(
            f_s, sep="\t", usecols=["#Base", "Mean"], index_col="#Base"
        )
        sample_name = os.path.basename(filename.split("_fastqc")[1])
        df.columns = [sample_name]
        f_s.close()
        return df
    except AttributeError as e:
        sys.stderr.write(f"{filename} has no per-base sequence quality reports.")
        return None
qr=[]
# iterate through all file
for subdir, dirs, files in os.walk(path):
    for file in files:
        #print(file)
        # Check whether file is in text format or not
        if file.endswith("fastqc_data.txt"):
            #file_path = f"{path}/{file}"
            file_path = os.path.join(subdir, file)
            qr.append(file_path)
            # call read text file function
            #read_text_file(file_path)
print(qr)
quality_list = [
    parse_fastqc_quality(file) for file in qr if file is not None
]
quality_list = [x for x in quality_list if x is not None]
quality_table = pandas.concat(quality_list, axis=1).transpose()
quality_table.to_csv("../fastqc_quality_report.tsv", sep="\t", index_label="Samples")
