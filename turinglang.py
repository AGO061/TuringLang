import turinglib as tl
import re
import sys

tape:list[int] = []
tape_spaces:int = 0
head_position:int = 0
parser = tl.Parser()
states:list[tl.State] = []
run_count:int = 1
halt_state = tl.State("H",False)
halt_state.set_as_halt()
states.append(halt_state)


# Open the file in read mode
with open(sys.argv[1], 'r') as file:
    remaining_runs = run_count
    # Read each line in the file
    for line in file:
        # cleanup line
        line = line.strip()
        comment_check = re.search(r"^(.*)#.*",line)
        if comment_check:
            line=comment_check.group(1).strip()
        
        command=parser.parse_line(line)
        if command:
            match command.command_type:
                case "TAPE":
                    tape_spaces = command.args[0]
                    tape = list(map(int, [*command.args[1]]))
                case "HEAD":
                    if command.args[1]:
                        head_position=command.args[0]-(tape_spaces)
                    else:
                        head_position=command.args[0]
                case "WIPE":
                    states:list[tl.State] = [halt_state]
                case "RUN":
                    tm = tl.TuringMachine(states,tape,head_position)
                    tm.run()
                    tape = tm.tape
                    head_position = tm.head_position
                case "READ":
                    print(tape)
                case "STATE":
                    new_state = tl.State(command.args[0], command.args[7]!=None)
                    new_state.set_conditions(tl.Process(command.args[1],command.args[2],command.args[3]),tl.Process(command.args[4],command.args[5],command.args[6]))
                    states.append(new_state)

                    for statecheck in states:
                        for state in states:
                            if state.name == "H":
                                continue
                            
                            if state.zero_condition.state == statecheck.name:
                                state.zero_condition.state=statecheck
                            elif state.zero_condition.state == "H":
                                state.zero_condition.state=halt_state
                            
                            if state.one_condition.state == "H":
                                state.one_condition.state=halt_state
                            elif state.one_condition.state == statecheck.name:
                                state.one_condition.state=statecheck
                case _:
                    print("COMMAND NOT FOUND: "+command.command_type+"!")
                    exit(3)