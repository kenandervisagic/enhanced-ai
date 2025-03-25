import os
import re
from enum import Enum

import openai

from open_ai.prompts.how_to_survive import prompt as prompt_how_to_survive
from open_ai.prompts.how_to_survive import system_prompt as system_prompt_how_to_survive
from open_ai.prompts.life_hacks import prompt as life_hacks_prompt, system_prompt as system_prompt_life_hacks
from open_ai.prompts.top3 import prompt as prompt_top3
from open_ai.prompts.top3 import system_prompt as system_prompt_top3

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class PromptType(Enum):
    HOW_TO_SURVIVE = 1
    TOP_3 = 2
    QUOTES = 3
    LIFEHACKS = 4


def get_user_prompt(topic, prompt_type):
    match prompt_type:
        case PromptType.LIFEHACKS:
            return life_hacks_prompt.format(topic=topic)
        case PromptType.HOW_TO_SURVIVE:
            return prompt_how_to_survive.format(topic=topic)
        case PromptType.TOP_3:
            return prompt_top3.format(topic=topic)


def get_system_prompt(prompt_type):
    match prompt_type:
        case PromptType.LIFEHACKS:
            return system_prompt_life_hacks
        case PromptType.HOW_TO_SURVIVE:
            return system_prompt_how_to_survive
        case PromptType.TOP_3:
            return system_prompt_top3


def refine_prompt(original_prompt):
    """
    Uses ChatGPT to refine the prompt if it violates DALL·E's content policy.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that ensures image generation prompts follow OpenAI's content policy."
                },
                {
                    "role": "user",
                    "content": f"The following prompt violated DALL·E's content policy: '{original_prompt}'. "
                               f"Please refine it while maintaining the original intent and ensuring it adheres to the guidelines."
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error refining prompt: {e}")
        return original_prompt


def generate_story(topic, prompt_type):
    # Select and fill out prompt based on topic and prompt type enum
    system_prompt = get_system_prompt(prompt_type)
    user_prompt = get_user_prompt(topic, prompt_type)

    # Send API request
    response = client.chat.completions.create(
        model="gpt-4-turbo",
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
    directory = "/app/output/story"  # Change this to your preferred directory path

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the story to a file within the directory
    file_path = os.path.join(directory, "story.txt")
    with open(file_path, "w") as file:
        file.write(story)

    return story

