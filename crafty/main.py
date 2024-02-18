import dotenv

dotenv.load_dotenv('crafty/.env', override=True)

from pathlib import Path
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# for audio transcription input, file
from fastapi import UploadFile, File
from pydantic import BaseModel
import json
from openai import OpenAI


from typing import Annotated


client = OpenAI()



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    
class ExampleInput(BaseModel):
    text: str

# audio transcription endpoint
@app.post("/transcribe")
def create_file(audio: UploadFile = File(...)):
    print(audio)
    # audio_file= open("/path/to/file/audio.mp3", "rb")
    # transcript = client.audio.transcriptions.create(
    #     model="whisper-1", 
    #     file=audio_file
    # )
    # use the file to transcribe
    print(audio.content_type)
    file = audio.file.read()
    # save file to disk
    with open("audio.webm", "wb") as f:
        f.write(file)
    # audio = AudioSegment.from_file("audio.ogg", format="ogg")
    # audio.export("outaudio.mp3", format="mp3") 
    file = open("audio.webm", "rb")
        
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
         file=file
    )
    transcribed_text = transcript.text
    
    return {"transcribed_text": transcribed_text}

# crafty endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate")
def generate(input: ExampleInput):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": 'return json {"message": "hi"}'},
        ],
        max_tokens=2000,
    )
    result = response.choices[0].message.content # this is json in string
    returned_dictionary =  json.loads(result)
    print(returned_dictionary)
    return returned_dictionary
