# Newsomatic

The Newsomatic is a prototype that is designed to explore the changing physicality of news consumption and the lack of user agency in algorithmic digital journalism distribution through the development of an audio-based digital news device. Created using a single board computer, a custom enclosure, and by embracing physical computing approaches, a prototype of a digital audio device was created that allows for users to control the content of an audio-based news bulletin using tactile knobs and buttons. 

This project was built using a Raspberry Pi 4B with 4GBs of memory. Connected to the Pi via its GPIO pins are 5 potentiometers and a button. The connections between the GPIO pins and the button and knobs are made via a mini-solderless breadboard, and a combination of Dupont style and soldered connections. As the Pi doesn’t have the capability to process analog inputs, an MCP8000 analog-to-digital converter chip was used to read the analog values from the potentiometers. Please see the list below for all of the items required for this project. 

A custom laser cut case was created for this project, which was used to house the Pi and the mini-breadboard, and serve as a mount for the knobs and button. 

The programming for this project was done using the Python programming language. Three Python scripts were created for this project, and serve as the functional brain of the Newsomatic: 1) the article grabber (readRSS.py), 2) the article summarizer (summarize.py) and 3) the newscast creator (createNews.py).  

The article grabber script reads news article website addresses from user defined RSS feeds, scrapes the article information and stores that information in a MySQL database. The article summarizer script uses the Transformers Python library to automatically create a summary of those articles, and stores that summary in a database on the Pi. Finally, the newscast creator script senses when the button is pressed, reads the values of the knobs, and creates a text radio script based on those values. Each knob is dedicated to one subject matter, in the case of my example: Canada, world, business, sports and politics. If you turn a knob clockwise, you will get more of that subject in your news bulletin. The text script is converted to an audio newscast using either Google Cloud Text-to-Speech or the pyttsx3 Python library and played over a speaker connected to the Pi. More details on the scripts included in this repository are available below. 

## Physical Requirements: 

- Raspberry Pi 4B with a MicroSD card and USB-C power supply
- Breadboard 
- MCP3008 analog-to-digital converter
- Dupont connectors - both female-to-male and male-to-male 
- Potentiometers 
- A button

## More Background:

### Raspberry Pi 4B

For this project I used the Pi 4B model with 4GB of memory. This was mostly because at the time of starting this project, models with 8GB were not available. This project could potentially work with Pi models with less memory or older Pi models such as the 3, but the text summarizations done with the Transformers library are processor intensive, and would probably run much slower on older models. I installed the 64-bit version of Raspberry Pi OS (Bullseye) on the Pi, but this project would probably also work on 32-bit versions. The Pi used in this project uses a 32 GB SD card for storage, but smaller cards such as 8GB or 16GB should also be fine. The Pi I purchased only came with passive cooling, but the Pi gets pretty hot (8O’C) while doing the text summarization, so active cooling via a fan would probably work better. 

### Breadboard

For my final version of this project, I used a mini breadboard, so that I could fit the breadboard into my custom case, but any size breadboard would be fine. You could also use some form of prototyping board and solder most of the connections for this project. I wanted to be able to change my connections around a bit more, and I am not really great with soldering so I used mostly Dupont style connections. I soldered 22 gauge wire to the leads of the potentiometers and the button, but all other connections were made with Dupont cables. 



