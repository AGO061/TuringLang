import turinglib as tl
import re
import sys

tape: list[str] = []
tape_spaces: int = 0
alphabet:list[str] = ["0","1"]
head_position: int = 0
parser = tl.Parser()
states: list[tl.State] = []
run_count: int = 1
halt_state = tl.State("H")
halt_state.set_as_halt()
states.append(halt_state)

# Debug options: -d wait_time log_file
use_debug=False
wait_time = 0
log_file = ""
if len(sys.argv)>2:
    use_debug=sys.argv[2] == "-d" or sys.argv[2] == "--debug" 
    if len(sys.argv)>3:
        wait_time = float(sys.argv[3])
        if len(sys.argv)>4:
            log_file = sys.argv[4]
try:
    with open(sys.argv[1], 'r') as file:
        remaining_runs = run_count
        # Read each line in the file
        for line in file:
            # Cleanup line
            line = line.strip()
            comment_check = re.search(r"^(.*)#.*", line)
            if comment_check:
                line = comment_check.group(1).strip()

            command = parser.parse_line(line)
            if command:
                match command.command_type:
                    case "TAPE":
                        tape_spaces = command.args[0]
                        tape = list(map(str, [*command.args[1]]))
                    case "CUT":
                        if len(command.args) == 1:
                            char = command.args[0]
                            try:
                                while True:
                                    if tape[0] == char:
                                        del tape[0]
                                    else:
                                        break
                                
                                while True:
                                    if tape[-1] == char:
                                        del tape[-1]
                                    else:
                                        break
                            except:
                                pass # skip all list errors that might occur here (at some point it's either gonna finish or fail)
                        elif len(command.args) == 2:
                            del tape[command.args[0]:command.args[1]+1] # shouldn't error out
                        else:
                            print(f"Error: CUT can't have that many arguments ({len(command.args)}).")
                            exit(1)
                    case "ELONGATE":
                        if command.args[0]=="L":
                            for i in range(int(command.args[2])):
                                tape.insert(0,command.args[1])
                        elif command.args[0]=="R":
                            for i in range(int(command.args[2])):
                                tape.append(command.args[1])
                        else:
                            print(f"Error: ELONGATE does not support the \"{command.args(1)}\" direction.")
                            exit(1)
                    case "HEAD":
                        if command.args[1]:
                            head_position = command.args[0] - tape_spaces
                        else:
                            head_position = command.args[0]
                        # Validate head position
                        if head_position < 0 or head_position >= len(tape):
                            print(f"Error: Head position {head_position} is out of tape bounds after HEAD command.")
                            exit(1)
                    case "WIPE":
                        states = [halt_state]
                    case "RUN":
                        #print([str(state) for state in states])
                        tm = tl.TuringMachine(states, tape, alphabet, head_position, debug=use_debug, wait_time=wait_time, log_file=log_file)
                        tm.run()
                        tape = tm.tape
                        head_position = tm.head_position
                    case "READ":
                        print("["+"".join(tape)+"]")
                    case "ALPHABET":
                        alphabet = list(map(str, [*command.args[0]]))
                    case "STATE":
                        # STATE [name, is initial, number of branches, branch, branch, ...]
                        new_state = tl.State(command.args[0], command.args[1])
                        for branch_number in range(command.args[2]):
                            new_state.add_branch(command.args[branch_number+3])
                        states.append(new_state)

                    case _:
                        print(f"Error: COMMAND NOT FOUND: {command.command_type}!")
                        exit(3)

except FileNotFoundError:
    print(f"Error: The file '{sys.argv[1]}' was not found.")
    exit(1)
except IndexError:
    print("Error: No input file specified. Please provide a file as a command line argument.")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)