#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
from math import floor
import csv
import urllib.request
import re
import time
import uuid
from its.pipeline import process_transforms

def main():

    """
        To compare AWS speeds via logs, use parse_log to create an output.csv file of the relevant
        log data before running this script.
    """

    jpegs = Path(__file__).parent / "compare-its/jpgs"
    pngs = Path(__file__).parent / "compare-its/pngs"
    results = dict()
    aws_results = dict()
    transforms = ["crop", "focalcrop", "fit", "resize", "passport"]
    mk_folder("results/")
    mk_folder("results/new_its/")
    mk_folder("results/old_its/")

    print("Local Tests")
    print("\nOld ITS\n")
    results['old_its'] = run_old_its(jpegs, pngs)

    print("\nNew ITS\n")
    results['new'] = run_new_its_local(jpegs, pngs)

    write_results_local(results)

    # print("AWS Tests")
    # mk_folder("results/new_its_aws/")
    # mk_folder("results/old_its_aws/")

    # log = parse_log_csv()
    # aws_results['old_its_aws'] = {}
    # aws_results['new_its_aws'] = {}

    # count = 0

    # for url in log:
    #     print(count)
    #     print(url)

    #     transform = re.sub('(http://its-prod-app-1098184084.us-east-1.elb.amazonaws.com:80/).+?(/)', '', url, flags=re.IGNORECASE)
    #     transform = re.sub('.+?(/)', '', transform, flags=re.IGNORECASE)
    #     transform = transform.split(".")
    #     transform = list(set(transform).intersection(transforms))

    #     if len(transform) == 0:
    #         transform = "none"
    #     elif len(transform) > 1:
    #         transform = "&".join(transform)
    #     else:
    #         transform = "".join(transform)

    #     aws_results['old_its_aws'][url] = {}
    #     aws_results['new_its_aws'][url] = {}

    #     aws_results['old_its_aws'][url] = run_old_its_aws(url)
    #     aws_results['old_its_aws'][url]['query'] = transform

    #     try:
    #         aws_results['new_its_aws'][url] = run_new_its_aws(url)
    #         aws_results['new_its_aws'][url]['query'] = transform
    #     except Exception as e:
    #         print("error occurred")
    #         aws_results['new_its_aws'][url] = {'run_time': "error", 'img_type':"error", 'result_size': 0, 'image':"error", 'error': str(e)}

    #     count += 1

    # write_results_aws(aws_results)

def mk_folder(dir_name):
    folder = Path(__file__).parent / dir_name
    if not folder.exists():
        Path.mkdir(folder)
    return folder


def parse_log_csv():

    log_dict = dict()

    with open('output.csv', 'r') as log_csv:
        reader = csv.DictReader(log_csv)
        for row in reader:
            log_dict[row['url']] = {
                'maybe_time': row['maybe_time'],
                'status': row['status'],
                'bytes': row['bytes']
            }

    return log_dict


