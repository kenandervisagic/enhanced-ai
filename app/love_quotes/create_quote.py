import os
import random
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
    }

    # Default case if index is out of range
    return cases.get(index, cases[1])


def get_text_font_size(image_name):
    """Determines text font_size based on image name index."""

    # Extract index number from file name (e.g., "empty_page_3.jpg" → 3)
    match = re.search(r"empty_page_(\d+)", image_name)
    index = int(match.group(1)) if match else 1  # Default to 1 if no number found

    # Define cases with different font sizes
    cases = {
        6: 25,
    }

    # Default case if index is out of range
    return cases.get(index, 20)  # Return 24 as default

def add_text_to_page(image_path, text, output_path):
    """Adds typewriter-style poetic text onto an existing book page image with varied positions."""

    # Open image and get filename
    image = Image.open(image_path)
    image_name = image_path.split("/")[-1]  # Extract file name
    draw = ImageDraw.Draw(image)
    font_size = get_text_font_size(image_name)
    try:
        font = ImageFont.truetype("/app/assets/cour.ttf", font_size)  # Typewriter font
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
        font = ImageFont.truetype("/app/assets/proximanova_regular.ttf", 30)  # Typewriter font
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
                  line, font=font, fill=(255, 255, 255), stroke_width=0.3, stroke_fill=(255, 255, 255))  # You can change the color here (dark gray)
        text_y += line_spacing

    # Save and show the final image
    image.show()
    image.save(output_path)


def create_quotes_images():
    quotes_data = [
        {
            "question": "missing you",
            "quote": "i wish you could see how empty my room feels without you in it."
        },
        {
            "question": "what if",
            "quote": "sometimes i wonder if you ever think about me like i think about you."
        },
        {
            "question": "alone",
            "quote": "i'm so tired of feeling like half a person since you left."
        },
        {
            "question": "memories hurt",
            "quote": "every song reminds me of you. every single one."
        },
        {
            "question": "i'm sorry",
            "quote": "i know i wasn't enough. i know i never will be."
        },
        {
            "question": "nights are hard",
            "quote": "3 am and i'm thinking about all the things i should have done differently."
        },
        {
            "question": "texts i'll never send",
            "quote": "i still check my phone hoping you'll message me. but you won't."
        },
        {
            "question": "letting go",
            "quote": "trying to forget you is like trying to breathe underwater."
        },
        {
            "question": "truth hurts",
            "quote": "i loved you more than you ever loved me. and that hurts."
        },
        {
            "question": "broken",
            "quote": "some days i'm okay. most days i'm not."
        },
        {
            "question": "phantom contact",
            "quote": "i keep my phone charged, hoping you'll text. knowing you won't."
        },
        {
            "question": "replaying",
            "quote": "i replay our last conversation in my head. over and over. looking for something i missed."
        },
        {
            "question": "spaces",
            "quote": "your side of the bed is still empty. i haven't moved your pillow."
        },
        {
            "question": "social media ghosts",
            "quote": "i scroll through your photos. i know i shouldn't. but i can't stop."
        },
        {
            "question": "worthless",
            "quote": "i keep wondering what was wrong with me. why wasn't i enough?"
        },
        {
            "question": "weak moments",
            "quote": "sometimes i want to call you. just to hear your voice. but i know better."
        },
        {
            "question": "memories hurt",
            "quote": "everything reminds me of you. the coffee mug. that jacket. this song."
        },
        {
            "question": "moving on",
            "quote": "trying to forget you feels like trying to hold water in my hands."
        },
        {
            "question": "regrets",
            "quote": "i wish i had said more. or maybe said less."
        },
        {
            "question": "alone",
            "quote": "some nights are harder than others. tonight is one of those nights."
        }
    ]

    # Folder where images are stored
    image_folder = "/app/assets/"
    output_folder = "/app/output/quotes"
    Path(output_folder).mkdir(exist_ok=True)

    # List of available image filenames
    question_images = ['image_1.png', 'image_6.jpg', 'image_7.jpg', 'image_8.jpg', 'image_9.jpg', 'image_10.jpg', "image_13.jpg", "image_14.jpg", "image_15.jpg", "image_16.jpg", "image_17.jpg", "image_18.jpg"]
    quote_images = ['empty_page_1.jpg', 'empty_page_2.jpg', 'empty_page_3.jpg', 'empty_page_5.jpg', 'empty_page_6.jpg', 'empty_page_8.jpg']

    # Loop through the quotes and create images
    for i, data in enumerate(quotes_data):
        question = data['question']
        quote = data['quote']

        # Select random images for question and quote
        question_image = random.choice(question_images)
        quote_image = random.choice(quote_images)

        # Prepare paths for question and quote image files
        question_image_path = os.path.join(image_folder, question_image)
        quote_image_path = os.path.join(image_folder, quote_image)

        # Paths where the generated images will be saved
        first_page_output_path = f"/app/output/quotes/quote_first_page_{i + 1}.png"
        second_page_output_path = f"/app/output/quotes/quote_second_page_{i + 1}.png"

        # Add text to pages using the previously defined add_text_to_page function
        add_text_to_image(question_image_path, "\"{}\"".format(question), first_page_output_path)
        add_text_to_page(quote_image_path, quote, second_page_output_path)

    print("Quote images generated successfully!")
