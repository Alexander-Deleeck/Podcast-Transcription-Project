This is a project for transcribing, archiving and displaying podcast transcriptions, similar to Andrej Karpathy's "Lexicap".

The goal is to create podcast transcriptions with diarization (speaker identification) and subsequently archive them in well-organized JSON files.
The JSON files are subsequently used for generating HTML pages which display the transcripts in a clear way.

Although the files in this repository are a subset of the entire project, you can find some examples of the transcripts, json and html files for both a podcast with Dr. Michael Levin and Hamilton Morris. 

The script "transcribe_and_diarize.py" contains an end-to-end pipeline for transcribing & diarizing new audio files from the data folder,
orgizing the results in the JSON format and lastly automatically creating the HTML page.
This pipeline should be run from the command line, and can either take the following arguments:
- Filepath to audio file: this only transcribes 1 audio file.
- "Michael" or "Hamilton", followed by "youtube_guest" or "youtube_lectures", which transcribes all audio files in the raw_audio folder of the respective podcaster.

The primary tools used are the following:
- Whisper: transcription software created by OpenAI which runs locally
- Pyannote: diarization models for speaker identification
