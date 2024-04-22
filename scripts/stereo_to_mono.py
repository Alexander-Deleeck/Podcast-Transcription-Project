from pydub import AudioSegment
import os
import sys

def convert_stereo_to_mono(input_file_path, output_file_path=None):
    """This function reduces the number of channels in the audio file to a single channel (mono audio).
    Thereby, the filesize is reduced, and the audio can be transformed into a tensor that is directly useable by the Whisper transcription & diarization models
    """
    if not output_file_path:
        output_file_path = input_file_path.rsplit('.', maxsplit=1)[-2] + "_mono.mp3"
    # Load the stereo audio file
    stereo_audio = AudioSegment.from_file(input_file_path)
    # Convert to mono
    mono_audio = stereo_audio.set_channels(1)
    # Export the mono audio to a file
    mono_audio.export(output_file_path, format="mp3")
    
    print(f"Converted mono audio saved to {output_file_path}")
    return

if __name__ == '__main__':
    filepath = str(sys.argv[1])
    if not filepath:
        raise ValueError("No path to audio file was provided")
    convert_stereo_to_mono(filepath, filepath)