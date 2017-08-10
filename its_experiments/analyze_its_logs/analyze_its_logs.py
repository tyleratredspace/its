#!/usr/bin/env python3
import csv
import re
import sys
from pathlib import Path
from collections import Counter

def main():
    logs_dir = Path(__file__).parent / "logs"
    num_logs = len(list(logs_dir.iterdir()))
    count = 0
    log_data_list = list()
    log_data = dict()
    exclude_zero_data = True # use this to exclude info about transforms that weren't
    # applied to a given image

    folder = Path(__file__).parent / "parsed_log_outputs/"
    if not folder.exists():
        Path.mkdir(folder)

    for log_folder in logs_dir.iterdir():
        if log_folder.is_dir()
            for log_file_path in log_folder.iterdir():
                if count <= num_logs:
                    print("On log # %s" % count)
                    parse_log(log_file_path, folder)
                    log_data_list.append(analyze_log(parse_log_csv(folder / log_file_path.name)))
                    count += 1
    

    for x_log_data in log_data_list:
        for img, img_transforms in x_log_data.items():
            if img in log_data:
                counters = [Counter(img_transforms), Counter(log_data[img])]
                log_data[img] = dict(sum(counters, Counter()))
            else:
                log_data[img] = img_transforms
    write_results(log_data, exclude_zero_data)

def write_results(results_dict, exclude_zero_data):

    """
    Excel Note:

    To get the averages of Column C, when the string in Column A contains "old"
    and the string in Column E doesn't contain HTTP, use :

    =AVERAGEIFS(C$2:C$3369,A$2:A$3369,"*old*",E2:E3369,"<>*HTTP*")

    """
    with open('log_data_analysis.csv', 'w') as csvfile:
        fieldnames = ['Image', 'Query', '# Requests For Query']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for img in results_dict:
            for transform in results_dict[img]:
                if exclude_zero_data and results_dict[img][transform] == 0:
                    none = 0
                    # print("%s had no data for %s so it wasn't added to csv.\n" % (img, transform))
                else:
                    writer.writerow({
                      'Image': img,
                        'Query': transform,
                        '# Requests For Query': results_dict[img][transform],
                        
                    })

def parse_log(file_path, parsed_logs_folder):
    with open(file_path) as f:
        lines = f.readlines()

    new_file_path = parsed_logs_folder / (str(file_path.name) + '_output.csv')
    Path.touch(new_file_path)
    with open(new_file_path, 'w') as ofile:
        out = csv.DictWriter(ofile, ('maybe_time', 'status', 'bytes', 'url'))
        out.writeheader()

        for line in lines:
            # re_match = re.match('^[\d\-:TZ\.]+ [\w\-]+ [\d\.:]+ [\d\.:]+ [\d\.]+ (?P<maybe_time>[\d\.]+) [\d\.]+ \d+ (?P<status>\d+) \d+ (?P<bytes>\d+) "GET (?P<url>.+?) HTTP/\d\.\d"', line)
            
            re_match = re.match('^[\d\-:TZ\.]+ [\w\-]+ [\d\.:\-]+ [\d\.:\-]+ [\d\.\-]+ (?P<maybe_time>[\d\.]+) [\d\.]+ \d+ (?P<status>\d+) \d+ (?P<bytes>\d+) "GET|HEAD (?P<url>.+?) HTTP/\d\.\d" "[\w\-\\\d]*"', line)
            try:
                group = re_match.groupdict()
                out.writerow(group)
            except AttributeError as e:
                print(e)
                print(line)

def parse_log_csv(log_path):
    log_dict = dict()

    with open(str(log_path) + '_output.csv', 'r') as log_csv:
        reader = csv.DictReader(log_csv)
        for row in reader:
            log_dict[row['url']] = {
                'maybe_time': row['maybe_time'],
                'status': row['status'],
                'bytes': row['bytes']
            }

    return log_dict

def analyze_log(log):
    data = dict()

    transforms = ["crop", "focalcrop", "fit", "resize", "passport", "none"]

    for url in log:
        file_name = re.sub('.+?(/)', '', url, flags=re.IGNORECASE)
        # file_name = re.sub('(\.).+', '', file_name, flags=re.IGNORECASE)
        transform = re.sub('(http://its-prod-app-1098184084.us-east-1.elb.amazonaws.com:80/).+?(/)', '', url, flags=re.IGNORECASE)
        transform = re.sub('.+?(/)', '', transform, flags=re.IGNORECASE)
        transform = transform.split(".")
        transform = list(set(transform).intersection(transforms))

        if len(transform) == 0:
            transform = "none"
        elif len(transform) > 1:
            transform = "&".join(transform)
            if transform not in transforms:
                transforms.append(transform)
        else:
            transform = "".join(transform)

        if file_name in data:
            if transform in data[file_name]:
                data[file_name][transform] += 1
            else:
                data[file_name][transform] = 1
        else:
            data[file_name] = dict((transform, 0) for transform in transforms)
            data[file_name][transform] = 1

    return data

if __name__ == '__main__':
    main()
