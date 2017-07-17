#!/usr/bin/env python
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

    out_folder = mk_folder("pngcrush_results/")
    out_folder = mk_folder("pngquant_results/")
    out_folder = mk_folder("optipng_results/")
    # out_folder = mk_folder("pngnq_results/")
    # out_folder = mk_folder("jpegoptim_results/")

    results['pngcrush'] = run_pngcrush(pngs)
    results['pngcrush_mode'] = run_pngcrush(pngs,results['pngcrush']['other']['mode_method'])

    # for val in list(range(1,12)):
    #     print("PNGQuant Speed:" + str(val))
    #     results['pngquant_speed_' + str(val)] = run_pngquant(pngs, val)

    for val in list(range(8)):
        print("OptiPNG optimization level:" + str(val))
        results['optipng_opt_' + str(val)] = run_optipng(pngs, val)

    # for val in list(range(1, 11)):
    #     print("PNGnq Speed:" + str(val))
    #     results['pngnq_speed_' + str(val)] = run_pngnq(pngs, val)
    
    # for val in list(range(0, 101)):
    #     print("JPEGOptim Quality:" + str(val))
    #     run_jpegoptim(jpegs, val)
    # write_results(results)


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
    with open('results.csv', 'w') as csvfile:
        fieldnames = ['utility', 'mean_run_time', 'best_compression_id', 'worst_compression_id','mean_compression_percentage','other_descript', 'other']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in results_dict:
            writer.writerow({'utility':key, 'mean_run_time':results_dict[key]['mean_run_time'], 'best_compression_id':results_dict[key]['best_compression_id'],\
                'worst_compression_id':results_dict[key]['worst_compression_id'],'mean_compression_percentage':results_dict[key]['mean_compression']})

            for other_key in results_dict[key]['other']:
                if results_dict[key]['other'] is not None:
                    writer.writerow({'other_descript':other_key, 'other':results_dict[key]['other'][other_key]})

def run_pngcrush(pngs, method=None):

    print("Running PNGCrush ...\n")
    
    print(method)
    if method is None:
        base = ["./pngcrush", "-reduce", "-brute"]
        out_folder = mk_folder("pngcrush_results/brute_force/")
    else:
        base = ["./pngcrush", "-reduce", "-m " + str(method)]
        out_folder = mk_folder("pngcrush_results/method_" + str(method) + "/")
    saved_output = [] # list of output that needs to be parsed to gather more data
    num_methods = 148
    best_methods = list()
    compression_percent = list()
    increase_percent = list() # list of filesize increase percentages
    mean_time = list()
    
    num_pngs = 0

    for img in pngs.iterdir():
        print(img.name)
        start = time.time()
        command = copy.deepcopy(base)
        command.append(img)
        command.append(out_folder / img.name)
        Path.touch(out_folder / img.name)

        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        # output is a bytes-like object, so decode into a string
        decoded_output = output.decode('ascii')
        # find index of relevant data i.e. best method, compression percentage, etc.
        relevant_index = decoded_output.find("Best")
        # store relevant data for later processing
        if relevant_index != -1:
            saved_output.append(decoded_output[relevant_index:])
        mean_time.append(time.time() - start)
    
    for line in saved_output:
        # best method number is after the first '=' and before the first '('
        best_method = int(line[line.find('=') + 1: line.find('(')])
        best_methods.append(best_method)

        if line.find('filesize reduction') != -1:
            percent_reduction = float(line[line.find('filesize reduction') - 7:line.find('filesize reduction')].strip('% ('))
            compression_percent.append(percent_reduction)
        else:
            # Sometimes filesizes increase for reasons unknown
            percent_increase = float(line[line.find('filesize increase') - 7:line.find('filesize increase')].strip('% ('))
            increase_percent.append(percent_increase)

    mean_time = mean(mean_time)

    if len(increase_percent) == 0:
        increase_percent.append(-1)

    if len(compression_percent) == 0:
        compression_percent.append(-1)

    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)),'other':{'mode_method':mode(best_methods), 'mean_size_increase':mean(increase_percent)}}
    return res

