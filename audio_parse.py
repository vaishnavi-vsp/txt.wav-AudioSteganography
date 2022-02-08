import wave
import struct
import sys

def getAudioInfo(audio):
    #takes in opened wave-object and prints out information about the .wav
    print("Samples in the file: ", audio.getnframes())
    print("Sampling rate of the file: ", audio.getframerate())
    print("Sampling width of file (bits per file: output*8):", audio.getsamplewidth())
    length = round(int(audio.getnframes()) / int(audio.getframerate()), 3)
    print("Length in seconds of the file:", length, "seconds")

def parseFrames(audio):
    #takes in opened wave-object, determines number of frames, then creates a list of integers that represent each sample of the audio
    length = audio.getnframes()
    audioFrames = []
    for i in range(0, length):
        frame = audio.readframes(1)
        data = struct.unpack("<h", frame)
        audioFrames.append(data[0])
    #clears variable memory
    del length
    #returns list of audio points
    return audioFrames

def writeNewWave(list, sr, name):
    #takes a list of integers that represent signed 16-bit wave samples and returns new wave-object of the written .wav file
    try:
        newWave = wave.open(name, "w")
        newWave.setnchannels(1)
        newWave.setsampwidth(2)
        newWave.setframerate(sr)
        newWave.setnframes(len(list))
        for items in list:
            byteType = struct.pack('<h', items)
            newWave.writeframes(byteType)
        newWave.close()
        #clears list and variable memory
        del list, sr, name
        #returns new wav-object
        return newWave
    except:
        print("Error opening or naming file, check name and directory.")
        sys.exit(-1)