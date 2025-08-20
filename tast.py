import sys
from rich import print
from time import sleep

def type_text(text, delay):
    
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print()

def print_lyrics():

    lines = [
        ("I wanna da-", 0.06),
        ("I wanna dance in the lights", 0.05),
        ("I wanna ro-", 0.07),
        ("I wanna rock your body", 0.08),
        ("I wanna go", 0.08),
        ("I wanna go for a ride", 0.068),
        ("Hop in the music and", 0.07),
        ("Rock your body", 0.08),
        ("Rock that body", 0.069),
        ("Come on, come on", 0.035),
        ("Rock that body", 0.05),
        ("Rock your body", 0.03),
        ("Rock that body", 0.049),
        ("Come on, come on", 0.035),
        ("Rock that body", 0.08)
    ]

    for text, char_delay in lines:
        type_text(text, char_delay)
        sleep(0.2)

if __name__ == "__main__":
    print_lyrics()
