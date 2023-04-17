import argparse
import os
import pandas as pd
import shutil
import yaml

from PIL import Image

from utils.find_project_root import find_project_root

def get_subset_of_relevant_pokemon(EXTERNAL_DATA_PATH, TARGET_POKEMON_TYPE):

    TARGET_POKEMON_TYPE = TARGET_POKEMON_TYPE.lower()

    if not TARGET_POKEMON_TYPE in ['all', 'none', '']:
        pokemon = pd.read_csv(PROJECT_ROOT / EXTERNAL_DATA_PATH / 'Pokedex_Cleaned.csv', encoding='latin-1', engine='python')
        pokemon = pokemon[["#", "Name", "Primary Type", "Secondary Type"]]

        # Make columns lowercase
        pokemon['Primary Type']= pokemon['Primary Type'].str.lower()
        pokemon['Secondary Type']= pokemon['Primary Type'].str.lower()

        subset_1 = pokemon.loc[pokemon['Primary Type'] == TARGET_POKEMON_TYPE]
        subset_2 = pokemon.loc[pokemon['Secondary Type'] == TARGET_POKEMON_TYPE]
        
        subset = pd.concat([subset_1, subset_2]).sort_values('#')
    else:
        subset = pokemon
    
    subset.head()
    return(subset)

def resize_images_in_directory(TRAIN_DATA_PATH, subset):
    # Create directory and clear if it already exists
    if not os.path.exists(PROJECT_ROOT / TRAIN_DATA_PATH):
        os.mkdir(PROJECT_ROOT / TRAIN_DATA_PATH)
    else:
        shutil.rmtree(PROJECT_ROOT / TRAIN_DATA_PATH)
        os.mkdir(PROJECT_ROOT / TRAIN_DATA_PATH)
            
    # Resize training images and save to processed directory
    for image_name in os.listdir(PROJECT_ROOT/EXTERNAL_DATA_PATH/'pokemon'):
        
        # Only keep sprites of our defined subset (e.g. water type generation 1)
        pokedex_number = int(image_name.split('.')[0])
        
        if pokedex_number in list(subset['#']):
            pokemon_sprite = Image.open(PROJECT_ROOT/ EXTERNAL_DATA_PATH / 'pokemon' / image_name)
            pokemon_sprite_resized = pokemon_sprite.resize((512, 512))

            # Add leading zeroes
            while len(image_name) < 8:
                image_name = "0" + image_name

            pokemon_sprite_resized.save(PROJECT_ROOT / TRAIN_DATA_PATH / image_name)

if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--params', dest='params', required=True)
    args = args_parser.parse_args()

    with open(args.params) as param_file:
        params = yaml.safe_load(param_file)

    PROJECT_ROOT = find_project_root()
    EXTERNAL_DATA_PATH: str = params['data_etl']['external_data_path']
    TRAIN_DATA_PATH: str = params['data_etl']['train_data_path']
    TARGET_POKEMON_TYPE: str = params['base']['train_pokemon_type']

    subset = get_subset_of_relevant_pokemon(EXTERNAL_DATA_PATH, TARGET_POKEMON_TYPE)
    resize_images_in_directory(TRAIN_DATA_PATH, subset)