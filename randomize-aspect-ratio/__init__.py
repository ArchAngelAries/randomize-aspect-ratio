from modules import script_callbacks
from .scripts.randomize_aspect_ratio import RandomizeAspectRatio

def on_app_started(block, app):
    pass  # You can add any initialization code here if needed

script_callbacks.on_app_started(on_app_started)