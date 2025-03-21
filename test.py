import torch
from diffusers import DiffusionPipeline
from diffusers.utils import load_image, export_to_video

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid")
pipe.to("cpu")  # If using a GPU

# Load the image you want to base the video on
image_path = "app/images/generated_image_0.png"
image = load_image(image_path)
generator = torch.manual_seed(42)
# Generate a video (You can modify parameters like the number of frames)
prompt = "A camera slowly zooms in"
frames = pipe(image, decode_chunk_size=8, generator=generator).frames[0]

export_to_video(frames, "generated_image_0.mp4", 14)
