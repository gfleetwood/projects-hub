from google.cloud import texttospeech
from boilerpy3 import extractors # web article to text
import time
import fire

def tts_book(output_file_name, text_chunk, lang = 'en-US-Wavenet-B'):
  
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text = text_chunk)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code = lang,
        ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL
        )

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding = texttospeech.enums.AudioEncoding.MP3
        )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(output_file_name, 'ab') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        
    print("Audio content written to file")
    
    return(1)
    
def process_web_txt(url):
  
  extractor = extractors.ArticleExtractor()
  content = extractor.get_content_from_url(url)
  
  return(content)
  
def read_txt(file):
  
  with open(file, "r") as f:
    content = f.read()
    
  return(content)

def get_txt(txt_from_web, source):
  
  output_file_name = source.replace("txt", "mp3")
  content = process_web_txt(source) if txt_from_web else read_txt(source)
  
  chunks = []
  temp = content.replace("\n", " ")

  while len(temp) != 0:
    chunks.append(temp[:4000])
    temp = temp[4000:]

  for chunk in chunks:
    _ = tts_book(output_file_name, chunk)
    time.sleep(5)
    
if __name__ == "__main__":
  fire.Fire(get_txt)
