
# Music Generator  
  
Generate music with artificial intelligence.  
  
## Installation  
  
### Requirements  
  
- Ubuntu 18.06 or Higher  
- Python 3.7 (Does not work on Python 3.10)  

## Build
  
### Docker  (Flask API):

     $ sudo docker build -t ${app} . 

  
### Virtual Environment:

     $ sudo apt-get install build-essential libasound2-dev libjack-dev portaudio19-dev -y sl  
     $ sudo apt-get install libsndfile1 -y sl 
     $ sudo apt install -y fluidsynth 
     $ sudo pip install --no-cache-dir -r requirements.txt  
     $ python application.py

 
## Run  

### Docker:

In order to upload to an AWS S3 Bucket, you need to add the following **environment variables** in **your docker run command**.

Example:

    $ docker run [container] -e AWS_ACCESS_KEY_ID=your-access-key \
    $ -e AWS_SECRET_ACCESS_KEY=your-secret-access-key \
    $ -e AWS_DEFAULT_REGION=your-default-region 
  
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

    $ curl -X POST -F file=@"your_seed_name_here.mid" http://localhost:5000/upload-midi-s3



## Anvil Front-end  
  
To route to your Anvil Web App just change the API code on **anvilapp.py**  
  
Example: **anvilapp.py**  
  

     from aibbeyroad import core    from midi2audio import FluidSynth    
     import anvil.server    
     import anvil.media    
     import random    
     import io  
      
     anvil.server.connect("your-key-here")  


## Docs  

### API Endpoints

| HTTP Request | Address         | Query Params | Response       | Description                                                                                |
|--------------|-----------------|--------------|----------------|--------------------------------------------------------------------------------------------|
|     POST     | /upload-midi-s3 | seed.mid     | Uploaded to S3 | Uploads .mid file to process and uploads a "generated midi" to folder in a S3 Bucket                      |
|     POST     | /upload-midi    | seed.mid     | generated.mid  | File Attachment, Uploads .mid file to process and returns the generated midi to download |
|              |                 |              |                |                                                                                            |

### aibbeyroad.core  
  
 *Function* **generate_midi(_filename_):**   
   
 Parameters:  
  
-   **filename** (_str_) – Filename or Filepath.  
  
  
 *Function* **generate_midi_only(_filename_, _bars_):**   
   
 Parameters:  
   
-   **filename** (_str_) – Filename or Filepath.  
-   **bars** (_int_) – Number of bars (Length or Compases)