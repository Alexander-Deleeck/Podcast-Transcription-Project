import whisper
import os
import sys
import shutil
from pyannotate_whisper import diarize_text
from stereo_to_mono import convert_stereo_to_mono   
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from utils import correct_word_errors, create_json, json_to_html
import torch
from dotenv import load_dotenv
device = "cuda" if torch.cuda.is_available() else "cpu"

load_dotenv()
HF_DIARIZATION_TOKEN = os.environ.get("HF_DIARIZATION_TOKEN")

def run_transcription_pipeline(path):
    print("starting")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)
    print("loaded whisper")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=HF_DIARIZATION_TOKEN)
    pipeline.to(torch.device(device))
    print("loaded pipeline")

    with ProgressHook() as hook:
        diarization_result = pipeline(path, hook=hook)#, device=torch.device("cuda"))
    print("diarized")
    
    transcription_result = model.transcribe(path, verbose=True)
    print("transcribed")
    full_result = diarize_text(transcription_result, diarization_result)

    corrected_result = correct_word_errors(full_result)

    # Create JSON file from transcription (can later be used for RAG)
    condensed_json = create_json(corrected_result, path)
    json_to_html(condensed_json, path)

    # Move processed file to archive folder
    archive_path = f"./data/{path.split('/')[2]}/audio_transcribed/{path.split('/')[-1]}"
    shutil.move(path, archive_path)
    print(f"Processed: {path.split('/')[-1]}")
    return 

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    # Get the parent directory of the script (if the script is in 'scripts/' subfolder)
    project_root = os.path.dirname(os.path.dirname(script_path))
    # Change the current working directory to the project root
    os.chdir(project_root)
    # Get user input parameter from command line prompt
    input_parameter = sys.argv[1]

    if '.mp3' in input_parameter:
        run_transcription_pipeline(input_parameter)
    elif input_parameter == "Hamilton":
        audio_subfolder = input("patreon_podcasts or youtube_guest?")
        path_raw_folder = f"./data/Hamilton Morris/audio_raw/{audio_subfolder}/"
        for file in os.listdir(path_raw_folder):
            path_audio = path_raw_folder + file
            run_transcription_pipeline(path_audio)

    elif input_parameter == "Michael":
        audio_subfolder = input("youtube_lectures or youtube_guest?")
        path_raw_folder = f"./data/Michael Levin/audio_raw/{audio_subfolder}/"
        for file in os.listdir(path_raw_folder):
            path_audio = path_raw_folder + file
            convert_stereo_to_mono(path_audio, path_audio)
            run_transcription_pipeline(path_audio)

    else:
        print("Invalid arguments")