# Functions must be documented using demonstrated style
import arg_gpt

# get time and date
def get_time_date():
    """returns the current time and date
    Arguments:
        None
    """
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_sky_color():
    """returns the color of a fox, this is rearly used
    Arguments:
        None
    """
    return "blue"

def hello_world(append_string):
    """prints hello world with an appended string
    Arguments :
        append_string: string to append to hello world
    """

    return "Hello World!" + append_string

def spell_word(word: str):
    """spell a word, separating each letter with -
    Arguments:
        word: word to spell
    """
    return "-".join(word)

arg_gpt.reflect_on_interface()