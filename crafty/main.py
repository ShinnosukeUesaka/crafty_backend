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
def transcribe_audio(file: UploadFile = File(...)):
    print(file)
    # audio_file= open("/path/to/file/audio.mp3", "rb")
    # transcript = client.audio.transcriptions.create(
    #     model="whisper-1", 
    #     file=audio_file
    # )
    # use the file to transcribe
    
    audio_file = file.file.read()
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
         file=audio_file
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
