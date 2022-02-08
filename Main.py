import wave
import audio_parse
import audio_manipulation


def main():
    print("Analyzing audio...")
    audio = wave.open("sample_audio/TheMoonLanding.wav", "r")
    list = audio_parse.parseFrames(audio)
    samplerate = audio.getframerate()
    print("Encoding audio...")
    encodedAudio = audio_manipulation.encode(list, "test.txt")
    audio_parse.writeNewWave(encodedAudio, samplerate, "new.wav")
    audio.close()
    print("Audio encoded successfully. Check new.wav file generated.\n")
    input("Press enter to decode")
    print("\nDecoding audio...")
    encodedAudio = wave.open("new.wav", "r")
    newlist = audio_parse.parseFrames(encodedAudio)
    secretMessage = audio_manipulation.decode(newlist, "secret.txt")
    print("Audio decoded successfully. Check secret.txt file generated.")
    print("Decoded message: "+secretMessage)
    encodedAudio.close()
main()