def write_results_aws(results_dict):
    with open('its_compare_results_aws.csv', 'w') as csvfile:
        fieldnames = ['ITS Version', 'URL', 'Query', 'Image', 'Run Time', 'Result Size (bytes)', 'Error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key in results_dict:
            for url in results_dict[key]:
                # for query in results_dict[key][url]:
                    if 'error' in results_dict[key][url] and results_dict[key][url]['error'] is not None:
                        writer.writerow({
                            'ITS Version': key,
                            'URL': url,
                            'Query': results_dict[key][url]['query'],
                            'Image': results_dict[key][url]['image'],
                            'Run Time': results_dict[key][url]['run_time'],
                            'Result Size (bytes)': results_dict[key][url]['result_size'],
                            'Error': results_dict[key][url]['error']
                        })
                    else:
                        writer.writerow({
                            'ITS Version': key,
                            'URL': url,
                            'Query': results_dict[key][url]['query'],
                            'Image': results_dict[key][url]['image'],
                            'Run Time': results_dict[key][url]['run_time'],
                            'Result Size (bytes)': results_dict[key][url]['result_size']
                        })


def run_old_its_aws(request):
    results = dict()
    img_types = [".jpg", ".jpeg", ".png"]
    out_folder = mk_folder("results/old_its_aws/")
    suffix = re.sub('.+?(\.)', '', request, flags=re.IGNORECASE)

    if suffix.lower() in ["jpg", "jpeg"]:
        suffix = "jpeg"

    file_name = re.sub('.+?(/)', '', request, flags=re.IGNORECASE)
    file_name = re.sub('(\.).+', '', file_name, flags=re.IGNORECASE)
    start = time.time()
    try:
        local_filename, headers = urllib.request.urlretrieve(request)
        end = time.time() - start
        result = Image.open(local_filename)
        result_name = file_name + "_"+ str(uuid.uuid4()) + "." + suffix
        result.save(Path(out_folder / result_name) , suffix.upper())
        results = {'run_time': end , 'img_type':suffix, 'result_size':Path(out_folder / result_name).stat().st_size, 'image':file_name + "." + suffix, 'error': None}
    except urllib.error.HTTPError as e:
        end = time.time() - start
        results = {'run_time': end, 'img_type':suffix, 'result_size': 0, 'image':file_name + "." + suffix, 'error': str(e)}

    return results

def run_new_its_aws(request):
    results = dict()
    img_types = [".jpg", ".jpeg", ".png"]
    out_folder = mk_folder("results/new_its_aws/")
    suffix = re.sub('.+?(\.)', '', request, flags=re.IGNORECASE)

    if suffix.lower() in ["jpg", "jpeg"]:
        suffix = "jpeg"

    file_name = re.sub('.+?(/)', '', request, flags=re.IGNORECASE)
    file_name = re.sub('(\.).+', '', file_name, flags=re.IGNORECASE)
    namespace = re.sub('(http://its-prod-app-1098184084.us-east-1.elb.amazonaws.com:80/)', '', request, flags=re.IGNORECASE)
    api_call = "https://4vv4hx7r3b.execute-api.us-east-1.amazonaws.com/dev/default/" + namespace
    start = time.time()
    try:
        local_filename, headers = urllib.request.urlretrieve(api_call)
        end = time.time() - start
        result = Image.open(local_filename)
        result_name = file_name + "_"+ str(uuid.uuid4()) + "." + suffix
        if result.mode == "RGBA" and suffix == "jpeg":
            result = result.convert("RGB")
        result.save(Path(out_folder / result_name) , suffix.upper())
        results = {'run_time': end , 'img_type':suffix, 'result_size':Path(out_folder / result_name).stat().st_size, 'image':file_name + "." + suffix, 'error': None}
    except urllib.error.HTTPError as e:
        end = time.time() - start
        results = {'run_time': end, 'img_type':suffix, 'result_size': 0, 'image':file_name + "." + suffix, 'error': str(e)}

    return results

def write_results_local(results_dict):
    with open('its_compare_results.csv', 'w') as csvfile:
        fieldnames = ['ITS Version', 'Query Name', 'Query',  'Image Name', 'Original Size (bytes)', 'Result Name', 'Result Size (bytes)', 'Error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in results_dict:
            writer.writerow({'ITS Version':key})

            for img_name in results_dict[key]:
                writer.writerow({'Image Name': img_name})
                for query_key in results_dict[key][img_name]:
                    if 'error' in results_dict[key][img_name][query_key]['file_info'] and results_dict[key][img_name][query_key]['file_info']['error'] is not None:
                        writer.writerow(
                            {'Query Name': query_key, 'Query': results_dict[key][img_name][query_key]['query'], \
                                'Original Size (bytes)': results_dict[key][img_name][query_key]['file_info']['original_size'], \
                                'Result Name': results_dict[key][img_name][query_key]['file_info']['result_filename'], 'Result Size (bytes)': results_dict[key][img_name][query_key]['file_info']['result_size'],\
                                'Error': results_dict[key][img_name][query_key]['file_info']['error']})
                    else:
                        writer.writerow(
                            {'Query Name': query_key, 'Query': results_dict[key][img_name][query_key]['query'], \
                                'Original Size (bytes)': results_dict[key][img_name][query_key]['file_info']['original_size'], \
                                'Result Name': results_dict[key][img_name][query_key]['file_info']['result_filename'], 'Result Size (bytes)': results_dict[key][img_name][query_key]['file_info']['result_size']})


def setup_requests(img_path):

    img_urls = {
        'bacteria.jpg': 'http://image.pbs.org/video-assets/ABsMthj-asset-mezzanine-16x9-iYxk9Oa.jpg',
        'bear.jpg': 'http://image.pbs.org/curate/1dd98268-82b4-4847-bd59-ab778e85ce3c.jpg',
        'bird.jpg': 'http://image.pbs.org/curate/5e2b5d25-588d-4ca2-a764-0d58d4f524b5.jpg',
        'couple.jpg': 'http://image.pbs.org/curate/89d157ea-f95f-43f0-a44a-a792a226200d.jpg',
        'GoT.jpg': 'http://image.pbs.org/video-assets/pbs/shanks-fx/241951/images/mezzanine_403.jpg',
        'ireland.jpg': 'http://image.pbs.org/curate/97a68cdd-cfef-4154-a5d3-b27fcee4fa7b.jpg',
        'moai.jpg': 'http://image.pbs.org/video-assets/pbs/nova/50369/images/Mezzanine_304.jpg',
        'pov_assets.jpg': 'http://image.pbs.org/video-assets/SsxgvVx-asset-mezzanine-16x9-ltWsSMF.jpg',
        'rewire.jpg': 'http://image.pbs.org/contentchannels/3603/0kWRZUo9qvjzM6nM91Ww.jpg',
        'spaceman.jpg': 'http://image.pbs.org/contentchannels/3603/0kWRZUo9qvjzM6nM91Ww.jpg',
        'ar-logo.png': 'http://image.pbs.org/contentchannels/6/cvNsH2NSZMAJvXqDfngA.png',
        'nova-logo.png': 'http://image.pbs.org/contentchannels/42/zEyRHtMrn4lWUSVrIsDqJg.png',
        'pbs-digital-studios-logo.png': 'http://image.pbs.org/curate-dev/ae9c826f-a1eb-446e-b29b-79a559a2976f.png',
        'pbs-food-logo.png': 'http://image.pbs.org/curate-dev/136fad7c-15ef-4a58-8b87-ba09775ee0dd.png',
        'pbs-kids-logo.png': 'http://image.pbs.org/curate/e496ee93-c3f2-4b86-90d3-064c595f816e.png',
        'rewire-logo.png': 'http://image.pbs.org/curate/cdd33fb8-ea80-45f6-81b2-fbd848129c99.png',
        'tgbbs-logo.png': 'http://image.pbs.org/contentchannels/2969/4nHr9Y12DYv5R3DqlzIh8A.png',
        'the-tunnel-logo.png': 'http://image.pbs.org/contentchannels/3547/9ZenmFoWw2usoystpisnw.png',
        'weta-logo.png': 'http://image.pbs.org/stations/weta-color-logo-iZbJH8k.png',
        'wosu-logo.png': 'http://image.pbs.org/stations/wosu-color-logo-c3tdR8s.png'
    }

    local_filename, headers = urllib.request.urlretrieve(img_urls[img_path.name])
    img = Image.open(local_filename)

    overlay = Path(__file__).parent / "compare-its/overlays/overlay.png"

    if img_path.suffix in [".jpg", ".jpeg"]:
        requests = {
            'no_transforms': img_urls[img_path.name],
            'crop_smaller': img_urls[img_path.name] + ".crop." + str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2))) + ".jpg",
            'crop_larger': img_urls[img_path.name] + ".crop." + str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5))) + ".jpg",
            'focal_smaller': img_urls[img_path.name] + ".focalcrop." + str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2))) + ".0.0" + ".jpg",
            'focal_larger': img_urls[img_path.name] + ".focalcrop." + str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5))) + ".0.0" + ".jpg",
            'overlay': img_urls[img_path.name] + ".passport.jpg",
            'resize_smaller': img_urls[img_path.name] + ".resize." + str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2))) + ".jpg",
            'resize_larger': img_urls[img_path.name] + ".resize." + str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5))) + ".jpg",
            'format': img_urls[img_path.name] + ".png",
        }
    else:
        requests = {
            'no_transforms': img_urls[img_path.name],
            'crop_smaller': img_urls[img_path.name] + ".crop." + str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2))) + ".png",
            'crop_larger': img_urls[img_path.name] + ".crop." + str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5))) + ".png",
            'focal_smaller': img_urls[img_path.name] + ".focalcrop." + str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2))) + ".0.0" + ".png",
            'focal_larger': img_urls[img_path.name] + ".focalcrop." + str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5))) + ".0.0" + ".png",
            'overlay': img_urls[img_path.name] + ".passport.jpg",
            'resize_smaller': img_urls[img_path.name] + ".resize." + str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2))) + ".png",
            'resize_larger': img_urls[img_path.name] + ".resize." + str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5))) + ".png",
            'format': img_urls[img_path.name] + ".jpg"
        }

    return requests


