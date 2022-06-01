# Newsomatic

![Newsomatic](https://stuartduncan.ca/newsomaticBanner.jpg)

The Newsomatic is a prototype that is designed to explore the changing physicality of news consumption and the lack of user agency in algorithmic digital journalism distribution through the development of an audio-based digital news device. Created using a single board computer, a custom enclosure, and by embracing physical computing approaches, a prototype of a digital audio device was created that allows for users to control the content of an audio-based news bulletin using tactile knobs and buttons. 

This project was built using a Raspberry Pi 4B with 4GBs of memory. Connected to the Pi via its GPIO pins are 5 potentiometers and a button. The connections between the GPIO pins and the button and knobs are made via a mini-solderless breadboard, and a combination of Dupont style and soldered connections. As the Pi doesn’t have the capability to process analog inputs, an MCP3008 analog-to-digital converter chip was used to read the analog values from the potentiometers. Please see the list below for all of the items required for this project. 

A custom laser cut case was created for this project, which was used to house the Pi and the mini-breadboard, and serve as a mount for the knobs and button. 

The programming for this project was done using the Python programming language. Three Python scripts were created for this project, and serve as the functional brain of the Newsomatic: 1) the article grabber (readRSS.py), 2) the article summarizer (summarize.py) and 3) the newscast creator (createNews.py).  

The article grabber script reads news article website addresses from user defined RSS feeds, scrapes the article information and stores that information in a MySQL database. The article summarizer script uses the Transformers Python library to automatically create a summary of those articles, and stores that summary in a database on the Pi. Finally, the newscast creator script senses when the button is pressed, reads the values of the knobs, and creates a text radio script based on those values. Each knob is dedicated to one subject matter, in the case of my example: Canada, world, business, sports and politics. If you turn a knob clockwise, you will get more of that subject in your news bulletin. The text script is converted to an audio newscast using either Google Cloud Text-to-Speech or the pyttsx3 Python library and played over a speaker connected to the Pi. More details on the scripts included in this repository are available below. 

