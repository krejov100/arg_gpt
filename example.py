import sys
import logging
import arg_gpt
import example_functions

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    sys.argv.append("what color is the sky?")
    arg_gpt.run_arg_prompt()