import re
# Parser
class Command:
    command_type = ""
    args:list = []
    def __init__(self, command_type:str, args:list = []):
        self.command_type = command_type
        self.args = args

class Parser:
    def __init__(self):
        pass

    def parse_line(self, line:str) -> Command:
        # TAPE COMMAND
        cmd = re.search(r"^TAPE ( *)\[([0-1]*)\]", line)
        if cmd:
            # Command TAPE [Spaces amount, binary string]
            return Command("TAPE",[len(cmd.group(1)),cmd.group(2)])
    
        # HEAD COMMAND
        cmd = re.search(r"^HEAD ( *)\^|^HEAD *(\d+)",line)
        if cmd:
            # Command HEAD [position,use_spaces]
            if cmd.group(1): # check if it has space so you know which one to choose
                return Command("HEAD",[len(cmd.group(1))-1,True])
            else:
                return Command("HEAD",[int(cmd.group(2)),False])

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


        # STATE ABSTRACT COMMAND
        cmd = re.search(r"^([^\s]+) *([0-1])([RXL])([^\s]+) *([0-1])([RXL])([^\s]+) *(INIT)?", line)
        if cmd:
            out = [
                cmd.group(1),
                int(cmd.group(2)),
                cmd.group(3),
                cmd.group(4),
                int(cmd.group(5)),
                cmd.group(6),
                cmd.group(7)
            ]

            if len(cmd.groups()) == 8:
                out.append(cmd.group(8))
            
            return Command("STATE",out)

        return None


# Logic Components


class State:
    name = None
    zero_condition = None
    one_condition = None
    is_initial = False
    is_halt = False
    def __init__(self, name:str, is_initial:bool = False):
        self.name = name
        self.is_initial = is_initial
    
    def set_conditions(self, zero_condition, one_condition):
        self.zero_condition = zero_condition
        self.one_condition = one_condition
    
    def set_as_halt(self):
        self.is_halt=True
    
    def __str__(self):
        return "State: "+self.name+ "(" + str(self.zero_condition) + ", " + str(self.one_condition) + ")"

class Process:
    write = None
    move = None
    state = None
    def __init__(self, write:int, move:str, state):
        self.write = write
        self.move = move
        self.state = state

    def __str__(self):
        return "Process(write: "+str(self.write)+", move: "+ str(self.move) +", state: "+str(self.state.name if isinstance(self.state,State) else "*"+self.state)+")"


class TuringMachine:
    states:list[State] = []
    tape:list[int] = []
    head_position:int = 0
    current_state:State = None
    def __init__(self, states:list[State], tape:list[int], head_position:int = 0):
        self.states = states
        self.tape = tape
        self.head_position = head_position
    
    def run(self):
        current_state = self.find_initial_state()
        
        while True:
            if current_state.is_halt:
                
                break

            if self.tape[self.head_position] == 0:

                self.run_process(current_state.zero_condition)
                current_state = current_state.zero_condition.state

            elif self.tape[self.head_position] == 1:

                self.run_process(current_state.one_condition)
                current_state = current_state.one_condition.state

            else:
                print("The state "+str(self.tape[self.head_position])+" does not exist for cells.")
                exit(1)
    

    def find_initial_state(self) -> State:
        for state in self.states:
            if state.is_initial:
                return state
    
    def run_process(self, process:Process):
        self.tape[self.head_position] = process.write

        match process.move:
            case "R":
                self.head_position+=1
            case "L":
                self.head_position-=1
            case "X":
                pass
            case _:
                print("The head movement of type: \""+process.move+"\" does not exist.")
                exit(2)
    
    def wipe(self) -> None:
        self.states = []
    
                
