import argparse
import requests
import pickle
import glob
import os

from doc_ock.mp_lock import mp_lock

URL = ''

def get_args():
    parser = argparse.ArgumentParser(description='Call API')
    parser.add_argument('--num_procs', type=int, required=True,
            help='Number of processes')
    parser.add_argument('--input_images', type=str, required=True,
            help='Path to the input images')
    parser.add_argument('--url', type=str, required=True,
            help='API request URL')
    parser.add_argument('--out_path', type=str, required=True,
            help='Output path')
    return parser.parse_args()


def process(data, shared_data={}, init_values={}):
    global URL
    with open(data, 'rb') as fid:
        multipart_form_data = (
            ('image', ('file.jpg', fid)),
        )
        res = requests.post(URL, files={'image': fid})
    return res.json()

def save_callback(output_filepath, data_results, data_names):
    with open(output_filepath+'.pickle', 'ba+') as fid:
        pickle.dump({'data_name': data_names, 'results': data_results}, fid)


if __name__ == '__main__':
    args = get_args()
    URL = args.url

    images = glob.glob(f'{args.input_images}/**/*', recursive=True)
    images = [x for x in images if os.path.isfile(x)]
    mp_lock(images, process, save_callback, args.num_procs, args.out_path, 1)

