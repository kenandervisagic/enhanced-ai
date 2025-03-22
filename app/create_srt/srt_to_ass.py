import random

import srt


def srt_to_ass(srt_path, ass_path, font="Comic Sans MS Bold Italic", font_size=55):
    try:
        with open(srt_path, "r", encoding="utf-8") as f:
            subtitles = list(srt.parse(f.read()))

        ass_header = f"""[Script Info]
Title: Converted Subtitles
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: YellowFont,{font},{font_size},&H0000FFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0.0,0.0,1,4.0,1,5,100,100,10,1
Style: YellowFontUnderThumbnail,{font},{font_size},&H0000FFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0.0,0.0,1,4.0,1,2,100,100,150,1
Style: PurpleFont,{font},{font_size},&H00FF00FF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0.0,0.0,1,4.0,1,5,100,100,10,1
Style: BlackFont,{font},{font_size},&H00000000,&H0000FFFF,&H0000FFFF,&H0000FFFF,-1,0,0,0,100,100,0.0,0.0,1,4.0,1,5,100,100,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        def format_timedelta(t):
            total_seconds = int(t.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            milliseconds = t.microseconds // 10000
            return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"

        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header)
            should_go_under_thumbnail = True
            one_more_time_under_thumbnail = False

            for sub in subtitles:
                start = format_timedelta(sub.start)
                end = format_timedelta(sub.end)
                text = sub.content.replace("\n", "\\N")

                percentage = random.random()
                style = ("PurpleFont" if percentage < 0.2 else
                         "BlackFont" if percentage < 0.3 else
                         "YellowFont")

                if one_more_time_under_thumbnail:
                    style = "YellowFontUnderThumbnail"
                    one_more_time_under_thumbnail = False

                if should_go_under_thumbnail:
                    style = "YellowFontUnderThumbnail"
                    if text.strip() == "PART":
                        one_more_time_under_thumbnail = True
                        should_go_under_thumbnail = False

                f.write(f"Dialogue: 0,{start},{end},{style},,0,0,0,,{text}\n")
        return ass_path
    except Exception as e:
        return None
