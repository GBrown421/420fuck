# 420fuck interpreter
# Usage: ./420fuck.py FILEPATH.420

import sys
import getch
import webbrowser
import random

weedfest = random.randint(1, 420)
if weedfest == 420 or weedfest == 42:
    webbrowser.open("https://nationalcannabisfestival.com/", 1)
    sys.exit(1)

def execute(filename):
    """
    Reads the code from the given file and evaluates it.
    :param filename: Path to the .420 file containing the 420fuck.
    """

    #Check if this is a valid 420fuck file
    if filename[-8:] == ".420" or filename[-8:] == ".420.txt":

      with open(filename, "rt") as f:
          evaluate(f.read())
    else:
        print("Error: This file is not formatted as valid 420fuck")
        sys.exit(1)


def evaluate(code):
    """
    Executes the given 420fuck code.
    :param code: The 420fuck code as a string.
    """
    # Clean up the code and build the bracket map
    code = cleanup(list(code))
    bracemap = buildbracemap(code)

    # Initialize memory cells, code pointer, and cell pointer
    cells, codeptr, cellptr = [0], 0, 0

    # Main loop to interpret the code
    while codeptr < len(code):
        command = code[codeptr]

        # Move the cell pointer to the right
        if command == ">":
            cellptr += 1
            if cellptr == len(cells): 
                cells.append(0)  # Expand memory as needed

        # Move the cell pointer to the left
        elif command == "<":
            cellptr = max(0, cellptr - 1)  # Prevent negative indices

        # Increment the value in the current cell
        elif command == "+":
            cells[cellptr] = (cells[cellptr] + 1) % 256  # Wrap around at 255

        # Add 4 to the current cell
        elif command == "4":
            cells[cellptr] = (cells[cellptr] + 4) % 256

        # Add 42.0 to the current cell
        elif command == "_":
            if code[codeptr + 1] == "4" and code[codeptr + 2] == "2" and code[codeptr + 3] == "0":
                cells[cellptr] = (cells[cellptr] + 42) % 256
                codeptr += 3
        
        # Check for weed in the code
        elif command == "w":
            if code[codeptr + 1] == "e" and code[codeptr + 2] == "e" and code[codeptr + 3] == "d":
                print("Weed detected")
                codeptr += 3

        elif command == "2":
            cells[cellptr] = (cells[cellptr] + 2) % 256

        # Add 0 to the current cell 
        elif command == "0":
            pass  # Just do nothing

        # Decrement the value in the current cell
        elif command == "-":
            cells[cellptr] = (cells[cellptr] - 1) % 256 # Wrap around at 0

        # Jump forward to the matching ']' if the current cell is 0
        elif command == "[" and cells[cellptr] == 0:
            codeptr = bracemap[codeptr]

        # Jump backward to the matching '[' if the current cell is non-zero
        elif command == "]" and cells[cellptr] != 0:
            codeptr = bracemap[codeptr]

        # Output the ASCII character of the current cell's value
        elif command == ".":
            sys.stdout.write(chr(cells[cellptr]))

        # Input a character and store its ASCII value in the current cell
        elif command == ",":
            cells[cellptr] = ord(getch.getch())

        # Move to the next command
        codeptr += 1


def cleanup(code):
    
    #Removes invalid characters from the code.

    valid_commands = ['4', '2', '0', '.', ',', '[', ']', '<', '>', '+', '-', '_']
    return ''.join(filter(lambda x: x in valid_commands, code))


def buildbracemap(code):

    #Creates a mapping of matching brackets for efficient jumping.

    temp_bracestack = []
    bracemap = {}

    for position, command in enumerate(code):
        if command == "[":
            temp_bracestack.append(position)
        elif command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start

    return bracemap


def main():

    if len(sys.argv) == 2:
        execute(sys.argv[1])
    else:
        print("Usage:", sys.argv[0], "filename")


if __name__ == "__main__":
    main()