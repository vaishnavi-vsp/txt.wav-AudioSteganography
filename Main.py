import wave
import AudioParse
import AudioSteganography


def main():
    audio = wave.open("TheMoonLanding.wav", "r")
    list = AudioParse.parseFrames(audio)
    samplerate = audio.getframerate()
    encodedAudio = AudioSteganography.encode(list, "test.txt")
    AudioParse.writeNewWave(encodedAudio, samplerate, "new.wav")
    audio.close()

    encodedAudio = wave.open("new.wav", "r")
    newlist = AudioParse.parseFrames(encodedAudio)
    secretMessage = AudioSteganography.decode(newlist, "secret.txt")
    print(secretMessage)
    encodedAudio.close()


main()
