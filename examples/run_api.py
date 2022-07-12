import argparse
import requests
import pickle
import glob
import os

from doc_ock.mp_lock import mp_lock


class Requester:
    def __init__(self, url):
        self.url = url

    def process(self, data):
        with open(data, 'rb') as fid:
            res = requests.post(self.url, files={'image': fid})
        return res.json()

    def save_callback(self, output_filepath, data_results, data_names):
        with open(f'{output_filepath}.pickle', 'ba+') as fid:
            pickle.dump({
                'data_name': data_names,
                'results': data_results
            }, fid)


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


if __name__ == '__main__':
    args = get_args()
    requester = Requester(args.url)

    images = glob.glob(f'{args.input_images}/**/*', recursive=True)
    images = [x for x in images if os.path.isfile(x)]
    mp_lock(images, requester.process, requester.save_callback, args.num_procs, args.out_path, 1)