def run_pngquant(pngs, speed=3): #default speed for pngquant is 3
    
    print("Running PNGQuant ...\n")

    base = ["./pngquant", "--force", "--verbose"]
    compression_percent = list()
    mean_time = list()

    out_folder = mk_folder("pngquant_results/speed_" + str(speed))
    speed = "-s" + str(speed)
    for img in pngs.iterdir():
        if img.name.find('png') != -1:
            print(img.name)
            start = time.time()
            command = copy.deepcopy(base)
            command.append("--output")
            command.append(str(Path(out_folder / img.name)))
            command.append(speed)
            command.append(str(Path(img)))
            Path.touch(out_folder / img.name)

            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            mean_time.append(time.time() - start)
            original_size = os.stat(img).st_size
            compressed_size = os.stat(Path(out_folder / img.name)).st_size
            percent_comp = ((original_size  - compressed_size) / original_size) * 100
            compression_percent.append(percent_comp)

    mean_time = mean(mean_time)
    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)), 'other':None}
    return res


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
        if img.name.find('png') != -1:
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
                print("An error occurred with Optipng:")

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

def run_pngnq(pngs, speed=3):
    
    print("Running PNGnq ...\n")
    out_folder = mk_folder("pngnq_results/speed_" + str(speed))
    base = ["./pngnq", "-v", "-s" + str(speed)]
    compression_percent = list()
    mean_time = list()
    saved_output = [] # list of output that needs to be parsed to gather more data

    for img in pngs.iterdir():
        if img.name.find('png') != -1:
            print(img.name)
            start = time.time()
            command = copy.deepcopy(base)
            Path.touch(out_folder / img.name)
            command.append("-d")
            command.append(str(Path(out_folder)))
            command.append(str(Path(img)))

            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            mean_time.append(time.time() - start)
            compression_percent.append(calc_percent_difference(img, Path(out_folder / img.name)))

    mean_time = mean(mean_time)
    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)), 'other':None}

    return res

def run_jpegoptim(jpgs, quality=None):

    print("Running JPEGOptim ...\n")

    if quality is None:
        base = ["./jpegoptim", "--strip-all", "--all-progressive", "-o", "--stdout"]
        out_folder = mk_folder("jpegoptim_results/lossless_opt/")
    else:
        base = ["./jpegoptim", "--strip-all", "--all-progressive", "-o", "--stdout","-m" + str(quality)]
        out_folder = mk_folder("jpegoptim_results/max_quality_" + str(quality) + "/")

    # saved_output = [] # list of output that needs to be parsed to gather more data
    # num_methods = 148
    # best_methods = list()
    # compression_percent = list()
    # increase_percent = list() # list of filesize increase percentages
    # mean_time = list()
    
    # num_pngs = 0

    for img in jpgs.iterdir():
        print(img.name)
        if img.name.lower().find("jpg") != -1 or img.name.lower().find("jpeg"):
            start = time.time()
            command = copy.deepcopy(base)
            command.append("-d")
            Path.touch(out_folder)
            command.append(str(Path(out_folder)))
            command.append(img)

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print(err)
        # output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    #     # output is a bytes-like object, so decode into a string
        # decoded_output = output.decode('ascii')
    #     # find index of relevant data i.e. best method, compression percentage, etc.
    #     relevant_index = decoded_output.find("Best")
    #     # store relevant data for later processing
    #     if relevant_index != -1:
    #         saved_output.append(decoded_output[relevant_index:])
    #     mean_time.append(time.time() - start)
    
    # for line in saved_output:
    #     # best method number is after the first '=' and before the first '('
    #     best_method = int(line[line.find('=') + 1: line.find('(')])
    #     best_methods.append(best_method)

    #     if line.find('filesize reduction') != -1:
    #         percent_reduction = float(line[line.find('filesize reduction') - 7:line.find('filesize reduction')].strip('% ('))
    #         compression_percent.append(percent_reduction)
    #     else:
    #         # Sometimes filesizes increase for reasons unknown
    #         percent_increase = float(line[line.find('filesize increase') - 7:line.find('filesize increase')].strip('% ('))
    #         increase_percent.append(percent_increase)

    # mean_time = mean(mean_time)

    # if len(increase_percent) == 0:
    #     increase_percent.append(-1)

    # if len(compression_percent) == 0:
    #     compression_percent.append(-1)

    # res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
    #     'worst_compression_id':compression_percent.index(min(compression_percent)),'other':{'mode_method':mode(best_methods), 'mean_size_increase':mean(increase_percent)}}
    # return res

# def run_jpegtran(jpgs):

# def run_pil_jpeg(jpgs):

if __name__ == '__main__':
    main()