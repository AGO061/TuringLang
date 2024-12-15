import re

# Parser
class Command:
    command_type = ""
    args: list = []

    def __init__(self, command_type: str, args: list = []):
        self.command_type = command_type
        self.args = args





class Parser:
    def __init__(self):
        pass

    def parse_line(self, line: str) -> Command:
        # TAPE COMMAND
        cmd = re.search(r"^TAPE ( *)\[([^\s]*)\]", line)
        if cmd:
            return Command("TAPE", [len(cmd.group(1)), cmd.group(2)])

        # HEAD COMMAND
        cmd = re.search(r"^HEAD ( *)\^|^HEAD *(\d+)", line)
        if cmd:
            if cmd.group(1):
                return Command("HEAD", [len(cmd.group(1)) - 1, True])
            else:
                return Command("HEAD", [int(cmd.group(2)), False])

        # RUN COMMAND
        cmd = re.search(r"^RUN", line)
        if cmd:
            return Command("RUN")

        # WIPE COMMAND
        cmd = re.search(r"^WIPE", line)
        if cmd:
            return Command("WIPE")

        # READ COMMAND
        cmd = re.search(r"^READ", line)
        if cmd:
            return Command("READ")

        # CUT COMMAND
        cmd = re.search(r"^CUT +(\d+) +(\d+)", line)
        if cmd:
            return Command("CUT",[cmd.group(1),cmd.group(2)])
        
        cmd = re.search(r"^CUT +([^\s])", line)
        if cmd:
            return Command("CUT",[cmd.group(1)])

        # ELONGATE COMMAND
        cmd = re.search(r"^ELONGATE +([RL]) +([^\s]) +(\d+)",line)
        if cmd:
            return Command("ELONGATE",[cmd.group(1),cmd.group(2),cmd.group(3)])

        # ALPHABET COMMAND
        cmd = re.search(r"^ALPHABET +\[([^\s]+)\]", line)
        if cmd:
            return Command("ALPHABET", [cmd.group(1)])


        # STATE ABSTRACT COMMAND
        # Reference: ^([^\s]+) *(([^\s])([^\s])([RXL])([^\s]+) *)+(INIT)?
        cmd = re.search(r"(^[^\s]+)( *(?:(?:[^\s])(?:[^\s])(?:[RXL])(?:[^\s]+) *)+(INIT)?)", line)
        if cmd:
            name = cmd.group(1) # save the name
            line = cmd.group(2) # remove the name
            is_initial = cmd.group(3) != None
            # get each state branch
            cmd = re.findall(r"((?:[^\s])(?:[^\s])(?:[RXL])(?:[^\s]+))",line)
            out=[]
            for branch in cmd:
                out.append(branch)
            out.insert(0,len(out))
            out.insert(0,is_initial)
            out.insert(0,name)

            
            # STATE [name, is initial, number of branches, branch, branch, ...]
            return Command("STATE", out)

        return None


# Logic Components

class StateBranch:
    check:str = "" # the character to check for
    write:str = "" # the character to write if the check passes
    move:str = "" # the direction to move the head in if the check passes
    next_state:str = "" # the state to go to next

    def write_states(self,check:str,write:str,move:str,next_state:str):
        self.check = check
        self.write = write
        self.move = move
        self.next_state = next_state

    def __init__(self,compact_string:str):
        parts = re.search(r"([^\s])([^\s])([RXL])([^\s]+)",compact_string)

        self.write_states(parts.group(1),
                          parts.group(2),
                          parts.group(3),
                          parts.group(4))

    def __str__(self):
        return f"StateBranch(check:{self.check}, write:{self.write}, move:{self.move}, next_state:{self.next_state})"



class State:
    name = None
    branches:list[StateBranch] = None # had to set this to None, because mutables
    is_initial = False
    is_halt = False

    def __init__(self, name: str, is_initial: bool = False):
        self.name = name
        self.is_initial = is_initial
        if not self.branches:
            self.branches=[]

    def add_branch(self,branch:str):
        
        self.branches.append(StateBranch(branch))

    def set_as_halt(self):
        self.is_halt = True

    def __str__(self):
        return "State: " + self.name + " (" + str([str(branch) for branch in self.branches]) + ")"


class TuringMachine:
    alphabet:list[str] = None
    states: list[State] = None
    tape: list[str] = None
    head_position: int = 0
    current_state: State = None

    def __init__(self, states: list[State], tape: list[str], alphabet:list[str], head_position: int = 0):
        self.states = states
        self.tape = tape
        self.head_position = head_position
        self.alphabet = alphabet

    def run(self):
        current_state = self.find_initial_state()

        while True:
            if current_state.is_halt:
                break

            if self.head_position < 0 or self.head_position >= len(self.tape):
                print(f"Error: Head position {self.head_position} is out of tape bounds.")
                exit(1)

            for branch in current_state.branches:
                try:
                    if self.run_branch(branch, self.tape[self.head_position]):
                        new_state = self.get_state_from_name(branch.next_state)
                        if new_state:
                            current_state = new_state
                            break
                        else:
                            print(f"Error: Couldn't find the state \"{branch.next_state}\".")
                            exit(1)
                except IndexError:
                    print(f"Error: Head position {self.head_position} is out of tape boundss.")
                    exit(1)

                
            
    def get_state_from_name(self, state_name:str) -> State:
        for state in self.states:
            if state_name == state.name:
                return state
        return None

    def find_initial_state(self) -> State:
        initial_states = [state for state in self.states if state.is_initial]
        if not initial_states:
            print("Error: No initial state defined.")
            exit(1)
        return initial_states[0]

    def run_branch(self, branch: StateBranch, condition:str) -> bool: # returns true if the branch ran successfully (condition was true)
        if branch is None:
            print("Error: Attempted to run a branch that is not defined.")
            exit(1)

        if condition not in self.alphabet:
            print(f"Error: The character \"{condition}\" (condition) is not in the given alphabet.")
            exit(1)

        if branch.check not in self.alphabet:
            print(f"Error: The character \"{branch.check}\" (branch check) is not in the given alphabet.")
            exit(1)

        if branch.check != condition:
            return False
        self.tape[self.head_position] = branch.write
        match branch.move:
            case "R":
                self.head_position += 1
            case "L":
                self.head_position -= 1
            case "X":
                pass
            case _:
                print("Error: The head movement of type: \"" + branch.move + "\" does not exist.")
                exit(2)

        return True

    def wipe(self) -> None:
        self.states = []
        self.tape = []
        self.head_position = 0
        print("Turing machine state wiped.")