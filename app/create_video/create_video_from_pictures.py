from pathlib import Path
import ffmpeg
from create_video.add_zoom import add_zoom_effect


def create_video_from_images(image_folder, output_video_path, image_durations, framerate=60, zoom_factor=1.05,
                             zoom_type='in'):
    try:
        # Ensure paths are Path objects and absolute
        image_folder = Path(image_folder).resolve()
        output_video_path = Path(output_video_path).resolve()

        # Validate input folder exists
        if not image_folder.exists():
            raise ValueError(f"Image folder '{image_folder}' does not exist")

        # Supported image extensions
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')

        # Get and sort all image files
        images = [img for img in image_folder.iterdir()
                  if img.is_file() and img.suffix.lower() in valid_extensions]

        if not images:
            raise ValueError(f"No valid images found in '{image_folder}'")

        images.sort()  # Sort images by Path object

        # Ensure image_durations matches the number of images
        if len(images) != len(image_durations):
            raise ValueError(
                f"Number of images ({len(images)}) doesn't match number of durations ({len(image_durations)})")

        # Create temporary directory for clips
        temp_clips_dir = image_folder / 'temp_clips'
        temp_clips_dir.mkdir(exist_ok=True)

        # Ensure output directory exists
        output_video_path.parent.mkdir(exist_ok=True)

        # Define variables with absolute paths
        concat_file = image_folder / 'concat_list.txt'
        clip_paths = []

        try:
            # Generate individual clips with zoom effect and apply image durations
            for idx, image in enumerate(images):
                image_path = image  # Already a Path object from iterdir()
                clip_path = temp_clips_dir / f"clip_{idx:04d}.mp4"

                print(f"Processing image: {image_path}")
                duration = image_durations[idx]  # Get the specific duration for this image
                zoomed_clip = add_zoom_effect(image_path, clip_path, duration, framerate, zoom_factor, zoom_type)
                if zoomed_clip and clip_path.exists():
                    clip_paths.append(clip_path)
                    print(f"Clip created: {clip_path}")
                else:
                    print(f"Skipping image {image.name} due to zoom processing error or file not created")

            if not clip_paths:
                raise ValueError("No clips were successfully created. Check add_zoom_effect function.")

            # Write concat file with absolute paths
            print(f"Writing concat file: {concat_file}")
            with open(concat_file, 'w') as f:
                for clip in clip_paths:
                    clip_abs_path = clip.resolve()
                    if clip_abs_path.exists():
                        f.write(f"file '{clip_abs_path}'\n")
                        print(f"Added to concat: {clip_abs_path}")
                    else:
                        print(f"Warning: Clip not found: {clip_abs_path}")

            # Verify concat file exists and is not empty
            if not concat_file.exists():
                raise FileNotFoundError(f"Concat file '{concat_file}' was not created.")
            if concat_file.stat().st_size == 0:
                raise ValueError(f"Concat file '{concat_file}' is empty.")

            # Create final video
            try:
                print(f"Running FFmpeg with input: {concat_file} and output: {output_video_path}")
                stream = ffmpeg.input(str(concat_file), format='concat', safe=0)
                stream = ffmpeg.output(stream, str(output_video_path),
                                       c='copy',
                                       pix_fmt='yuv420p')
                ffmpeg.run(stream, quiet=True, overwrite_output=True)
                print(f"Video successfully created at: {output_video_path}")
            except ffmpeg.Error as e:
                raise Exception(f"Error concatenating clips: {e.stderr.decode()}")

        finally:
            # Cleanup
            if concat_file.exists():
                concat_file.unlink()
            if temp_clips_dir.exists():
                for clip in clip_paths:
                    if clip.exists():
                        clip.unlink()
                try:
                    temp_clips_dir.rmdir()
                except OSError as e:
                    print(f"Warning: Could not remove temp_clips directory: {e}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
