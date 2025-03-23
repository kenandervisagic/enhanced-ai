import os
import openai
import requests

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def refine_prompt(original_prompt):
    """
    Uses ChatGPT to refine the prompt if it violates DALL·E's content policy.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Ensure the prompt follows OpenAI's content policy."},
                {"role": "user", "content": f"Refine this prompt while keeping its intent: {original_prompt}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error refining prompt: {e}")
        return original_prompt  # Fallback to the original prompt


def generate_image(prompt, image_idx):
    """
    Generates an image using DALL·E. If the prompt is rejected, it refines and retries once.
    """
    attempt = 0
    os.makedirs("/app/output/images", exist_ok=True)

    while attempt < 2:  # Allow one retry after refining the prompt
        try:
            print(f"Attempt {attempt + 1}: Generating image for prompt: {prompt}")

            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1792"
            )

            if response and response.data:
                image_url = response.data[0].url
                print(f"Image URL: {image_url}")

                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    image_filename = os.path.join("/app/output/images", f"generated_image_{image_idx}.png")
                    with open(image_filename, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Image downloaded successfully to {image_filename}")
                    return image_filename
                else:
                    print(f"Failed to download image. Status code: {img_response.status_code}")
                    return None

        except openai.OpenAIError as e:
            if "400" in str(e) and attempt == 0:  # Only refine the prompt on the first failure
                print(f"Prompt violation detected. Refining prompt...")
                prompt = refine_prompt(prompt)  # Get a refined prompt
            else:
                print(f"An error occurred: {e}")
                return None

        attempt += 1  # Increment attempt only if an error occurred

    print("Image generation failed after all attempts.")
    return None
