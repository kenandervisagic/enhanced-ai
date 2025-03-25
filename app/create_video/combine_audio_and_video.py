import ffmpeg
from numpy.f2py.crackfortran import quiet


def combine_audio_and_video(video_path, audio_path, output_path):
    """
    Combines a video file and an audio file into a final output video.

    :param video_path: Path to the input video file.
    :param audio_path: Path to the input audio file.
    :param output_path: Path to save the final video with audio.
    """
    try:
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(audio_path)

        (
            ffmpeg
            .output(video, audio, output_path, vcodec='libx264', acodec='aac', strict='experimental')
            .run(quiet=False, overwrite_output=True)
        )
        print(f"Video with audio saved at: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")