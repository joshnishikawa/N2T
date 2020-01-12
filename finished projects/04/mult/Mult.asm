@R3
M=0		//Zero out R3 (the counter)

@R2
M=0		//Zero out R2 (where the product is stored)

@R0
D=M		//Load the first factor into D
@END
D;JEQ		//End if it's 0 (because n*0=0)
	
@R1
D=M		//Load the second factor into D
@END
D;JEQ		//End if it's 0 (because n*0=0)

(LOOP)	
@R3	
M=D-1		//Store R1-1 in the counter
@R0
D=M		//Load the first factor into D again
@R2
M=D+M		//Add the value of R0 to the product
@R3
D=M		//Load the value of the counter into D
@END
D;JEQ		//End if it's 0
@LOOP
0;JMP		//Continue adding the value of R0 to R2
		//until the loop has run a number of times equal to R1
(END)
@END
0;JMP
