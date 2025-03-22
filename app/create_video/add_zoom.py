import os

import ffmpeg

def add_zoom_effect(input_path, output_path, duration, framerate, zoom_factor=1.1, zoom_type='in'):
    """
    Adds a subtle, smooth zoom effect to a single clip, centered, optimized for TikTok 9:16.
    """
    try:
        # Convert Path objects to strings if necessary
        input_path = str(input_path)
        output_path = str(output_path)

        # Validate input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file '{input_path}' does not exist")

        # Calculate zoom expression for subtle effect
        if zoom_type == 'in':
            zoom_expr = f'zoom+{(zoom_factor-1)/(framerate*duration)}'  # Subtle zoom in
        elif zoom_type == 'out':
            zoom_expr = f'zoom-{(zoom_factor-1)/(framerate*duration)}:zoom={zoom_factor}'  # Subtle zoom out
        else:
            raise ValueError("zoom_type must be 'in' or 'out'")

        # Apply zoom effect with improved smoothness
        stream = ffmpeg.input(input_path, loop=1, t=duration, framerate=framerate)
        # Pre-scale slightly larger with Lanczos to reduce jitter
        stream = ffmpeg.filter(stream, 'scale',
                              w='1080*1.2', h='1920*1.2',  # Pre-scale 20% larger
                              force_original_aspect_ratio='increase',
                              sws_flags='lanczos')  # Use Lanczos for smooth scaling
        # Apply zoompan with correct centered zoom
        stream = ffmpeg.filter(stream, 'zoompan',
                              z=zoom_expr,
                              d=int(duration*framerate),
                              s='1080x1920',  # TikTok 9:16 resolution
                              fps=framerate,
                              x='iw/2-(iw/zoom/2)',  # Center horizontally
                              y='ih/2-(ih/zoom/2)')  # Center vertically
        # Final scale and crop with Lanczos to exact 9:16
        stream = ffmpeg.filter(stream, 'scale',
                              w=1080, h=1920,
                              force_original_aspect_ratio='increase',
                              sws_flags='lanczos')
        stream = ffmpeg.filter(stream, 'crop',
                              w=1080, h=1920)
        stream = ffmpeg.output(stream, output_path,
                              vcodec='libx264',
                              pix_fmt='yuv420p',
                              t=duration)
        ffmpeg.run(stream, quiet=True, overwrite_output=True)
        print(f"Zoom effect applied successfully to {output_path}")
        return output_path
    except ffmpeg.Error as e:
        print(f"Error applying zoom effect: {e.stderr.decode()}")
        return None
    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        return None