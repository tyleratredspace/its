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

    out_folder = mk_folder("pngquant_results/")

    for val in list(range(1,12)):
        print("PNGQuant Speed:" + str(val))
        results['pngquant_speed_' + str(val)] = run_pngquant(pngs, val)

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
    with open('pngquant_results.csv', 'w') as csvfile:
        fieldnames = ['utility', 'mean_run_time', 'best_compression_id', 'worst_compression_id','mean_compression_percentage','other_descript', 'other']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in results_dict:
            writer.writerow({'utility':key, 'mean_run_time':results_dict[key]['mean_run_time'], 'best_compression_id':results_dict[key]['best_compression_id'],\
                'worst_compression_id':results_dict[key]['worst_compression_id'],'mean_compression_percentage':results_dict[key]['mean_compression']})

            for other_key in results_dict[key]['other']:
                if results_dict[key]['other'] is not None:
                    writer.writerow({'other_descript':other_key, 'other':results_dict[key]['other'][other_key]})

def run_pngquant(pngs, speed=3): #default speed for pngquant is 3
    
    print("Running PNGQuant ...\n")

    base = ["./pngquant", "--force", "--verbose"]
    compression_percent = list()
    mean_time = list()

    out_folder = mk_folder("pngquant_results/speed_" + str(speed))
    speed = "-s" + str(speed)
    for img in pngs.iterdir():
        if img.name.lower().find('png') != -1:
            print(img.name)
            start = time.time()
            command = copy.deepcopy(base)
            command.append("--output")
            command.append(str(Path(out_folder / img.name)))
            command.append(speed)
            command.append(str(Path(img)))

            try:
                Path.touch(out_folder / img.name)
                output = subprocess.check_output(command, stderr=subprocess.STDOUT)
                mean_time.append(time.time() - start)
                original_size = os.stat(img).st_size
                compressed_size = os.stat(Path(out_folder / img.name)).st_size
                percent_comp = ((original_size  - compressed_size) / original_size) * 100
                compression_percent.append(percent_comp)
            except Exception as e:
                print("An error occurred with PNGQuant:" + str(e))


    mean_time = mean(mean_time)
    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)), 'other':None}
    return res

if __name__ == '__main__':
    main()