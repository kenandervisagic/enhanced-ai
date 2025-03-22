import os

import openai
import requests

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image(prompt, image_idx):
    try:
        # Call the DALL·E API to generate an image
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,  # Your text prompt
            n=1,  # Number of images to generate
            size="1024x1792"  # The image size
        )

        # Extract the image URL from the response
        image_url = response.data[0].url
        print(f"Image URL: {image_url}")
        if not os.path.exists("/app/output/images"):
            os.makedirs("/app/output/images")

            # Get the image from the URL
        response = requests.get(image_url)

        if response.status_code == 200:
            # Get the image filename from the URL (e.g., the last part of the URL)
            image_filename = os.path.join("/app/output/images", f"generated_image_{image_idx}.png")
            # Save the image to the 'images' directory
            with open(image_filename, 'wb') as f:
                f.write(response.content)
                print(f"Image downloaded successfully to {image_filename}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
