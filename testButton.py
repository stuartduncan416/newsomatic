from gpiozero import Button


def startCreation():

    print("Button pressed.")

def main():

    button = Button(4)

    print("Please press the button.")

    while True:
    	button.when_pressed = startCreation

if __name__ == "__main__":
    main()
