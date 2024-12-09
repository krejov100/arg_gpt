# Functions must be documented using demonstrated style
import arg_gpt
import os
from arg_gpt.ai_func import ai_func

@ai_func
def get_sky_color(time_of_day: str):
    """returns the color of the sky, based on the time of day
    Arguments:
        time_of_day: time of day, either day or night
    """
    if time_of_day == "day":
        return "blue"
    elif time_of_day == "night":
        return "black"
    else:
        return "unknown"

@ai_func
def call_commands(commands: list[str]):
    """
    Iterates through and calls each command from a list of Unix commands.
    CAUTION: This function will execute the commands passed to it.

    Arguments:
        commands: A list of strings, each representing a Unix command.
    """
    for command in commands:
        print(command)
        os.system(command)

@ai_func
def hello_world(append_string):
    """prints hello world with an appended string
    Arguments:
        append_string: string to append to hello world
    """

    return "Hello World!" + append_string


@ai_func
def spell_word(word: str):
    """spell a word, separating each letter with -
    Arguments:
        word: word to spell
    """
    return "-".join(word)


@ai_func
def get_time_date():
    """returns the current time and date
    Arguments:
        None
    """
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@ai_func
def get_weather(location: str = ""):
    """Gets the current weather information using a web browser
    Arguments:
        location: Optional location to get weather for. If not provided, will attempt to get local weather.
    """
    import webbrowser
    if location:
        url = f"https://www.google.com/search?q=weather+in+{location}"
    else:
        url = "https://www.google.com/search?q=weather"
    webbrowser.open(url)
    return f"Opening weather information for {location if location else 'your location'}"
