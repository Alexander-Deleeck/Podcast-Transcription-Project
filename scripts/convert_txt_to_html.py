from utils import txt_to_json, json_to_html
from constants import PATH_TO_DATA
import os
import shutil

podcast_series = "Hamilton Morris"
podcast_series_folder = PATH_TO_DATA + podcast_series + '/'
text_folder = podcast_series_folder + 'text/'
text_files_list = os.listdir(text_folder+'text_unprocessed/')

for file in text_files_list:
    filepath_source = text_folder + 'text_unprocessed/'+ file
    filepath_dest = text_folder + file

    result_json = txt_to_json(filepath_source, podcast_series_folder)
    json_to_html(result_json, podcast_series_folder)

    shutil.move(filepath_source, filepath_dest)
    print(f"done with {file}\n")
    print(f"Text moved to {filepath_dest}")
