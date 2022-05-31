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

[Google Cloud Libraries](https://cloud.google.com/python/docs/setup)
[pyttsx3](https://github.com/nateshmbhat/pyttsx3)
[gpiozero](https://gpiozero.readthedocs.io/en/stable/)
[Transformers](https://huggingface.co/docs/transformers/index)
[feedparser](https://github.com/kurtmckee/feedparser)
[pytz](https://pypi.org/project/pytz/)
[Newspaper3k](https://newspaper.readthedocs.io/en/latest/)
[MySQL Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)
[pygame](https://www.pygame.org/)

Each of these libraries is straightforward to install with the exception of Transformers and to a lesser degree the Google Cloud Libraries. 

Transformers requires PyTorch which is a bit tricky to install on a Pi, but I followed these [instructions](https://medium.com/secure-and-private-ai-writing-challenge/a-step-by-step-guide-to-installing-pytorch-in-raspberry-pi-a1491bb80531), and was able to get it to work. 

With Google Cloud Text to Speech, you have to have a Google Cloud account, and you have to set up the credentials in a JSON file on your Pi. Google has provided [some instructions](https://medium.com/secure-and-private-ai-writing-challenge/a-step-by-step-guide-to-installing-pytorch-in-raspberry-pi-a1491bb80531), but it is a bit of a convoluted process. Also note that Google Cloud Text to Speech is not free. You can do alot with their free account level, but ultimately it is a paid service. 



