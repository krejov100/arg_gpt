# Functions must be documented using demonstrated style
import arg_gpt


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

def call_commands(commands: list[str]):
    """
    Iterates through and calls each command from a list of Unix commands.

    Arguments:
        commands: A list of strings, each representing a Unix command.
    """
    for command in commands:
        print(command)


def hello_world(append_string):
    """prints hello world with an appended string
    Arguments:
        append_string: string to append to hello world
    """

    return "Hello World!" + append_string


def spell_word(word: str):
    """spell a word, separating each letter with -
    Arguments:
        word: word to spell
    """
    return "-".join(word)


def get_time_date():
    """returns the current time and date
    Arguments:
        None
    """
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")