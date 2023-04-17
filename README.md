# Pokémon concept art generation with Stable Diffusion

This project contains a pipeline to generate Pokémon concept art text2image. It
takes [Stable Diffusion
1.5](https://huggingface.co/runwayml/stable-diffusion-v1-5) as a base model and
trains a [LoRA](https://arxiv.org/abs/2106.09685) model on Pokémon artwork to
tweak its results.

The project serves as a demo project for converting a Jupyter Notebook prototype
into a DVC pipeline. The base notebook is located in
`notebooks/pokemon_generator.ipynb`; the DVC pipeline is defined in `dvc.yaml`.

## How to run

The project is configured to work on a Mac with an M1 chip. Tweaks will be
necessary to run the project on different hardware. Make sure to change
`pipe.to("mps")` in `src/generate_text_to_image.py` if you are not using an M1
(or later) device.

### Requirements (tested)
- [Python >= 3.11.2](https://www.python.org/downloads/)
- [virtualenv >=
  20.14.1](https://virtualenv.pypa.io/en/latest/installation.html)
- A Mac with an M1 chip or later (see above)

### Instructions

1. Clone the repository
2. Create a new virtual environment with `python3 -m venv .venv`
3. Activate the virtual environment with `source .venv/bin/activate`
4. Install the requirements with `pip install -r requirements.txt`
5. [Configure your Kaggle API
   credentials](https://github.com/Kaggle/kaggle-api#api-credentials).
6. To run the notebook, use `jupyter notebook`
7. To run the DVC pipeline, use `dvc repro`. Or use `dvc exp run` for a new
   experiment.
8. If you would like to mirror your DVC cache to a DVC remote, [follow these
   docs](https://dvc.org/doc/user-guide/data-management/remote-storage).

## Further reading
If you would like a more detailed rundown on converting a Jupyter Notebook into
a DVC pipeline, please take a look at the following materials:

- [Blog post: from Jupyter Notebook to DVC pipeline for reproducible ML
  experiments](https://iterative.ai/blog/jupyter-notebook-dvc-pipeline/)
- [Recording of workshop for DTC](https://www.youtube.com/watch?v=t92ISBh4y_E)
- [Repository with instructions for DTC
  workshop](https://github.com/RCdeWit/dtc-workshop)

## Sources used
- https://huggingface.co/docs/diffusers/quicktour
- https://huggingface.co/docs/diffusers/optimization/mps
- https://github.com/cloneofsimo/lora
- https://replicate.com/blog/lora-faster-fine-tuning-of-stable-diffusion
- https://aituts.com/stable-diffusion-lora/
- https://huggingface.co/blog/lora0
- https://old.reddit.com/r/StableDiffusion/comments/1171zhk/how_can_i_make_a_lora_model_on_my_m1_mac/jeraqeb/
- https://civitai.com/models/5115/pokemon-lora-ken-sugimori-style
- https://stable-diffusion-art.com/lora/