* For more background on this project, watch a [YouTube video](https://youtu.be/9qo_R_hOarE) which further explains how the Newsomatic works. Also [watch a simple demo](https://youtu.be/81uKX2uwyas) of the Newsomatic in action.*

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

### Potentiometers

For this project I used five 3-pin linear rotary potentiometers, with varying resistor values. The kit that I purchased from Amazon included the potentiometers, plastic knobs, nuts and washers. To work with my case design, I had to file down the little metal tab that protrudes the potentiometers. 

### Button

Any button that allows you to connect an input and ground to it should be fine for this project. I first used a [small button](https://www.pishop.ca/product/tactile-button-switch-6mm-20-pack/) that included with many electronics kits  but I found this style of button challenging to properly mount to my case, and switched to an [“arcade style” button](https://www.amazon.ca/gp/product/B07FKB6648) which worked far better. 

### Connections

This prototype is reliant on MCP3008 to convert the analog signals from the potentiometers to digital signals that can be read by the Pi. This great tutorial and video from [Robotica DIY](https://roboticadiy.com/potentiometer-analog-input-for-the-raspberry-pi-4/), outlines how to connect the potentiometers to the Pi. 

In broad strokes, using Dupont female to male connectors, you connect pins 9 to 16 on the MCP3008 to specific GPIO pins on the Pi. Each pin 1 to 8, on the MCP3008 acts as an analog input reading in values from the potentiometers. One pin on the potentiometer is connected to ground, the middle pin is connected to an input channel of the MCP3008 and the other pin is connected to the 3v3 power from the Pi. 

For the button, one pin of the button is connected to a general GPIO pin (in my case GPIO 4) and the other pin is connected to ground. The Raspberry Pi site has a [simple tutorial](https://projects.raspberrypi.org/en/projects/physical-computing/5)that further explains this process.

### Configuring MySQL (and optionally Apache and PHP)

This project uses a MySQL database and would require Apache and PHP if you would like to use phpMyAdmin to administer the database. I followed this great tutorial from [Random Nerd Tutorials](https://randomnerdtutorials.com/raspberry-pi-apache-mysql-php-lamp-server/) to configure MySQL, Apache, PHP and phpMyAdmin on the Pi. A sample database structure, and test data is included in this repository. 

### Required Python Libraries 

This project requires several Python libraries including:

- [Google Cloud Libraries](https://cloud.google.com/python/docs/setup)
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- [gpiozero](https://gpiozero.readthedocs.io/en/stable/)
- [Transformers](https://huggingface.co/docs/transformers/index)
- [feedparser](https://github.com/kurtmckee/feedparser)
- [pytz](https://pypi.org/project/pytz/)
- [Newspaper3k](https://newspaper.readthedocs.io/en/latest/)
- [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)
- [pygame](https://www.pygame.org/)

Each of these libraries is straightforward to install with the exception of Transformers and to a lesser degree the Google Cloud Libraries. 

Transformers requires PyTorch which is a bit tricky to install on a Pi, but I followed these [instructions](https://medium.com/secure-and-private-ai-writing-challenge/a-step-by-step-guide-to-installing-pytorch-in-raspberry-pi-a1491bb80531), and was able to get it to work. 

With Google Cloud Text to Speech, you have to have a Google Cloud account, and you have to set up the credentials in a JSON file on your Pi. Google has provided [some instructions](https://medium.com/secure-and-private-ai-writing-challenge/a-step-by-step-guide-to-installing-pytorch-in-raspberry-pi-a1491bb80531), but it is a bit of a convoluted process. Also note that Google Cloud Text to Speech is not free. You can do alot with their free account level, but ultimately it is a paid service. 

### Project File Overview

**config.ini** - This project can be configured by altering the values in this file. Within the [config] section you can specify the number of RSS feeds you would like to read into your database, the number of items you would like to have in your audio newscast, which text to speech method you would like to use (google or pyttsx3), and the GPIO pin that your button is connected to. The [google] section you can specify a path to your Google Cloud text-to-speech (TTS) credentials file, and also the language code and language name that you would like Google TTS to use. The [database] section would contain all the details required to connect to your database. In this section you will need to specify your database host, name, user, password, and port. There are also entries for all of the RSS feeds you would like to read news article data from. You can enter any number of feeds, but each of these sections must be named as [feedNumber], so feed1, feed2, feed3, feed4 etc. These individual items feature value for the url of the feed, the section name of the feed, and the MCP3008 channel number the potentiometer for that feed is connected to. 

**readRSS.py** - This script reads the RSS feeds specified in the config file, scrapes the article information using the Newspaper 3k python library, and stores the information in the MySQL database. 

**summarize.py** - The script queries the MySQL database, determines which articles do not have summaries, creates a short summary of those articles using the Transformers Python library, and adds these summaries to the MySQL database. Due to the limited processing power of the Pi, this script takes a while to run. It usually takes a minute or two to summarize an article. When this script is running, the Pi also gets pretty hot. 

**createNews.py** : The script listens for a press of the button. When the button is pressed, this script reads the values of the potentiometers, creates a text based script for a news bulletin using the articles summaries based upon the values of the potentiometers, uses text-to-speech (either Google or pyttsx3) to create an MP3 of the news bulletin, and then plays that MP3 over speakers connected to the Pi via the audio Jack. 

### Running the Scripts 

On the Raspberry Pi, I set the readRSS.py and summarize.py scripts to run automatically every hour as a cron job. I run the summarize.py file 15 minutes after the readRSS.py file. The post from [BC Robotics](https://bc-robotics.com/tutorials/setting-cron-job-raspberry-pi/) provides a good background on how to set up cron jobs on the Pi. I still manually run the createNews.py script, usually by connecting to the Pi via an SSH client, but the Pi could be configured to run the script on boot up. 

### Laser Cut Case

For this project, I created a custom laser cut case to house the Pi and the breadboard, and also serve as a mount for the button and knobs. I created a laser cut case instead of a 3d printed case, as the process seemed simpler and it was more affordable. I made my case out of black acrylic. The Pi is mounted to the case using four M2.5 standoffs. You may want to mount or attach the mini breadboard to your case, but it was helpful being able to easily remove it from the case when making connections, and it didn’t seem to move around much, even though it was attached to the case. My case is held together using t-slots and M3 screws. I felt this worked better than gluing or cementing the case together, as I could remove the sides of the case for easier access. There are holes in the sides of the case to allow access to the USB and network connections, and the HDMI, USB-C power and audio jacks. 

## Future Work

This prototype is very much a work in progress and there are elements of its implementation that could definitely use improvement. I would like to create a bit more of a complex text based script for the news bulletin. I would also like a future version of the prototype to incorporate some type of display to provide some feedback to the user. I also do not like how hot the Pi gets when summarizing the article text, and I might investigate using some form of cloud based solution that wouldn’t tax the Pi as much. That being said I am also a bit torn by the use of cloud based computing in this project, and might examine other free text-to-speech platforms that might produce better results than pyttsx3. 




