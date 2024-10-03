# RPlease Note: Randomize Aspect Ratio has been changed to a custom script to ensure functionality. If anyone has more exp than me and is willing to help me figure out how to re-implement the ext with the accordion UI I'm open to suggestions. Claude, ChatGPT, Gemini, and Copilot all failed to help me solve it.



# Randomize Aspect Ratio Custom Script for Stable Diffusion WebUI

This script for the Automatic1111 Stable Diffusion WebUI allows you to generate images with randomized aspect ratios, adding variety to your output and potentially inspiring new creative directions. Personally, I use it to randomize Aspect Ratios in conjuction with dynamic prompts and my extension [Random LoRA Injector](https://github.com/ArchAngelAries/random-lora-injector) . Using both with Dynamic Prompts can create both a random and tailored generation experience for unique and random generations.

![Screenshot 2024-10-02 184415](https://github.com/user-attachments/assets/70640314-f0ca-44c9-a4ef-9821e1e125d4)

## Features

- Randomly selects aspect ratios for each generation
- Supports landscape, portrait, and square orientations
- Optional prompt recognition to suggest appropriate aspect ratios
- Customizable minimum and maximum dimensions
- Adds aspect ratio information to generation parameters

## Installation

1. Clone this repository (or download and extract the zip file) into the root folder of your Stable Diffusion WebUI installation:
   
2. Restart your Stable Diffusion WebUI.

## Usage

1. In the Stable Diffusion WebUI, look for the "Randomize Aspect Ratio" in the custom scripts interface.
2. Enable the extension by checking the "Enable Randomize Aspect Ratio" box.
3. Optionally, enable "Use Prompt Recognition" to have the extension suggest aspect ratios based on keywords in your prompt.
4. Adjust the "Minimum Short Side" and "Maximum Short Side" sliders to set your desired size range.
5. Generate your image as usual. The script will randomly select an aspect ratio for each image in your batch.

## Prompt Recognition Keywords

When "Use Prompt Recognition" is enabled, the extension looks for these keywords to suggest orientations:

- Landscape: aerial view, bird's-eye view, establishing shot, extreme long shot, long shot, fisheye-shot, hdri, panorama, wide angle
- Portrait: close-up, extreme close-up, full shot, full body shot, medium close-up, medium shot, cowboy shot, from behind, from the side, over-the-shoulder shot, worm's eye shot, low-angle shot, macro shot
- Square: dutch angle, point-of-view shot, two-shot

If no keywords are found, a random orientation is chosen.

## Notes

- The script ensures that the longer side of the image does not exceed 2048 pixels (Stable Diffusion's limit).
- Aspect ratio information is added to the generation parameters for easy reference.

## Support

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.

Enjoy exploring new aspect ratios in your generations!
