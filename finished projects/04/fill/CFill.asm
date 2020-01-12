(LOOP)
@KBD
D=M		// load the KBD value into D
@CLEAR
D;JEQ		// if 0, jump to WRITE
D=-1		// else load the "blacken" command into D

(CLEAR)
@kbdval
M=D		// store KBD value (either 0 or -1) in a new variable
@SCREEN
D=A		// load SCREEN address into D
@fillme
M=D		// store it as a new variable

(WRITE)
@fillme
D=M		// load the current address
@KBD
D=D-A		// subtract the KBD address from the current address
@LOOP
D;JGE		// if negative, jump back to LOOP
@kbdval 
D=M		// else load the kbdval back into D,
@fillme
A=M		// load the current address into A,
M=D		// and write kbdval into it
D=A+1		// load the next address into D
@fillme
M=D		// write the next address into fill
@WRITE
0;JMP		// run the WRITE loop again
