import logging
import os

from create_srt.create_srt import extract_image_durations_how_to_survive, generate_srt_file, transcribe_audio, \
    extract_image_durations_top_3
from create_srt.srt_to_ass import srt_to_ass
#
from create_video.combine_audio_and_video import combine_audio_and_video
from create_video.combine_srt_and_video import create_video
from create_video.create_video_from_pictures import create_video_from_images
from love_quotes.create_quote import create_quotes_images
from open_ai.api_calls.generate_image import generate_image
from open_ai.api_calls.generate_story import generate_story, PromptType
from text_parsing.parse_text import extract_image_descriptions
from voiceover.create_voiceover import create_voiceover

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

topic_type = os.getenv("TOPIC_TYPE")
topic = os.getenv("TOPIC")


def create_ai_video():
    logging.info(f"Generating story for topic: {topic}")

    try:
        response_gpt = generate_story(topic, topic_type)

        logging.info("Story generation completed successfully.")

        images = extract_image_descriptions(response_gpt)
        logging.info(f"Extracted {len(images)} image descriptions.")
        #
        for index, image in enumerate(images):
            logging.info(f"Generating image {index + 1}/{len(images)}: {image}")
            generate_image(image, index)

        image_folder = '/app/output/images'
        output_video_path = '/app/output/video/final_video_no_sound.mp4'
        audio_path = '/app/output/audio/voiceover_output.mp3'
        create_voiceover(file_path='/app/output/story/story.txt', output_folder='/app/output/audio')
        if topic_type == PromptType.TOP_3:
            timestamps = extract_image_durations_top_3('/app/output/audio/voiceover_output.mp3')
        elif topic_type == PromptType.HOW_TO_SURVIVE:
            timestamps = extract_image_durations_how_to_survive('/app/output/audio/voiceover_output.mp3')
        else:
            exit(1)
        create_video_from_images(image_folder, output_video_path, timestamps, 60, 1.2, 'in')
        combine_audio_and_video('/app/output/video/final_video_no_sound.mp4', audio_path,
                                '/app/output/video/final_video_with_sound.mp4')
        segments = transcribe_audio(audio_path)

        if not segments:
            logging.warning(f"No transcription segments generated for {audio_path}")
            exit(1)
        srt_path = generate_srt_file(segments, audio_path)
        if not srt_path:
            logging.warning(f"Failed to generate SRT for {audio_path}")
            exit(1)

        ass_path = '/app/output/audio/voiceover_output.mp3.ass'
        ass_path = srt_to_ass(srt_path, ass_path)
        if not ass_path:
            logging.warning(f"Failed to convert SRT to ASS for {audio_path}")
            exit(1)
        create_video('/app/output/video/final_video_with_sound.mp4', ass_path,
                     '/app/output/video/final_video_with_captions.mp4')

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        exit(1)

    logging.info("Story and image generation process finished.")


if __name__ == '__main__':
    if topic_type is None:
        logging.error("env variable TOPIC_TYPE must be set")
        exit(1)
    if topic_type != PromptType.QUOTES and topic is None: #quotes don't require topics
        logging.error("env variable TOPIC must be set")
        exit(1)
    if topic_type == PromptType.QUOTES:
        create_quotes_images()
    else:
        create_ai_video()
