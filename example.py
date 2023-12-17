import sys
import logging
import arg_gpt
import example_functions

logging.basicConfig(level=logging.INFO)

@arg_gpt.gpt_func
def get_time_date():
    """returns the current time and date
    Arguments:
        None
    """
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    sys.argv.append("what is the time?")
    arg_gpt.run_arg_prompt()