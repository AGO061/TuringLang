# TuringLang
TuringLang is an esoteric programming language inspired by the Turing machine. It mirrors the core principles of a Turing machine but uses a more modern syntax. While simple in design, the language is intentionally difficult to read, aligning with the spirit of esolangs. 

This document provides an overview of TuringLang and its syntax. For a detailed explanation of Turing machines, check out this [video tutorial](https://www.youtube.com/watch?v=gJQTFhkhwPA).

---

## How a Turing Machine Works
A Turing machine operates with three main components:

### 1. The Tape
- The tape stores information as a series of cells.
- Each cell can hold a symbol from the machine's alphabet (default: `0` or `1`).
- Data on the tape can be initialized before execution but cannot be modified during execution by the user.

Example tape:
```
[0, 1, 0, 0, 0, 1]
```

### 2. The Head
- The head reads and writes to the current cell on the tape.
- It can perform one of three actions after reading/writing:
  - Stay in place.
  - Move one cell to the left.
  - Move one cell to the right.

### 3. The State
- States dictate the behavior of the machine based on the value read by the head.
- Each state specifies:
  1. The value to write.
  2. The movement of the head.
  3. The next state to transition to.

Example state diagram:
1. **State 0**: If the current cell is `0`, write `1`, stay in place, and transition to State 1. If the current cell is `1`, write `1`, stay in place, and halt.
2. **State 1**: Similar logic applies to subsequent states.
3. The **Halt** state ends execution.

---

## TuringLang Syntax

### 1. Initializing the Tape
To initialize the tape, use the `TAPE` command:
```
TAPE [<SYMBOL0><SYMBOL1><SYMBOL2>...]
```
Example:
```
TAPE [010001]
```
**Note:** The size of the tape cannot exceed its initial length during execution.

### 2. Setting a Custom Alphabet
To define a custom alphabet for the tape, use the `ALPHABET` command:
```
ALPHABET [<SYMBOL0><SYMBOL1><SYMBOL2>...]
```
Example:
```
ALPHABET [01AB]
```
This allows symbols `0`, `1`, `A`, and `B` to be used on the tape and in states.

### 3. Positioning the Head
Set the starting position of the head using one of two methods:

#### a. Using `HEAD <N>`
Specify the cell (starting at 0) where the head should be placed:
```
TAPE [010001]
HEAD 3
```
The head is positioned on the 4th cell of the tape.

#### b. Using `HEAD ^`
Visually align the head with the desired cell using the `^` symbol:
```
TAPE [010001]
HEAD     ^
```
The head is positioned on the 4th cell.

### 4. Defining States
Define states with the following syntax:
```
<STATENAME> <CHECK><WRITE><MOVE><NEXTSTATE> ... <INITIAL?>
```
Each state specifies actions for multiple possible symbols defined in the `ALPHABET`.

**Fields:**
- **STATENAME**: Name of the state (no spaces allowed).
- **CHECK**: The symbol to compare with the current cell value (from the alphabet).
- **WRITE**: The symbol to write (from the alphabet).
- **MOVE**: Direction to move the head:
  - `R` for right.
  - `L` for left.
  - `X` for no movement.
- **NEXTSTATE**: Name of the next state.
- **INITIAL?**: Use `INIT` to mark the initial state.

Example:
```
0 01X1 11XH INIT
```
This defines State 0 with:
- If the current cell is `0`, write `1`, stay in place, and transition to State 1.
- If the current cell is `1`, write `1`, stay in place, and halt.

#### The Halt State
The `H` state is reserved as the halt state and cannot be redefined.

#### Naming Rules
State names must:
- Not contain spaces.
- Not match existing commands.
- Not be `H`.

### 5. Comments
Use `#` for comments:
```
# This is a comment
```

---

## Machine Commands

### `RUN`
Runs the machine until it halts or encounters an error:
```
RUN
```

### `WIPE`
Clears all states in the machine:
```
WIPE
```

### `READ`
Outputs the current tape contents as a series of symbols:
```
READ
```

### `CUT`
Cuts a portion of the tape. There are two ways to use `CUT`:

#### a. Cut by Index Range
```
CUT <START> <END>
```
This removes the segment of the tape from index `START` (inclusive) to `END` (inclusive).
Example:
```
TAPE [111AB]
CUT 0 2
```
Resulting tape:
```
[AB]
```

#### b. Cut by Character
```
CUT <CHARACTER>
```
This removes all occurrences of `CHARACTER` from both ends of the tape.
Example:
```
TAPE [AA01101AA]
CUT A
```
Resulting tape:
```
[01101]
```

### `ELONGATE`
Adds symbols to the left or right of the tape.
```
ELONGATE [R/L] <CHARACTER> <LENGTH>
```
- **R/L**: Direction to add the symbols (`R` for right, `L` for left).
- **CHARACTER**: Symbol to add (must be in the alphabet).
- **LENGTH**: Number of symbols to add.

Example:
```
TAPE [01]
ELONGATE R A 3
```
Resulting tape:
```
[01AAA]
```
Another example:
```
TAPE [01]
ELONGATE L B 2
```
Resulting tape:
```
[BB01]
```

### Notes:
- The tape is persistent between runs unless explicitly overwritten using `TAPE`.

---

## Example Program
Here is an example that forces the current cell to `1`:

### Original State Diagram
1. Start at State 0.
2. If the current cell is `0`, write `1`, stay in place, and transition to State 1. If the current cell is `1`, write `1`, stay in place, and halt.
3. In State 1, halt regardless of the cell value.

### TuringLang Code
```
# Initialize the tape
TAPE [0]
# Set a custom alphabet
ALPHABET [01]
# Set head to the first cell
HEAD 0

# Define states
0 00X1 11XH INIT
1 01XH 11XH

# Run the program
RUN

# Output the final tape
READ
```