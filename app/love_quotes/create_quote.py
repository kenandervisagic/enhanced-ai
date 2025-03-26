import json
import os
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def format_poem(text, max_words_per_line=3):
    """Breaks text into a poetic format with short, centered lines."""
    words = text.split()
    poem_lines = []

    while words:
        line = " ".join(words[:max_words_per_line])
        poem_lines.append(line)
        words = words[max_words_per_line:]

    return "\n".join(poem_lines)


def get_text_position(image_name, image_width, image_height):
    """Determines text position based on image name index."""

    # Extract index number from file name (e.g., "empty_page_3.jpg" → 3)
    match = re.search(r"empty_page_(\d+)", image_name)
    index = int(match.group(1)) if match else 1  # Default to 1 if no number found

    # Define cases with different text positions (no rotation)
    cases = {
        1: {"x": image_width // 2, "y": image_height // 3},
        2: {"x": image_width // 1.8, "y": image_height // 2.3},
        3: {"x": image_width // 1.6, "y": image_height // 2.9},
        4: {"x": image_width // 1.4, "y": image_height // 2.5},
        5: {"x": image_width // 1.8, "y": image_height // 4},
        6: {"x": image_width // 1.7, "y": image_height // 2.2},
        7: {"x": image_width // 1.93, "y": image_height // 2.4},
        8: {"x": image_width // 1.97, "y": image_height // 2.6},
        9: {"x": image_width // 2.05, "y": image_height // 3.3},
        10: {"x": image_width // 1.95, "y": image_height // 3.3},
        11: {"x": image_width // 1.95, "y": image_height // 3.3},

    }

    # Default case if index is out of range
    return cases.get(index, cases[1])


def get_text_font_size(image_name):
    """Determines text font_size based on image name index."""

    # Extract index number from file name (e.g., "empty_page_3.jpg" → 3)
    match = re.search(r"empty_page_(\d+)", image_name)
    index = int(match.group(1)) if match else 5  # Default to 1 if no number found

    # Define cases with different font sizes
    cases = {
        5: 18,
        6: 20,
    }

    # Default case if index is out of range
    return cases.get(index, 20)  # Return 20 as default


def add_text_to_page(image_path, text, output_path):
    """Adds typewriter-style poetic text onto an existing book page image with varied positions."""

    # Open image and get filename
    image = Image.open(image_path)
    image_name = image_path.split("/")[-1]  # Extract file name
    draw = ImageDraw.Draw(image)
    font_size = get_text_font_size(image_name)
    try:
        font = ImageFont.truetype("/app/assets/fonts/cour.ttf", font_size)  # Typewriter font
    except:
        font = ImageFont.load_default()

    # Format text as a poem
    poem_text = format_poem(text, max_words_per_line=3)

    # Get position based on the image name
    settings = get_text_position(image_name, image.width, image.height)
    text_x, text_y = settings["x"], settings["y"]

    # Draw text on image
    line_spacing = 25  # Space between lines
    for line in poem_text.split("\n"):
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        line_x = text_x - text_width // 2  # Center align text
        jitter_x = np.random.randint(-1, 2)
        jitter_y = np.random.randint(-1, 2)
        draw.text((line_x + jitter_x, text_y + jitter_y),
                  line, font=font, fill=(25, 25, 25), stroke_width=0.2, stroke_fill=(35, 35, 35))
        text_y += line_spacing

    # Save and show the final image
    image.show()
    image.save(output_path)


def add_text_to_image(image_path, text, output_path):
    """Adds typewriter-style poetic text to an image with a different font and style."""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("/app/assets/fonts/proximanova_regular.ttf", 33)  # Typewriter font
    except:
        font = ImageFont.load_default()

    # Format text as a poem
    poem_text = format_poem(text, max_words_per_line=5)

    # Define text area (position will be adjusted based on image size)
    text_x = image.width // 2
    text_y = image.height // 4  # Adjusted for a lower position
    line_spacing = 25  # More space between lines

    # Draw text centered on the image
    for line in poem_text.split("\n"):
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        line_x = text_x - text_width // 2  # Center align text
        jitter_x = np.random.randint(-1, 2)
        jitter_y = np.random.randint(-1, 2)
        draw.text((line_x + jitter_x, text_y + jitter_y),
                  line, font=font, fill=(255, 255, 255), stroke_width=0.3,
                  stroke_fill=(255, 255, 255))  # You can change the color here (dark gray)
        text_y += line_spacing

    # Save and show the final image
    image.show()
    image.save(output_path)


def create_quotes_images():
    # Load quotes from JSON file
    with open("/app/assets/quotes.json", "r", encoding="utf-8") as file:
        quotes_data = json.load(file)

    # Folder where images are stored
    image_folder = "/app/assets/quotes_images"
    output_folder = "/app/output/quotes"
    Path(output_folder).mkdir(exist_ok=True)

    # List of available image filenames
    tagline_images = ['image_1.png', 'image_2.jpg', 'image_3.jpg', 'image_4.jpg', 'image_5.jpg', 'image_6.jpg',
                      'image_7.jpg', 'image_8.jpg', 'image_9.jpg', 'image_10.jpg', 'image_11.jpg',
                      "image_13.jpg", "image_14.jpg", "image_15.jpg", "image_16.jpg", "image_17.jpg", "image_18.jpg"]
    quote_images = ['empty_page_1.jpg', 'empty_page_2.jpg', 'empty_page_3.jpg', 'empty_page_4.jpg', 'empty_page_5.jpg',
                    'empty_page_6.jpg', 'empty_page_7.jpg', 'empty_page_8.jpg', 'empty_page_9.jpg', 'empty_page_10.jpg',
                    'empty_page_11.jpg']

    # Initialize indices for looping through images
    tagline_index = 0
    quote_index = 0
    tagline_count = len(tagline_images)
    quote_count = len(quote_images)

    # Loop through the quotes and create images
    for i, data in enumerate(quotes_data):
        tagline = data['tagline']
        quote = data['quote']

        # Select images sequentially, looping back when reaching the end
        tagline_image = tagline_images[tagline_index]
        quote_image = quote_images[quote_index]

        # Update indices and loop back if necessary
        tagline_index = (tagline_index + 1) % tagline_count
        quote_index = (quote_index + 1) % quote_count

        # Prepare paths for tagline and quote image files
        tagline_image_path = os.path.join(image_folder, tagline_image)
        quote_image_path = os.path.join(image_folder, quote_image)

        # Paths where the generated images will be saved
        first_page_output_path = f"{output_folder}/quote_first_page_{i + 1}.png"
        second_page_output_path = f"{output_folder}/quote_second_page_{i + 1}.png"

        # Add text to pages using the previously defined add_text_to_page function
        add_text_to_image(tagline_image_path, f"\"{tagline}\"", first_page_output_path)
        add_text_to_page(quote_image_path, quote, second_page_output_path)

    print("Quote images generated successfully!")
