# TuringLang
As a great enjoyer of brainfuck myself, I decided it was time to create an esolang.\
TuringLang is an Esoteric programming language inspired by the Turing machine.
It works practically in the same way, but it uses modern syntax which is fast to type but
not so easy to understand.\
This is just a small project but I hope it reaches the right audience.
I'm not the best when it comes to explaining so, i tried, but I'll leave here a [simple video](https://www.youtube.com/watch?v=gJQTFhkhwPA) that explains the whole thing in detail, it's great and he does a much better job than me at explaining this concept.

## How a turing machine works
Turing machines are composed of the following:
* There is a tape divided in cells which can contain either 1 or 0.
* There is a head which can move between cells.
* The machine is in a state and it can transition into another state.

Now we'll see everything in more detail
### The Tape
The tape contains information which can be fed into the machine before it starts, but it can't be manipulated during execution.\
![0,1,0,0,0,1 on tape](https://github.com/AGO061/TuringLang/blob/main/tape.png?raw=true)\
The data in the tape is divided into single cells and each cell can only contain either 1 or 0.
### The Head
The head looks at a specific cell, it reads the cell, writes the cell and then it can do one of three things: Nothing, Move left, Move right.\
The head is the "Arm" of the operation, it reads, writes and moves, nothing more.\
### The State
The state is the "Brain" of the machine and it describes what value the head should write and what the state of the next operation is, based on what the head read.\
It connects to two states, one for 0 and the other one for 1.\
The following is an example of states:\
![Example States](https://github.com/AGO061/TuringLang/blob/main/simpleprogram.png?raw=true)\
The state loop in this case would be:
1. Start at state 0
2. If the cell i'm on is 0 then set to 1, don't move the head and go to state 1. If the cell I'm on is 1 then set it to 1, don't move the head and halt the program.
3. do the same for the next states unless you are on halt.

The halt state is  a special one, as it determines the end of all operations in the program.

## Feeding again and again and again...
With a real touring machine, you can "change" the states and feed the tape from a machine into another. TuringLang allows for a similar thing, it allows you to edit the machine and feed back the data into it and rerun it. But let's get to the juicy bit, the syntax!
## TuringLang Syntax
### Tape
You start a TuringLang program with:
```
TAPE [<BIT0><BIT1><BIT2>...]
```
So if you wanted to write `010001` onto the tape you would write:
```
TAPE [010001]
```
**You can't exceed the size of the tape during the execution!**
### Head
Before running the machine, you may decide where you want the head to be placed on your tape.\
The syntax is divided in 2:
#### HEAD \<N\>
You can specify the position of the head (starting from 0) on a single cell of the tape.\
Example:
```
TAPE [010001]
HEAD 3
```
The head will be positioned on the 4th cell of the tape.
#### HEAD ^
You can also specify the position of the head visually using spaces and ^\
to do so, just put the arrow where you want the head to go (a monospace font is required though to visualize correctly).
```
TAPE [010001]
HEAD     ^
```
The head will be positioned on the 4th cell of the tape.
### States
To define states you just have to type:
```
<STATENAME> <WRITE><MOVE><NEXTSTATE> <WRITE><MOVE><NEXTSTATE> <INITIAL?>
```
There are 2 couples of `<WRITE><MOVE><NEXTSTATE>`, the first one is if the value read by the head is 0, the second one is if it is 1.
* STATENAME is the name of the state, it's a string without spaces.
* WRITE is the bit to write can be either 0 or 1
* MOVE is the direction the head has to move to, which can be: R for Right, L for Left, X for None.
* NEXTSTATE is the name of the next state.
* INITIAL? write "INIT" if this is the initial state

#### The H state
The H state is the halt state, thus it can't be overwritten.
#### Allowed Names
As long as the state name follows the following rules, it's allowed:
* It must not contain spaces.
* It must not be the same as an existing command.
* It must not be `H`.

### Comments
Comments are done the pythonic way, using `#`.

### Machine commands
These commands are meant to imitate a user interacting with the machine, kind of like writing the tape or moving the head.
#### Run
The run command runs the machine until it reacher either an error or the halt state, the next lines of code are read afterwards.
```
RUN
```

#### Wipe
The wipe command allows you to clear the states of the machine.
```
WIPE
```

#### Read
The read command reads the tape as a series of 1s and 0s.
```
READ
```

### Useful notes
* The TAPE is never cleared unless specified by the user, that means that the tape is saved between runs, unless overwritten by the TAPE command.

## Example
Let's translate the example of the states we had before.
```
# Force current cell to 1

# Make the cell 0
TAPE [0]
# Move the head to the start
HEAD 0

# State 0 (Initial)
#  0   1
0 1X1 1XH INIT
# State 1
1 1XH 1XH
#  0   1

RUN # Runs the machine

READ # Reads the final tape
```
