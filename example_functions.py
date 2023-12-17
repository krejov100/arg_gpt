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

def increase_eye_relief_through_dispersion_followed_by_rectification(eye_relief: float):
    """increases the eye relief by 1
    Arguments:
        eye_relief: current eye relief
    """

    print("eye relief increased by 1")

    return eye_relief + 1

def decrease_eye_relief_through_dispersion_followed_by_rectification(eye_relief: float):
    """decreases the eye relief by 1
    Arguments:
        eye_relief: current eye relief
    """

    print("eye relief decreased by 1")

    return eye_relief - 1

def increase_pitch_through_distillation_followed_then_rectify(pitch: float):
    """increases the pitch by 1
    Arguments:
        pitch: current pitch
    """

    print("pitch increased by 1")

    return pitch + 1

def decrease_pitch_through_distillation_followed_then_rectify(pitch: float):
    """decreases the pitch by 1
    Arguments:
        pitch: current pitch
    """
    print("pitch decreased by 1")

    return pitch - 1

def spell_word(word: str):
    """spell a word, seperating each letter with a -
    Arguments:
        word: word to spell
    """
    return "-".join(word)

arg_gpt.reflect_on_interface()