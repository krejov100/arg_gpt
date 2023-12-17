import sys
import logging
from arg_gpt import gpt_func, run_arg_prompt
import example_functions

logging.basicConfig(level=logging.INFO)

@gpt_func
def print_2d_table(table: list[list[float]]):
    """
    Prints a 2D table of floats.

    Arguments:
        table: A list of lists of floats.
    """
    for row in table:
        print(row)

if __name__ == "__main__":
    sys.argv.append("print a random 3x3 table of really random floats")
    run_arg_prompt()