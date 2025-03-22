import ffmpeg
import logging

def create_video(video_path, ass_path, output_path):
    try:
        # Input video stream (including audio)
        video_stream = ffmpeg.input(video_path)

        # Apply ASS subtitles to the video
        video_with_subtitles = video_stream.filter('subtitles', ass_path)

        # Output the video with subtitles and preserve original audio
        output = ffmpeg.output(
            video_with_subtitles,
            video_stream['a'],  # Pass the original audio stream
            output_path,
            vcodec='libx264',
            acodec='aac',  # Ensure audio is encoded
            shortest=None,
            preset='ultrafast',
            crf='21'
        )

        # Run the FFmpeg command
        ffmpeg.run(output, overwrite_output=True, quiet=True)
    except ffmpeg.Error as e:
        logging.error(f"FFmpeg error creating video {output_path}: {e.stderr.decode()}")
        raise
    except Exception as e:
        logging.error(f"Error creating video {output_path}: {e}")
        raise