def run_old_its(jpegs, pngs):

    results = dict()
    jpeg_out_folder = mk_folder("results/old_its/jpegs/")
    png_out_folder = mk_folder("results/old_its/pngs/")
    overlay = Path(__file__).parent / "compare-its/overlays/overlay.png"
    img_types = [".jpg", ".jpeg", ".png"]

    for img_path in jpegs.iterdir():
        print("\n" + img_path.name + "\n")
        if img_path.suffix in img_types:
            requests = setup_requests(img_path)
            results[img_path.name] = {}
            for key, request in requests.items():
                print(key)
                results[img_path.name][key] = {}
                try:
                    local_filename, headers = urllib.request.urlretrieve(request)
                    result = Image.open(local_filename)
                    result_name = img_path.stem + "_" + key + img_path.suffix
                    result.save(Path(jpeg_out_folder / result_name) , "JPEG")
                    results[img_path.name][key]['query'] = request
                    results[img_path.name][key]["file_info"] = {'original_size':img_path.stat().st_size, 'result_filename':result_name, 'result_size': Path(jpeg_out_folder / result_name).stat().st_size, 'error': None}
                except urllib.error.HTTPError as e:
                # except Exception as e:
                    results[img_path.name][key]['query'] = request
                    results[img_path.name][key]["file_info"] = {'original_size':img_path.stat().st_size, 'result_filename':"No Result Returned", 'result_size':0, 'error': str(e)}
    
    for img_path in pngs.iterdir():
        print("\n" + img_path.name + "\n")
        if img_path.suffix in img_types:
            requests = setup_requests(img_path)
            results[img_path.name] = {}
            for key, request in requests.items():
                print(key)
                results[img_path.name][key] = {}
                try:
                    local_filename, headers = urllib.request.urlretrieve(request)
                    result = Image.open(local_filename)
                    result_name = img_path.stem + "_" + key + img_path.suffix
                    result.save(Path(png_out_folder / result_name) , "PNG")
                    results[img_path.name][key]['query'] = request
                    results[img_path.name][key]["file_info"] = {'original_size':img_path.stat().st_size, 'result_filename':result_name, 'result_size': Path(png_out_folder / result_name).stat().st_size, 'error': None}
                except urllib.error.HTTPError as e:
                # except Exception as e:
                    results[img_path.name][key]['query'] = request
                    results[img_path.name][key]["file_info"] = {'original_size':img_path.stat().st_size, 'result_filename':"No Result Returned", 'result_size':0, 'error': str(e)}


    return results


