#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
from statistics import mode, mean
import subprocess
import copy
import csv
import time
import os

"""
Test various compression tools on a directory of images.
"""

def main():
    jpegs = Path(__file__).parent / "images/test_jpgs"
    pngs = Path(__file__).parent / "images/test_pngs"
    results = dict()

    out_folder = mk_folder("optipng_results/")

    for val in list(range(8)):
        print("OptiPNG optimization level:" + str(val))
        results['optipng_opt_' + str(val)] = run_optipng(pngs, val)

    write_results(results)


def calc_percent_difference(original, compressed):
    original_size = os.stat(original).st_size
    compressed_size = os.stat(compressed).st_size
    percent_comp = ((original_size  - compressed_size) / original_size) * 100
    return percent_comp

def mk_folder(dir_name):
    folder = Path(__file__).parent / dir_name
    if not folder.exists():
        Path.mkdir(folder)
    return folder

def write_results(results_dict):
    with open('optipng_results.csv', 'w') as csvfile:
        fieldnames = ['utility', 'mean_run_time', 'best_compression_id', 'worst_compression_id','mean_compression_percentage','other_descript', 'other']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in results_dict:
            writer.writerow({'utility':key, 'mean_run_time':results_dict[key]['mean_run_time'], 'best_compression_id':results_dict[key]['best_compression_id'],\
                'worst_compression_id':results_dict[key]['worst_compression_id'],'mean_compression_percentage':results_dict[key]['mean_compression']})

            if results_dict[key]['other'] is not None:
                for other_key in results_dict[key]['other']:
                    if results_dict[key]['other'][other_key] is not None:
                        writer.writerow({'other_descript':other_key, 'other':results_dict[key]['other'][other_key]})


def run_optipng(pngs, opt_level):
    
    print("Running OptiPNG ...\n")

    out_folder = mk_folder("optipng_results/opt_level_" + str(opt_level))
    base = ["./optipng","-clobber", "-v", "-o" + str(opt_level)]
    compression_percent = list()
    percent_unchanged = 0
    mean_time = list()
    saved_output = [] # list of output that needs to be parsed to gather more data
    imgs = list(pngs.iterdir())

    for img in imgs:
        if img.name.lower().find('png') != -1:
            print(img.name)
            start = time.time()
            command = copy.deepcopy(base)
            command.append("-out")
            command.append(str(Path(out_folder / img.name)))
            command.append(str(Path(img)))

            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT)
                # output is a bytes-like object, so decode into a string
                decoded_output = output.decode('ascii')
                # find index of relevant data i.e. best method, compression percentage, etc.
                relevant_index = decoded_output.find("Output file size")
                # store relevant data for later processing
                if relevant_index != -1:
                    saved_output.append(decoded_output[relevant_index:])
                mean_time.append(time.time() - start)
            except Exception as e:
                print("An error occurred with Optipng:" + str(e))

    for line in saved_output:
        if line.find('decrease') != -1:
            percent_reduction = float(line[line.find('=', line.find('(')):line.find('%')].strip("% ="))
            compression_percent.append(percent_reduction)
        else:
            percent_unchanged += 1

    mean_time = mean(mean_time)
    percent_unchanged = (percent_unchanged / len(imgs)) * 100
    if len(compression_percent) == 0:
        compression_percent.append(-1)

    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent), 'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)), 'other':{'percent_unchanged': percent_unchanged}}

    return res


if __name__ == '__main__':
    main()