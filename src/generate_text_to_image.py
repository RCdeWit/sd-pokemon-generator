import argparse
import matplotlib.pyplot as plt
import os
import shutil
import torch
import yaml

from diffusers import DDIMScheduler, DiffusionPipeline, StableDiffusionPipeline, DPMSolverMultistepScheduler

from utils.find_project_root import find_project_root

def set_up_pipeline(BASE_MODEL, LORA_PATH, USE_LORA=True):
    pipe = DiffusionPipeline.from_pretrained(BASE_MODEL)
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

    # These settings work for Apple M1/M2 silicon
    # Docs for configuring to your hardware: https://huggingface.co/docs/diffusers/optimization/fp16
    pipe.to("mps")

    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()

    if USE_LORA:
        # Load LoRA on top of base model weights
        pipe.unet.load_attn_procs(PROJECT_ROOT/LORA_PATH)

    return(pipe)

def generate_images(pipe, SEED, PROMPT, NEGATIVE_PROMPT, BATCH_SIZE, NUM_INFERENCE_STEPS):
    generator = torch.Generator().manual_seed(SEED)

    outputs = pipe(prompt=[PROMPT] * BATCH_SIZE
                , negative_prompt=[NEGATIVE_PROMPT] * BATCH_SIZE
                , generator=generator
                , num_inference_steps=NUM_INFERENCE_STEPS)
    
    return outputs

def save_images(outputs, OUTPUT_DIRECTORY, batch_iteration):
    # Create directory and clear if it already exists
    if not os.path.exists(PROJECT_ROOT / OUTPUT_DIRECTORY):
        os.mkdir(PROJECT_ROOT / OUTPUT_DIRECTORY)
    else:
        shutil.rmtree(PROJECT_ROOT / OUTPUT_DIRECTORY)
        os.mkdir(PROJECT_ROOT / OUTPUT_DIRECTORY)

    for i, image in enumerate(outputs.images):      
        image.save(f'{PROJECT_ROOT / OUTPUT_DIRECTORY}/batch_iteration-{i}.png')


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--params', dest='params', required=True)
    args = args_parser.parse_args()

    with open(args.params) as param_file:
        params = yaml.safe_load(param_file)

    PROJECT_ROOT = find_project_root()
    BASE_MODEL: str = params['train_lora']['base_model']
    LORA_PATH: str = params['train_lora']['lora_path']
    USE_LORA: bool = params['generate_text_to_image']['use_lora']

    SEED: str = params['generate_text_to_image']['seed']
    NUM_INFERENCE_STEPS: int = params['generate_text_to_image']['num_inference_steps']
    BATCH_SIZE: int = params['generate_text_to_image']['batch_size']
    BATCH_COUNT: int = params['generate_text_to_image']['batch_count']
    PROMPT: str = params['generate_text_to_image']['prompt']
    NEGATIVE_PROMPT: str = params['generate_text_to_image']['negative_prompt']
    OUTPUT_DIRECTORY: str = params['generate_text_to_image']['output_directory']

    pipe = set_up_pipeline(BASE_MODEL, LORA_PATH, USE_LORA)

    for i in range(BATCH_COUNT):
        outputs = generate_images(pipe, SEED, PROMPT, NEGATIVE_PROMPT, BATCH_SIZE, NUM_INFERENCE_STEPS)

        save_images(outputs, OUTPUT_DIRECTORY, batch_iteration=i)