import re


def extract_image_descriptions(text):
    # Regular expression to find text inside square brackets
    pattern = r'\[([^\]]+)\]'

    # Find all matches and return them as a list of strings
    return re.findall(pattern, text)


def remove_brackets_from_file(input_file):
    """
    Reads a text file and removes all text within square brackets [], including the brackets.
    Args:
        input_file (str): Path to the input text file.
    Returns:
        str: Cleaned text if output_file is None, otherwise None.
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Remove text within brackets
        result = ""
        inside_brackets = False
        for char in text:
            if char == '[':
                inside_brackets = True
            elif char == ']':
                inside_brackets = False
            elif not inside_brackets:
                result += char

        return result.replace("Conclusion:", "").replace("Hook:","")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

