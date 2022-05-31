from configparser import ConfigParser
from google.cloud import texttospeech
import pyttsx3
import os
from gpiozero import Button
from gpiozero import MCP3008

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import dbConnect

def createScript(dbCursor, dbConnection, config):

    knobList = []

    # for each feed find out the knob number, section and then get value from knob

    for x in range(1, int(config["config"]["feedCount"]) + 1):

        feedString = "feed" + str(x)
        section = config[feedString]["section"]
        knobNumber = config[feedString]["knob"]
        knobValue = getKnobValue(int(knobNumber))
        # append a dictionary to the knob info list
        knobList.append({"section":section, "knobValue": knobValue})

    print("Knob details: \n {} \n".format(knobList))

    # do some calculations to figure out how many of each subject should be in the script

    #cacluate the total values of all knob values
    sumOfValue = 0
    for knob in knobList:
        sumOfValue = sumOfValue + knob["knobValue"]

    # caluate the total amount of stories for each section
    totalItems = config["config"]["numberItems"]

    summaries = []

    for knob in knobList:

        # with rounding you can sometimes get an extra item
        sectionItems = round((knob["knobValue"] / sumOfValue) * float(totalItems))
        print("The total items for section {} is {}".format(knob["section"], sectionItems))
        # query the database to get the summaries based upon the calculations

        sql = "SELECT pubdate, summary FROM articles WHERE section = %s AND SUMMARY != '' ORDER BY pubdate DESC LIMIT %s"
        values = (knob["section"],sectionItems)
        dbCursor.execute(sql, values)
        articles = dbCursor.fetchall()

        # add each summary to the larger list of summaries
        for article in articles:
            summaries.append(article[1])

    # build the script by join all the summaries into one string
    # for Google TTS add a bit of SSML

    if(config["config"]["TTSmethod"] == "pyttsx3"):
        script = " ".join(summaries)
        makeMP3pyttsx3(script)
    elif(config["config"]["TTSmethod"] == "google"):
        script = "<break time='1.5s'/>".join(summaries)
        finalScript = "<speak>{}</speak>".format(script)
        makeMP3Google(finalScript,config)

    # play the mp3
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    print("Playing newscast now")

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def getKnobValue(knobNumber):

    knobInfo = MCP3008(knobNumber)
    return(knobInfo.value)

def makeMP3Google(script,config):

    os.environ ["GOOGLE_APPLICATION_CREDENTIALS"]= config["google"]["pathToGoogle"]

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=script)

    voice = texttospeech.VoiceSelectionParams(
        language_code=config["google"]["languageCode"],
        name=config["google"]["languageName"],
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)

def makeMP3pyttsx3(script):

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    engine.save_to_file(script,"output.mp3")
    engine.runAndWait()

# created a seperate function because the gpiozero button press is not great
# at sending parameters to a function

def startCreation():

    config = ConfigParser()
    config.read("config.ini")
    dbCursor, dbConnection = dbConnect.getDbConnection(config["database"])
    createScript(dbCursor, dbConnection, config)
    print("----------------------------------------------------------")
    print("Please press the button to build and play your newscast.")

def main():

    config = ConfigParser()
    config.read("config.ini")

    # define the button
    button = Button(int(config["config"]["buttonGPIO"]))

    print("Please press the button to build and play your newscast.")

    while True:
    	button.when_pressed = startCreation

if __name__ == "__main__":
    main()
