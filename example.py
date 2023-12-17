import sys

import arg_gpt
import example_functions

if __name__ == "__main__":
    sys.argv.append("what can you do")
    arg_gpt.run_arg_prompt()