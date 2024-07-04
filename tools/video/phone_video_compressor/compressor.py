import glob
from datetime import datetime
from pathlib import Path, PurePath

import ffmpeg

OUTPUT_FOLDER = "compressed"


class Compressor:
    """Compress phone videos in a particular directory."""

    @staticmethod
    def _get_dt_for_recording(input_path: Path) -> str:
        """Probe metadata for creation_time."""
        # Default to using the current datetime in isoformat.
        created_dt = datetime.now()
        try:
            probe_creation_time = (
                ffmpeg.probe(input_path)
                .get("streams")[0]
                .get("tags")
                .get("creation_time")
            )
            dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            created_dt = datetime.strptime(probe_creation_time, dt_format)
        except AttributeError:
            pass
        except TypeError:
            pass
        except ffmpeg.Error as exc:
            raise exc

        return created_dt.strftime("%Y-%m-%d_%H%M%S")

    @staticmethod
    def _create_output_name(input_path: Path) -> PurePath:
        """Create a new file with a standard output name."""
        created_dt = Compressor._get_dt_for_recording(input_path=input_path)

        # Create new output dir if it does not exist.
        output_dir = PurePath(input_path).parent
        output_path = output_dir.joinpath(OUTPUT_FOLDER)
        Path(output_path).mkdir(parents=True, exist_ok=True)

        # Create new filename and place it in the output path.
        file_ext = PurePath(input_path).suffix
        new_file_name = f"VIDEO_{created_dt}{file_ext}"
        new_file_path = output_path.joinpath(new_file_name)

        return new_file_path

    @staticmethod
    def compress_file(input_path: str, logging=False) -> None:
        """
        Compress video at ``input_path``.

        Notes
        -----
        - ``sn`` refers to Subtitles being ignored or not.
            - See: https://github.com/kkroening/ffmpeg-python/issues/514
        - ``scale`` in the video filter takes -2 ("keep aspect ratio")
          and 720 (for 720p).
        """
        _input_path = Path(input_path).absolute()
        print(f"* Compressing: {_input_path}")

        output_path = Compressor._create_output_name(input_path=_input_path)

        start_time = datetime.now()

        # The compression.
        input_stream = ffmpeg.input(_input_path, sn=None)
        vid = input_stream.video.filter("scale", -2, 720)
        aud = input_stream.audio
        output = ffmpeg.output(
            vid,
            aud,
            filename=output_path,
            format="mp4",
            preset="slower",
            vcodec="libx264",
            acodec="aac",
            r=29.93,  # Framerate
            crf=22,  # Constant Rate Factor
        ).run_async(pipe_stdout=True, pipe_stderr=True)

        if logging:
            out, err = output.communicate()
            output_dir = PurePath(_input_path).parent
            with open(
                output_dir.joinpath("output.log"), "w+", encoding="utf-8"
            ) as elog:
                elog.write(err.decode("utf-8"))
                elog.write(out.decode("utf-8"))

        print(f"* Compressed file at: {output_path}")

        total_conv_time_secs = (datetime.now() - start_time).total_seconds()
        total_conv_time_mins = round(10 * (total_conv_time_secs / 60)) / 10
        print(f"* Total compressed time: {total_conv_time_mins} minutes.")

    @staticmethod
    def compress_all(input_path: str, logging=False) -> None:
        """Call ``compress_file`` on all files in the input path."""
        _input_path = Path(input_path).absolute()

        for movie_path in glob.glob(f"{_input_path}/*.mp4"):
            Compressor.compress_file(input_path=movie_path, logging=logging)


if __name__ == "__main__":
    import sys

    Compressor.compress_file(input_path=sys.argv[1], logging=True)
