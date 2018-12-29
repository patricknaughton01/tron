import numpy as np
import sys

from generation import Generation


def main():
    generation = Generation(
        100,
        [11, 11, 4, 4],
        0.5,
        10
    )
    print("Starting the program at generation 0")
    while True:
        try:
            command = input("Enter a command (sbs, asap, alap): ")
            if command == "sbs":
                generation.do_generation(render=True)
                print("That was generation {}.".format(str(generation.age - 1)))
            elif command == "asap":
                generation.do_generation()
                print("Just did generation {} as fast as possible.".format(str(generation.age - 1)))
            elif command == "alap":
                print("Doing generations for as long as possible starting at generation {}.".format(str(generation.age)))
                print("Type Ctrl-C to exit the alaping")
                while True:
                    try:
                        generation.do_generation()
                        print("Just did generation {}".format(str(generation.age - 1)))
                    except KeyboardInterrupt:
                        print("Exiting alap")
                        break;
            else:
                print("Not a valid command")
        except KeyboardInterrupt:
            print("Thanks for playing")
            print("Exiting now")
            sys.exit()
    
    
if __name__ == "__main__":
    main()