def setup_queries(img_path):

    img = Image.open(img_path)
    overlay = Path(__file__).parent / "compare-itss/compare-its/overlays/overlay.png"
    queries = {}
    queries['no_transforms'] = {}
    queries['crop_smaller'] = {}
    queries['crop_larger'] = {}
    queries['focal_smaller'] = {}
    queries['focal_larger'] = {}
    queries['overlay'] = {}
    queries['resize_smaller'] = {}
    queries['resize_larger'] = {}
    queries['format'] = {}

    # set up queries
    queries['crop_smaller']['crop'] = str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2)))
    queries['crop_larger']['crop'] = str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5)))
    queries['focal_smaller']['crop'] = str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2))) + "x1x1"
    queries['focal_larger']['crop'] = str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5))) + "x1x1"
    queries['overlay']['overlay'] = str(overlay)
    # queries['overlay_in']['overlay'] = overlay + "x0x0"  # overlay completely encapsulated in image
    # queries['overlay_semi']['overlay'] = overlay + "x95x95"  # overlay partially encapsulated in image
    # queries['overlay_out']['overlay'] = overlay + "x100x100"  # overlay outside of image
    queries['resize_smaller']['resize'] = str(int(floor(img.width / 2))) + "x" + str(int(floor(img.height / 2)))
    queries['resize_larger']['resize'] = str(int(floor(img.width * 1.5))) + "x" + str(int(floor(img.height * 1.5)))


    # # combo transforms
    # queries['combo_1']['resize'] = str(floor(img.width * 1.5)) + "x" + str(floor(img.height * 1.5))
    # queries['combo_1']['crop'] = str(img.width / 2) + "x" + str(img.height / 2)

    # queries['combo_2']['resize'] = str(floor(img.width * 1.5)) + "x" + str(floor(img.height * 1.5))
    # queries['combo_2']['overlay'] = overlay + "x0x0"

    # queries['combo_3']['crop'] = str(img.width / 2) + "x" + str(img.height / 2)
    # queries['combo_3']['overlay'] = overlay

    # queries['combo_4']['resize'] = str(floor(img.width * 1.5)) + "x" + str(floor(img.height * 1.5))
    # queries['combo_4']['overlay'] = overlay + "x75x80"
    # queries['combo_4']['crop'] = str(img.width / 2) + "x" + str(img.height / 2)


    if img_path.suffix in ["jpg", "jpeg"]:
        queries['format']['format'] = 'png'
        # queries['combo_4']['format'] = 'png'
    else:
        queries['format']['format'] = 'jpg'
        # queries['combo_4']['format'] = 'jpeg'

    return queries


