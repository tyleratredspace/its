#!/usr/bin/env python
from pathlib import Path
import subprocess
import copy
import csv
import time

"""
Test various compression tools on a directory of images.
"""

def main():
	jpegs = Path(__file__).parent / "images/test_jpgs"
	pngs = Path(__file__).parent / "images/test_pngs"
	results = dict()

	run_pngcrush(pngs, results)

def mk_out_folder(dir_name):
	out_folder = Path(__file__).parent / dir_name
	if not out_folder.exists():
		Path.mkdir(out_folder)

	return out_folder

# def write_results():

def run_pngcrush(pngs, results):

	print("Running PNGCrush ...\n")
	out_folder = mk_out_folder("pngcrush_results")
	base = ["./pngcrush", "-reduce", "-brute"]
	best_methods = dict()
	compression_percent = list()
	start = time.time()
	num_pngs = 0
	mean_time = 0

	for img in pngs.iterdir():
		
		command = copy.deepcopy(base)
		command.append(img)
		command.append(out_folder / img.name)
		Path.touch(out_folder / img.name)
		# process = subprocess.Popen(command, stdout=subprocess.PIPE)
		# for line in process.stdout:
		# 	if "Best pngcrush method" in line:
		# 		print(line)
		data = subprocess.check_output(command)
		print(data.decode('ascii')[:-5])
		num_pngs += 1
	
	mean_time = (time.time() - start) / num_pngs

	results['pngcrush'] = {'mean_time':mean_time, }


if __name__ == '__main__':
	main()