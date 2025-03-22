import logging

from open_ai.api_calls.generate_image import generate_image
from open_ai.api_calls.generate_story import generate_story, PromptType, extract_image_descriptions

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    logging.info("Starting story generation process...")

    topic = "How to Survive a Nuclear Fallout"
    logging.info(f"Generating story for topic: {topic}")

    try:
        response_gpt = generate_story(topic, PromptType.HOW_TO_SURVIVE)
        logging.info("Story generation completed successfully.")

        images = extract_image_descriptions(response_gpt)
        logging.info(f"Extracted {len(images)} image descriptions.")

        for index, image in enumerate(images):
            logging.info(f"Generating image {index + 1}/{len(images)}: {image}")
            generate_image(image, index)
            logging.info(f"Image {index + 1} generated successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

    logging.info("Story and image generation process finished.")


if __name__ == '__main__':
    main()
