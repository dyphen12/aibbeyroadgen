"""

core.py

This module contains the core functions for the Aibbey Road project.

"""


import ctypes.util
orig_ctypes_util_find_library = ctypes.util.find_library
def proxy_find_library(lib):
  if lib == 'fluidsynth':
    return 'libfluidsynth.so.1'
  else:
    return orig_ctypes_util_find_library(lib)
ctypes.util.find_library = proxy_find_library


import magenta
import note_seq
import tensorflow
import os
import random
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2

print('🎉 Done!')
print(magenta.__version__)
print(tensorflow.__version__)


def generate_midi_only(seed, bars):

    sample_seq = note_seq.midi_io.midi_file_to_note_sequence(seed)

    # Model options. Change these to get different generated sequences!

    # Initialize the model.
    print("Initializing Melody RNN...")
    try:
        bundle = sequence_generator_bundle.read_bundle_file('aibbeyroad/models/attention_rnn.mag')
    except:
        print('Model not found...')
        print('Downloading model bundle. This will take less than a minute...')
        note_seq.notebook_utils.download_bundle('attention_rnn.mag', 'aibbeyroad/models')
        bundle = sequence_generator_bundle.read_bundle_file('aibbeyroad/models/attention_rnn.mag')

    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map['attention_rnn'](checkpoint=None, bundle=bundle)
    melody_rnn.initialize()

    input_sequence = sample_seq  # change this to teapot if you want
    num_steps = 128  # change this for shorter or longer sequences
    temperature = 1.0  # the higher the temperature the more random the sequence.

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in input_sequence.notes)
                     if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
        start_time=last_end_time + seconds_per_step,
        end_time=total_seconds)

    # Ask the model to continue the sequence.

    sequence = melody_rnn.generate(input_sequence, generator_options)

    # print(sample_seq.notes)
    # twinkle_twinkle = music_pb2.NoteSequence()
    # Add the notes to the sequence.
    # twinkle_twinkle.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)

    for i in range(len(sample_seq.notes)):
        try:
            sequence.notes.remove(sequence.notes[i])
        except IndexError:
            continue

    #print(len(sequence.notes))

    sequences = []
    if bars != 1:
        sequences.append(sequence)
        for k in range(bars):
            sequencex = melody_rnn.generate(input_sequence, generator_options)
            for j in range(len(sample_seq.notes)):
                            #print(j)
                            try:
                                sequencex.notes.remove(sequencex.notes[j])
                            except IndexError:
                                continue

            sequences.append(sequencex)

        sequence=note_seq.concatenate_sequences(sequences)



    note_seq.plot_sequence(sequence)
    # note_seq.play_sequence(sequence, synth=note_seq.fluidsynth)

    a = random.randint(0, 9000)

    fname = 'generated_song_' + str(a) + '.mid'

    relpath = 'aibbeyroad/generated/' + fname

    note_seq.sequence_proto_to_midi_file(sequence, relpath)

    abpath = os.path.abspath(relpath)

    #print(abpath)

    return abpath, fname

def generate_midi_for_web(seed, bars):

    sample_seq = note_seq.midi_io.midi_file_to_note_sequence(seed)

    # Model options. Change these to get different generated sequences!

    # Initialize the model.
    print("Initializing Melody RNN...")
    try:
        bundle = sequence_generator_bundle.read_bundle_file('aibbeyroad/models/attention_rnn.mag')
    except:
        print('Model not found...')
        print('Downloading model bundle. This will take less than a minute...')
        note_seq.notebook_utils.download_bundle('attention_rnn.mag', 'aibbeyroad/models')
        bundle = sequence_generator_bundle.read_bundle_file('aibbeyroad/models/attention_rnn.mag')

    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map['attention_rnn'](checkpoint=None, bundle=bundle)
    melody_rnn.initialize()

    input_sequence = sample_seq  # change this to teapot if you want
    num_steps = 128  # change this for shorter or longer sequences
    temperature = 1.0  # the higher the temperature the more random the sequence.

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in input_sequence.notes)
                     if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
        start_time=last_end_time + seconds_per_step,
        end_time=total_seconds)

    # Ask the model to continue the sequence.

    sequence = melody_rnn.generate(input_sequence, generator_options)

    # print(sample_seq.notes)
    # twinkle_twinkle = music_pb2.NoteSequence()
    # Add the notes to the sequence.
    # twinkle_twinkle.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)

    for i in range(len(sample_seq.notes)):
        try:
            sequence.notes.remove(sequence.notes[i])
        except IndexError:
            continue

    #print(len(sequence.notes))

    sequences = []
    if bars != 1:
        sequences.append(sequence)
        for k in range(bars):
            sequencex = melody_rnn.generate(input_sequence, generator_options)
            for j in range(len(sample_seq.notes)):
                            #print(j)
                            try:
                                sequencex.notes.remove(sequencex.notes[j])
                            except IndexError:
                                continue

            sequences.append(sequencex)

        sequence=note_seq.concatenate_sequences(sequences)



    note_seq.plot_sequence(sequence)
    # note_seq.play_sequence(sequence, synth=note_seq.fluidsynth)

    a = random.randint(0, 9000)

    fname = seed.replace('preprocess', 'generated')

    relpath = 'aibbeyroad/generated/' + fname

    fname = fname.replace('seeds','generated')

    note_seq.sequence_proto_to_midi_file(sequence, fname)

    abpath = os.path.abspath(relpath)

    print(abpath)

    return abpath, fname

def generate_midi(seed):

    print('generating song')

    sample_seq = note_seq.midi_io.midi_file_to_note_sequence(seed)
    #print(type(sample_seq))

    # This is a colab utility method that visualizes a NoteSequence.
    #note_seq.plot_sequence(sample_seq)

    # This is a colab utility method that plays a NoteSequence.
    #note_seq.play_sequence(sample_seq, synth=note_seq.fluidsynth)

    # Model



    # Import dependencies.
    from magenta.models.melody_rnn import melody_rnn_sequence_generator
    from magenta.models.shared import sequence_generator_bundle
    from note_seq.protobuf import generator_pb2
    from note_seq.protobuf import music_pb2

    # Initialize the model.
    print("Initializing Melody RNN...")
    try:
        bundle = sequence_generator_bundle.read_bundle_file('aibbeyroad/models/attention_rnn.mag')
    except:
        print('Model not found...')
        print('Downloading model bundle. This will take less than a minute...')
        note_seq.notebook_utils.download_bundle('attention_rnn.mag', 'aibbeyroad/models')
        bundle = sequence_generator_bundle.read_bundle_file('aibbeyroad/models/attention_rnn.mag')

    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map['attention_rnn'](checkpoint=None, bundle=bundle)
    melody_rnn.initialize()

    print('🎉 Done!')

    # Model options. Change these to get different generated sequences!

    input_sequence = sample_seq  # change this to teapot if you want
    num_steps = 128  # change this for shorter or longer sequences
    temperature = 1.0  # the higher the temperature the more random the sequence.

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in input_sequence.notes)
                     if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
        start_time=last_end_time + seconds_per_step,
        end_time=total_seconds)
    print('Generating Sequence')
    # Ask the model to continue the sequence.
    sequence = melody_rnn.generate(input_sequence, generator_options)

    #note_seq.plot_sequence(sequence)
    #note_seq.play_sequence(sequence, synth=note_seq.fluidsynth)

    a=random.randint(0,9000)

    fname = seed.replace('preprocess','generated')

    relpath = 'aibbeyroad/generated/'+fname

    note_seq.sequence_proto_to_midi_file(sequence, fname)

    abpath = os.path.abspath(relpath)

    print(abpath)

    return abpath, fname



