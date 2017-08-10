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

    out_folder = mk_folder("jpegoptim_results/")
    # out_folder = mk_folder("pil_jpeg_results/")

    
    for val in list(range(0, 101)):
        print("JPEGOptim Quality:" + str(val))
        results['jpegoptim_quality_' + str(val)] = run_jpegoptim(jpegs, val)

    # for val in list(range(1, 96)):
    #     print("Pillow Quality:" + str(val))
    #     results['pillow_quality' + str(val)] = run_pil_jpeg(jpegs, val)

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
    with open('jpegoptim_results.csv', 'w') as csvfile:
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

def run_jpegoptim(jpgs, quality=None):

    print("Running JPEGOptim ...\n")

    if quality is None:
        base = ["./jpegoptim", "--strip-all", "--all-progressive", "-v","-o"]
        out_folder = mk_folder("jpegoptim_results/lossless_opt/")
    else:
        base = ["./jpegoptim", "--strip-all", "--all-progressive", "-o", "-v", "-m" + str(quality)]
        out_folder = mk_folder("jpegoptim_results/max_quality_" + str(quality) + "/")

    saved_output = [] # list of output that needs to be parsed to gather more data
    compression_percent = list()
    mean_time = list()

    for img in jpgs.iterdir():
        print(img.name)
        if img.name.lower().find("jpg") != -1 or img.name.lower().find("jpeg") != -1:
            start = time.time()
            command = copy.deepcopy(base)
            command.append("-d")
            command.append(str(Path(out_folder)) + "/")
            command.append(str(Path(img)))

            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT)
                decoded_output = output.decode('ascii')
                relevant_index = decoded_output.find("bytes")
                # store relevant data for later processing
                if relevant_index != -1:
                    saved_output.append(decoded_output[relevant_index:])
                mean_time.append(time.time() - start)
            except Exception as e:
                print("JPEGOptim had an error: " + str(e))
                print(img.name + " has the following stats:" + str(os.stat(img)))
    
    for line in saved_output:
        # percent reduction
        percent_reduction = float(line[line.find('('): line.find(')')].strip("( )%"))
        compression_percent.append(percent_reduction)

    mean_time = mean(mean_time)

    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)),'other':None}
    return res

def run_pil_jpeg(jpgs, quality=None):
    print("Running JPEG compression via Pillow ...\n")

    compression_percent = list()
    mean_time = list()

    if quality is None:
        out_folder = mk_folder("pil_jpeg_results/quality_default_75" + str(quality) + "/")
    else:
        out_folder = mk_folder("pil_jpeg_results/quality_" + str(quality) + "/")

    for img in jpgs.iterdir():
        print(img.name)
        if img.name.lower().find("jpg") != -1 or img.name.lower().find("jpeg") != -1:
            start = time.time()
            try:
                image = Image.open(img)
                image.save(Path(out_folder / img.name), "JPEG", quality=quality, optimize=True, progressive=True)
                mean_time.append(time.time() - start)
                compression_percent.append(calc_percent_difference(img, Path(out_folder / img.name)))
            except Exception as e:
                print("An error occurred with Pillow:" + str(e))


    mean_time = mean(mean_time)

    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)),'other':None}
    return res


if __name__ == '__main__':
    main()