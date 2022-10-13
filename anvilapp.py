from aibbeyroad import core
from midi2audio import FluidSynth
import anvil.server
import anvil.media
import random
import io

anvil.server.connect("LFGKW7PAQ7IZHNOD5IIK3JFC-TA27YMSOYSMWWUBQ")

#core.generate_midi('seeds/TearsInHeaven.mid')
#core.generate_midi_only('seeds/I-want-to-hold-your-hand.MID',4)


@anvil.server.callable
def generate_midi_api(file, exportoption, bars):

    genname = 'preprocess-' + str(random.randint(1000, 9999)) + '-' + file.get_name()
    filegenname = 'seeds/'+ genname
    print(genname)


    #Save on /seeds
    mid_file = file
    with open(filegenname, 'wb') as saveMidFile:
        saveMidFile.write(mid_file.get_bytes())
        print('Downloaded {} successfully.'.format(file.get_name()))
        print(filegenname)

    #Send Seed from seeds folder

    try:
        core.generate_midi_for_web(filegenname,int(bars))
    except:
        return 'Invalid'

    gname = filegenname.replace('preprocess', 'generated')
    gname = gname.replace('seeds','generated')


    if exportoption == 'WAV':
        replacementStr = 'wav'
        # Replace last 3 characters in string with 'XXX'
        exportname = gname[:-3] + replacementStr

        # using the default sound font in 44100 Hz sample rate
        fs = FluidSynth()
        fs.midi_to_audio(gname, exportname)
        return anvil.media.from_file(exportname)


    return anvil.media.from_file(gname)


anvil.server.wait_forever()