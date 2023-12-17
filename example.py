import sys
import logging
import arg_gpt
import example_functions

logging.basicConfig(level=logging.INFO)

@arg_gpt.gpt_func
def print_2d_table(table: list[list[float]]):
    """
    Prints a 2D table of floats.

    Arguments:
        table: A list of lists of floats.
    """
    for row in table:
        print(row)

if __name__ == "__main__":
    #sys.argv.append("empty the directory /Users/philipkrejov/PycharmProjects/arg_gpt/test")
    sys.argv.append("print a random 3x3 table of really random floats")
    arg_gpt.run_arg_prompt()