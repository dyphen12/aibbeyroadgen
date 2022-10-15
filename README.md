
# Music Generator  
  
Generate music with artificial intelligence.  
  
## Installation  
  
### Requirements  
  
- Ubuntu 18.06 or Higher  
- Python 3.7 (Does not work on Python 3.10)  

## Build & Run
  
### Docker  (Flask API):

     $ sudo docker compose build $
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

    $ curl -X POST -F file=@"TearsInHeaven.mid" http://localhost:5000/upload-midi --output TearsInHeaven-generated.mid


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
  
### aibbeyroad.core  
  
 *Function* **generate_midi(_filename_):**   
   
 Parameters:  
  
-   **filename** (_str_) – Filename or Filepath.  
  
  
 *Function* **generate_midi_only(_filename_, _bars_):**   
   
 Parameters:  
   
-   **filename** (_str_) – Filename or Filepath.  
-   **bars** (_int_) – Number of bars (Length or Compases)