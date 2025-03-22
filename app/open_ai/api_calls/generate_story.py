import os
import re
from enum import Enum

import openai

from open_ai.prompts.how_to_survive import prompt as prompt_how_to_survive
from open_ai.prompts.how_to_survive import system_prompt as system_prompt_how_to_survive
from open_ai.prompts.life_hacks import prompt as life_hacks_prompt, system_prompt as system_prompt_life_hacks
from open_ai.prompts.top5 import prompt as prompt_top5
from open_ai.prompts.top5 import system_prompt as system_prompt_top5

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class PromptType(Enum):
    LIFEHACKS = 1
    HOW_TO_SURVIVE = 2
    TOP_5 = 3


def get_user_prompt(topic, prompt_type):
    match prompt_type:
        case PromptType.LIFEHACKS:
            return life_hacks_prompt.format(topic=topic)
        case PromptType.HOW_TO_SURVIVE:
            return prompt_how_to_survive.format(topic=topic)
        case PromptType.TOP_5:
            return prompt_top5.format(topic=topic)


def get_system_prompt(prompt_type):
    match prompt_type:
        case PromptType.LIFEHACKS:
            return system_prompt_life_hacks
        case PromptType.HOW_TO_SURVIVE:
            return system_prompt_how_to_survive
        case PromptType.TOP_5:
            return system_prompt_top5


def generate_story(topic, prompt_type):
    # Select and fill out prompt based on topic and prompt type enum
    system_prompt = get_system_prompt(prompt_type)
    user_prompt = get_user_prompt(topic, prompt_type)

    # Send API request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000
    )

    # Extract and print the story
    story = response.choices[0].message.content
    print(story)

    # Define the directory path where the file will be saved
    directory = "/app/story"  # Change this to your preferred directory path

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the story to a file within the directory
    file_path = os.path.join(directory, "story.txt")
    with open(file_path, "w") as file:
        file.write(story)

    return story


def extract_image_descriptions(text):
    # Regular expression to find text inside square brackets
    pattern = r'\[([^\]]+)\]'

    # Find all matches and return them as a list of strings
    return re.findall(pattern, text)
