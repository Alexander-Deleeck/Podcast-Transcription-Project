from constants import REPLACEMENT_DICT, PRE_S, POST_S
import os
import re
import json

def get_podcast_attributes(creator_name):
    if "hamilton" in creator_name.lower():
        attributes = {"image_url":"https://img.youtube.com/vi/LMhqTrAn56A/maxresdefault.jpg",
                      "youtube_url":"https://www.youtube.com/@hamiltonmorris"}
    elif "michael" in creator_name.lower():
        attributes = {"image_url":"https://www.youtube.com/@drmichaellevin",
                      "youtube_url":"https://yt3.ggpht.com/_VcY9oC2Ll9BE_62EQNWLtXbMMqG-oJn7WbwLlLsb3ThFn6eKebsmU2W1uXoJt4fgNSCToXJ=s176-c-k-c0x00ffffff-no-rj-mo"}
    else:
        attributes = {"image_url":"",
                      "youtube_url":"https://www.youtube.com/"}
    return attributes


def correct_word_errors(transcription_result:list, replacement_dict:dict=REPLACEMENT_DICT):
    modified_transcription = []
    for a, b, c in transcription_result:
        for old, new in replacement_dict.items():
            c = c.replace(old, new)
        modified_transcription.append((a, b, c))
    return modified_transcription


def seconds_to_timestamp(seconds_str):
    # Convert the string to float to get both the whole and fractional seconds
    total_seconds = float(seconds_str)
    
    # Calculate hours, minutes, and seconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    # Calculate milliseconds (the fractional part of the seconds)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)
    
    # Format these components into a string with the format HH:MM:ss.sss
    timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    return timestamp


def condense_json_texts(input_json, N:int = 700):
    """
    Condenses texts in the input JSON based on the length criteria and speaker matching.
    Parameters:
    - input_json (dict): Input JSON-like dictionary.
    - N (int): The length threshold for the text.
    Returns:
    - dict: Modified JSON-like dictionary with condensed texts.
    """
    keys_to_delete = []
    prev_key = None

    for key, value in list(input_json.items()):
        # Skip this key if it's marked for deletion
        if key in keys_to_delete or key == "title":
            continue
        # Only proceed if there's a previous key and the current and previous speakers match
        if prev_key is not None and input_json[prev_key]['speaker'] == value['speaker']:
            combined_text = input_json[prev_key]['text'] + " " + value['text']

            if len(input_json[prev_key]['text']) < N and len(combined_text) <= N:
                input_json[prev_key]['text'] = combined_text
                keys_to_delete.append(key)
            else:
                prev_key = key
        else:
            prev_key = key

    # Delete the marked keys
    print(f"Condensed {len(keys_to_delete)} sections.")
    for key in keys_to_delete:
        del input_json[key]
    return input_json


def create_html_title(podcast_title:str, image_url:str):
    html_title_section = f"""
    <h2>{podcast_title}</h2>
    <a><img src={image_url} width=auto height=250> </a>"""

    return html_title_section


def json_to_html(json_dict:dict, path:str):#, podcast_series_folder:str):
    if '.json' in path: # Ensures that you can convert both path to mp3 and path to json into html
        creator_name = path.split("/")[-3]
    else:
        creator_name = path.split("/")[-4]
    print(f"creator name: {creator_name}")
    attributes = get_podcast_attributes(creator_name)
    podcast_title = json_dict['title']
    del json_dict['title']

    html = list(PRE_S)
    html.append(create_html_title(podcast_title, attributes['image_url'])) # TODO need to find way to get podcast thumbnails

    for k, v in json_dict.items():
        html.append('\n\n<div class="text-block">')
        html.append(f"\n<a href='{attributes['youtube_url']}'>{v['timestamp']}</a>")
        html.append(f"\n<b>[{v['speaker']}]</b> {v['text']}\n") #voice
        html.append('</div>')
        
    html.append(POST_S)
    s = "".join(html)

    output_path_html = f"./data/{creator_name}/html/{podcast_title}.html"
    #output_html_path = podcast_series_folder + "/html/" + podcast_title + ".html"
    #output_path_html = path.replace("mp3","html")
    with open(output_path_html, "w", encoding="utf-8") as text_file:
        text_file.write(s)
    print("Done converting JSON to html")
    return


