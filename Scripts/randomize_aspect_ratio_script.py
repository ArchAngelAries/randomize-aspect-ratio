import modules.scripts as scripts
import gradio as gr
import random
import math

from modules import processing
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

class Script(scripts.Script):
    def __init__(self):
        self.keyword_orientations = {
            'landscape': [
                'aerial view', 'bird\'s-eye view', 'establishing shot', 'extreme long shot',
                'long shot', 'fisheye-shot', 'hdri', 'panorama', 'wide angle'
            ],
            'portrait': [
                'close-up', 'extreme close-up', 'full shot', 'full body shot',
                'medium close-up', 'medium shot', 'cowboy shot', 'from behind',
                'from the side', 'over-the-shoulder shot', 'worm\'s eye shot',
                'low-angle shot', 'macro shot'
            ],
            'square': ['dutch angle', 'point-of-view shot', 'two-shot']
        }

    def title(self):
        return "Randomize Aspect Ratio and Layout"

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Row():
                is_enabled = gr.Checkbox(label="Enable Randomize Aspect Ratio", value=False)
            with gr.Row():
                use_prompt_recognition = gr.Checkbox(label="Use Prompt Recognition", value=False)
            with gr.Row():
                min_dim = gr.Slider(minimum=64, maximum=2048, step=8, label="Minimum Short Side", value=512)
                max_dim = gr.Slider(minimum=64, maximum=2048, step=8, label="Maximum Short Side", value=1024)

        return [is_enabled, use_prompt_recognition, min_dim, max_dim]

    def recognize_orientation(self, prompt):
        prompt = prompt.lower()
        for orientation, keywords in self.keyword_orientations.items():
            if any(keyword in prompt for keyword in keywords):
                return orientation
        return 'random'

    def calculate_dimensions(self, width_ratio, height_ratio, min_dim, max_dim):
        # Determine the shorter side of the aspect ratio
        if width_ratio < height_ratio:
            short_ratio, long_ratio = width_ratio, height_ratio
        else:
            short_ratio, long_ratio = height_ratio, width_ratio

        # Calculate the short side dimension
        short_side = random.randint(min_dim, max_dim)

        # Calculate the long side based on the aspect ratio
        long_side = math.floor(short_side * (long_ratio / short_ratio))

        # Ensure the long side doesn't exceed 2048 (SD limit)
        if long_side > 2048:
            long_side = 2048
            short_side = math.floor(long_side * (short_ratio / long_ratio))

        # Assign dimensions back to width and height
        if width_ratio < height_ratio:
            width, height = short_side, long_side
        else:
            width, height = long_side, short_side

        return width, height

    def process(self, p, is_enabled, use_prompt_recognition, min_dim, max_dim):
        if not is_enabled:
            return p

        p.extra_generation_params["Randomize Aspect Ratio"] = True
        return p

    def run(self, p, is_enabled, use_prompt_recognition, min_dim, max_dim):
        if not is_enabled:
            return processing.process_images(p)

        aspect_ratios = {
            'landscape': [(16, 9), (3, 2), (4, 3)],
            'portrait': [(9, 16), (2, 3), (3, 4)],
            'square': [(1, 1)],
            'random': [(16, 9), (9, 16), (4, 3), (3, 4), (1, 1)]
        }

        original_batch_size = p.batch_size
        p.batch_size = 1  # Process one image at a time to allow different sizes

        all_processed = []
        for _ in range(original_batch_size):
            if use_prompt_recognition:
                orientation = self.recognize_orientation(p.prompt)
            else:
                orientation = 'random'

            aspect_ratio = random.choice(aspect_ratios[orientation])
            
            if orientation == 'random':
                if random.choice([True, False]):
                    aspect_ratio = aspect_ratio[::-1]  # Flip for random orientation
            
            width_ratio, height_ratio = aspect_ratio
            
            # Calculate dimensions
            p.width, p.height = self.calculate_dimensions(width_ratio, height_ratio, min_dim, max_dim)

            p.init_latent = None  # Reset latent to force recalculation with new dimensions

            processed = processing.process_images(p)
            
            # Add aspect ratio info to generation parameters
            processed.infotexts[0] = f"{processed.infotexts[0]}, Randomized Base Dimensions: {p.width}x{p.height}, Aspect Ratio: {width_ratio}:{height_ratio}, Orientation: {orientation}"
            
            all_processed.append(processed)

        # Combine all processed results
        combined = Processed(p, [], p.seed, "")
        for processed in all_processed:
            combined.images.extend(processed.images)
            combined.all_prompts.extend(processed.all_prompts)
            combined.all_seeds.extend(processed.all_seeds)
            combined.infotexts.extend(processed.infotexts)

        return combined