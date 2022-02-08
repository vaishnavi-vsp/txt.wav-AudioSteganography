import sys

"""""
Audio Manipulation is a library created to provide tools to hide messages inside of audio files. This library works
in conjunction with the AudioParse library to take lists of audio information from a 16-bit .wav file, and then
encode or decode information in it. 
"""""

class InputFile:
    # This class is designed to open an existing text file as defined by the user. It determines the amount
    # of bytes and bits that make up the contents of the file. It opens the file in a read-only mode. It
    # stores the name given to the file, a list of characters that make up the list, and a list of integers
    # that correspond to the ASCII values of these characters.
    

    def __init__(self, filename):
        self.totalBits = 0
        self.totalBytes = 0
        self.charlist = []
        self.intlist = []
        self.filestr = ""
        self.filename = filename
        self.openfile()

    # opens the file, throwing an exception if this fails,
    # calls the two other functions to set the parameters of the class.
    # The file is read and a list of characters is created for charlist[]   
    def openfile(self):
        try:
            file = open(self.filename, "r")
            for item in file.read():
                self.charlist.append(item)
            self.charlist.append(None)
            self.totalBits, self.totalBytes = self.calculateBitsAndBytes()
            file.close()
            file = open(self.filename, "r")
            self.filestr = file.read()
            file.close()
            self.createIntList()
        except:
            print("Could not create file, check file name or that file is in current directory.")
            print("Exiting program.")
            sys.exit()

    # takes the charlist[] and increments the totalBits and totalBytes variable to
    # define the contents of the data.
    def calculateBitsAndBytes(self):
        bit = 0
        byte = 0
        for i in range(len(self.charlist)):
            bit += 8
            byte += 1
        return bit, byte

    # takes the charlist[] and makes a new list in the class called intolist[] that is
    # essentially a copy of char list but with the char values converted to their ASCII integer form.
    def createIntList(self):
        intlist = []
        for i in range(len(self.charlist)-1):
            intlist.append(ord(self.charlist[i]))
        intlist.append(0)
        self.intlist = intlist


def encode(list, textfile):
    file = InputFile(textfile)
    encodedAudio = []
    audioNum = 0
    if len(list) >= file.totalBits:
        # for every character in the textfile
        for val in file.intlist:
            # for every bit in the character
            for i in range(7, -1, -1):
                # encode bit from left to right into the audio bytes
                bitToEncode = readBit(val, i)
                if list[audioNum] != abs(list[audioNum]):
                    negative = True
                else:
                    negative = False
                newVal = writeBit(abs(list[audioNum]), bitToEncode)
                if negative == True:
                    encodedAudio.append(-1*newVal)
                else:
                    encodedAudio.append(newVal)
                audioNum += 1

        return encodedAudio + list[audioNum:]
    else:
        print("Not enough samples to encode message in.")
        sys.exit(-1)

def decode(list, newfilename):
    bitlist = []
    for bits in list:
        bitlist.append(readBit(abs(bits), 0))
    potentialBytes = determineTotalBytes(bitlist)
    newByte = ""
    endByte = False
    counter = 0
    message = []
    for i in range(potentialBytes):
        if counter < 8 and endByte == False:
            newByte += str(bitlist[i])
            counter += 1
        elif counter >= 8:
            character = int(newByte, 2)
            if(character == 0):
                endByte = True
            message.append(chr(character))
            newByte = ""
            newByte += str(bitlist[i])
            counter = 0
            counter += 1
        elif endByte == True:
            strMessage = ""
            for characters in message:
                strMessage += characters
            writeMessageToFile(strMessage, newfilename)
            return strMessage

    print("No message found in signal (No sentinel encountered).")
    print("Returning string and file of random bytes found in message.")
    garbage = ""
    for things in message:
        garbage += things
    return garbage

def writeMessageToFile(message, filename):
    try:
        newtext = open(filename, "w")
        newtext.write(message)
        newtext.close()
    except:
        print("Unable to open and write to file. Check file name and extension.")
        sys.exit()
    return

def determineTotalBytes(list):
    return int(len(list) / 8)

def writeBit(integer, boolean):
    if boolean == True:
        value = integer | 0x01
    else:
        value = integer & ~0x01
    return value

def readBit(integer, position):
    return ((0x01 << position) & abs(integer)) >> position
