import argparse
import os
import shutil
from tqdm import tqdm
import urllib.request
import yaml

from utils.find_project_root import find_project_root

def scrape_images():
    # Create directory and clear if it already exists
    if not os.path.exists(PROJECT_ROOT / EXTERNAL_DATA_PATH / 'pokemon'):
        os.mkdir(PROJECT_ROOT / EXTERNAL_DATA_PATH / 'pokemon')
    else:
        shutil.rmtree(PROJECT_ROOT / EXTERNAL_DATA_PATH / 'pokemon')
        os.mkdir(PROJECT_ROOT / EXTERNAL_DATA_PATH / 'pokemon')

    for i in tqdm(range(1, 1009)):
        id = str(i)
        while len(id) < 3:
            id = "0" + id

        imgURL = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{id}.png"
        urllib.request.urlretrieve(imgURL, f"{PROJECT_ROOT}/{EXTERNAL_DATA_PATH}/pokemon/{id}.png")

if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--params', dest='params', required=True)
    args = args_parser.parse_args()

    with open(args.params) as param_file:
        params = yaml.safe_load(param_file)

    PROJECT_ROOT = find_project_root()
    EXTERNAL_DATA_PATH: str = params['data_etl']['external_data_path']

    scrape_images()