def create_json(transcription: list, path:str):
    """create json file from transcription list"""
    creator_name = path.split("/")[-4]
    podcast_title = path.split("/")[-1].replace(".mp3","")
    json_transcription_file = {"title": str(podcast_title)}

    for idx, (seg, spk, sent) in enumerate(transcription):
        timestamp = seconds_to_timestamp(seg.start)
        json_transcription_file[idx] = {"speaker": spk,
                        "timestamp": timestamp,
                        "text": sent}
    
    condensed_json = condense_json_texts(json_transcription_file)

    output_path_json = f"./data/{creator_name}/json/{podcast_title}.json"
    #output_path_json = path.replace("mp3","json")

    with open(output_path_json, 'w') as json_file:
        json.dump(condensed_json, json_file, indent=4)  # Indent for readability
    
    print("Done converting to JSON")
    return condensed_json


def format_timestamp(timestamp):
    parts = timestamp.split(":")
    if len(parts) == 2:  # Only minutes and seconds are present
        formatted_timestamp = f"00:{parts[0]}:{parts[1]}.000"
    else:  # Hour, minutes, and seconds are present
        formatted_timestamp = f"{parts[0]}:{parts[1]}:{parts[2]}.000"
    return formatted_timestamp


def correct_txt(text, correction_dict:dict=REPLACEMENT_DICT):
    # Sort keys by length in descending order to match longer words first
    sorted_corrections = sorted(correction_dict.keys(), key=len, reverse=True)
    def replace(match):
        word = match.group(0)  # Get the matched word
        return correction_dict[word]  # Return the corrected word
    
    # Build a regular expression pattern that matches any of the incorrect words
    pattern = r'\b(' + '|'.join(re.escape(word) for word in sorted_corrections) + r')\b'
    corrected_text = re.sub(pattern, replace, text)
    return corrected_text


def txt_to_json(input_file_path:str):#, podcast_series_folder:str):
    """Parses a transcript from a text file into a dictionary and saves it as a JSON file."""
    
    creator_name = input_file_path.split('/')[-3]
    podcast_title = input_file_path.split("/")[-1].replace(".txt","")
    output_path_json = f"./data/{creator_name}/json/{podcast_title}.json"

    #output_json_path = podcast_series_folder + "/json/" + podcast_title + ".json"

    transcript_dict = {}
    transcript_dict['title']= podcast_title

    with open(input_file_path, 'r', encoding='utf-8') as file: # Load .txt file
        content = file.read()
    content = correct_txt(content) # Correct transcription errors

    # Define REGEX pattern for extracting: Speaker, timestamp, content
    entry_pattern = re.compile(r'\[Speaker (\d+) (\d+:?\d+:\d+)\]\s*(.*?)(?=\n\n|\Z)', re.DOTALL)
    entries = entry_pattern.findall(content)

    for i, (speaker_number, timestamp, text) in enumerate(entries):
        # Preprocess and format the timestamp and text
        formatted_timestamp = format_timestamp(timestamp)
        formatted_text = text.strip().replace("\n", " ")

        # Add the entry to the dictionary
        transcript_dict[str(i)] = {
            "speaker": f"Speaker {speaker_number}",
            "timestamp": formatted_timestamp,
            "text": formatted_text}

    # Save the dictionary as a JSON file
    with open(output_path_json, 'w', encoding='utf-8') as json_file:
        json.dump(transcript_dict, json_file, indent=4, ensure_ascii=False)
    
    print("Done converting txt to json")
    return transcript_dict


def create_html(transcription: list, path:str):
    """Creates an html page from the transcription list"""
    creator_name = path.split('/')[-4]
    html = list(PRE_S)
    podcast_title = path.split("/")[-1].replace(".mp3","")
    json_transcription_file = {"title": str(podcast_title)}

    for idx, (seg, spk, sent) in enumerate(transcription):
        timestamp = seconds_to_timestamp(seg.start)
        json_transcription_file[idx] = {"speaker": spk,
                        "timestamp": timestamp,
                        "text": sent}
        
        html.append('\n\n<div class="text-block">')
        html.append(f"\n<a href='https://www.youtube.com/@HamiltonMorris'>{timestamp}</a>")
        html.append(f'\n<b>[{spk}]</b> {sent}\n') #voice
        html.append('</div>')

    html.append(POST_S)
    s = "".join(html)

    output_path_html = f"./data/{creator_name}/html/{podcast_title}.html"
    output_path_json = f"./data/{creator_name}/json/{podcast_title}.json"
    #output_path_html = path.replace("mp3","html")
    #output_path_json = path.replace("mp3","json")

    with open(output_path_json, 'w') as json_file:
        json.dump(json_transcription_file, json_file, indent=4)  # Indent for readability

    with open(output_path_html, "w") as text_file:
        text_file.write(s)
    print("Done")