def run_new_its_local(jpegs, pngs):

    results = dict()
    jpeg_out_folder = mk_folder("results/new_its/jpegs/")
    png_out_folder = mk_folder("results/new_its/pngs/")
    img_types = [".jpg", ".jpeg", ".png"]

    for img_path in jpegs.iterdir():
        print("\n" + img_path.name + "\n")

        if img_path.suffix in img_types:
            queries = setup_queries(img_path)
            results[img_path.name] = {}
            img = Image.open(img_path)
            img.info['filename'] = img_path.name
            for key, query in queries.items():
                print(key)
                results[img_path.name][key] = {}
                # try:
                result = process_transforms(img, query)
                result_name = img_path.stem + "_" + key + img_path.suffix
                result.save(Path(jpeg_out_folder / result_name) , "JPEG")
                results[img_path.name][key]['query'] = query
                results[img_path.name][key]["file_info"] = {'original_size':img_path.stat().st_size, 'result_filename':result_name, 'result_size': Path(jpeg_out_folder / result_name).stat().st_size, 'error': None}
                # except Exception as e:
                #     print(e)
                #     results[img_path.name][key]['query'] = query
                #     results[img_path.name][key]["file_info"] = {'original_size':img_path.stat().st_size, 'result_filename':"No Result Returned", 'result_size':0, 'error': str(e)}

    for img_path in pngs.iterdir():
        print("\n" + img_path.name + "\n")

        if img_path.suffix in img_types:
            queries = setup_queries(img_path)
            results[img_path.name] = {}
            img = Image.open(img_path)
            img.info['filename'] = img_path.name
            for key, query in queries.items():
                print(key)
                results[img_path.name][key] = {}
                # try:
                result = process_transforms(img, query)
                result_name = img_path.stem + "_" + key + img_path.suffix
                result.save(Path(png_out_folder / result_name) , "PNG")
                results[img_path.name][key]['query'] = query
                results[img_path.name][key]["file_info"] = { 'original_size':img_path.stat().st_size, 'result_filename':result_name, 'result_size': Path(png_out_folder / result_name).stat().st_size, 'error': None}
                # except Exception as e:
                #     print(e)
                #     results[img_path.name][key]['query'] = query
                #     results[img_path.name][key]["file_info"] = {'original_size':img_path.stat().st_size, 'result_filename':"No Result Returned", 'result_size':0, 'error': str(e)}


    return results

if __name__ == '__main__':
    main()