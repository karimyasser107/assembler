# assembler
FUNCTIONALITTY:
---------------
This assembler take a program (lines of assembly commands) and translate the commands into machine code (0 and 1)

Instruction Set Architecture ISA:
---------------------------------
Please read the instructionSetArchitecture.pdf and the Designof16bits.xlsx to understand the design I have followed in my assembler program.

To run the assembler:
---------------------
Download assembler.py and interpreter.py 
open a cmd and cd to the directory containing the python files "assembler.py", "interpreter.py"
and enter command $python assembler.py
Create your own assembly program or use the test case "Testcase.asm.txt" included in the repo.
Then you will be asked to enter file name (the input file having the program instruction) ex: Testcase.asm.txt

NB: Testcase.asm.txt must be in the same directory as the python files

OUTPUT:
-------
output file will be a memory file containing the instructions assembled in a memeory sized 2^10 words. The memory file will be in the same directory with name "instCache.mem"
