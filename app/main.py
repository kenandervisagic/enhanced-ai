from app.open_ai.api_calls.generate_image import generate_image
from app.open_ai.api_calls.generate_story import generate_story, PromptType, extract_image_descriptions


def main():
    response_gpt = generate_story("How to Survive a Nuclear Fallout", PromptType.HOW_TO_SURVIVE)
    images = extract_image_descriptions(response_gpt)
    is_ok = input("Is this ok")
    if is_ok == "yes":
        for index, image in enumerate(images):
            generate_image(image, index)
            print(index, image)
    else:
        exit(1)

if __name__ == '__main__':
    main()