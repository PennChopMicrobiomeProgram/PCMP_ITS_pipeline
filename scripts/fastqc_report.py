import pandas
import re
import os
import sys
from collections import OrderedDict
from io import StringIO
from typing import TextIO

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


quality_list = [
    parse_fastqc_quality(file) for file in snakemake.input.files
]
quality_list = [qr for qr in quality_list if qr is not None]
quality_table = pandas.concat(quality_list, axis=1).transpose()
quality_table.to_csv(snakemake.output[0], sep="\t", index_label="Samples")