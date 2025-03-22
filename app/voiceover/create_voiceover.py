import os

from text_parsing.parse_text import remove_brackets_from_file
from tiktok_voice import Voice, tts


def create_voiceover(file_path, output_folder):
    """
    Reads a text file from the given location, processes it with remove_brackets_from_file(),
    generates a voiceover using tts(), and saves the output audio file.

    :param file_path: Path to the input text file.
    :param output_folder: Folder where the output audio file should be saved.
    """
    try:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Define the output file path
        output_path = os.path.join(output_folder, "voiceover_output.mp3")

        # Process the text file
        parsed_text = remove_brackets_from_file(file_path)

        # Generate the voiceover
        tts(parsed_text, Voice.US_MALE_1, output_path)

        print(f"Voiceover saved at: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")