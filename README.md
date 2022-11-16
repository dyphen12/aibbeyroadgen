
# Music Generator  
  
Generate music with artificial intelligence.  
  
## Installation  
  
### Requirements  
  
- Ubuntu 18.06 or Higher  
- Python 3.7 (Does not work on Python 3.10)  

## Build & Run
  
### Docker  (Flask API):

     $ sudo docker compose build 
     $ sudo docker compose up -d

  
### Virtual Environment:

     $ sudo apt-get install build-essential libasound2-dev libjack-dev portaudio19-dev -y sl  
     $ sudo apt-get install libsndfile1 -y sl 
     $ sudo apt install -y fluidsynth 
     $ sudo pip install --no-cache-dir -r requirements.txt  
     $ python application.py

 
## Run  

### Docker:

    $ sudo docker compose up -d

  
### Flask API:

    $ python application.py

### Anvil Web App :

 

    $ python anvilapp.py 


### As Package:
  

     from aibbeyroad import core 
 
     core.generate_midi('seeds/TearsInHeaven.mid')   
     core.generate_midi_only('seeds/I-want-to-hold-your-hand.MID',4)  


### Flask API:  Upload MIDI with CURL

#### Direct Download

    $ curl -X POST -F file=@"your_seed_name_here.mid" http://localhost:5000/upload-midi --output your_generated_midi_name_here.mid

#### AWS S3 Bucket

    $ curl -X POST -F file=@"your_seed_name_here.mid" http://localhost:5000/process-midi



## Anvil Front-end  
  
To route to your Anvil Web App just change the API code on **anvilapp.py**  
  
Example: **anvilapp.py**  
  

     from aibbeyroad import core    from midi2audio import FluidSynth    
     import anvil.server    
     import anvil.media    
     import random    
     import io  
      
     anvil.server.connect("your-key-here")  

### AWS Endpoint

#### Download AWS CLI and configure your user

Set up the AWS command-line tool because it makes authentication so much easier.

Open the terminal, then, type `aws configure`
  
Insert your AWS Key ID and Secret Access Key, along with the region you created your bucket in (use the CSV file). You can find the region name of your bucket on the S3 page of the console.

Now you can upload your files directly to the s3 bucket.

## Docs  

### API Endpoints

| HTTP Request |  Address      | Query Params | Response       | Description                                                                                |
|--------------|---------------|--------------|----------------|--------------------------------------------------------------------------------------------|
|     POST     | /process-midi | seed.mid     | Uploaded to S3 | Uploads .mid file to process and uploads a "generated midi" to folder in a S3 Bucket                      |
|     POST     | /upload-midi  | seed.mid     | generated.mid  | File Attachment, Uploads .mid file to process and returns the generated midi to download |
|              |               |              |                |                                                                                            |

### aibbeyroad.core  
  
 *Function* **generate_midi(_filename_):**   
   
 Parameters:  
  
-   **filename** (_str_) – Filename or Filepath.  
  
  
 *Function* **generate_midi_only(_filename_, _bars_):**   
   
 Parameters:  
   
-   **filename** (_str_) – Filename or Filepath.  
-   **bars** (_int_) – Number of bars (Length or Compases)