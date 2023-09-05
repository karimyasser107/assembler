import re
import sys
from Interpreter import Interpreter

# prompt user to enter file name
FileName = input("Enter file Name: ")
# open the file
programFile = open(FileName, "r")
instructionsList = []
# loop on lines of the program
for line in programFile:
    # skip comments and empty lines
    if line[0] == "#" or line[0] == "\n" or line[0] == "ï":
        continue
    # we want to remove comments written besides instructions
    words = line.split()
    instructionLine = ""
    for word in words:
        if word[0] == "#":
            break
        if(not instructionLine):
            instructionLine = word.upper()
        else:
            instructionLine = instructionLine+" "+word.upper()
    # put the instruction without comments in the list "instructionsList"
    if(len(words) != 0 and words[0] != "#"):
        instructionsList.append(instructionLine)

# close programFile
programFile.close()

# create a list of size 2^10 like the instruction memory initialised with zeros
instCache = ["0000000000000000\n"] * (2**10)
address = -1
instruction_16bits = ""
instructionORG = False
# loop on instructions
for instruction in instructionsList:
    # split instruction into "words" list
    # example "INC R5, R5" ==> ["INC","R5","R5"]
    words = re.split(r"\s+|,\s|,", instruction)
    if(len(words) == 1):  # NO operands
        # instructions NOP, SETC, CLRC, RET, RTI, hexVal(in case of .ORG address \n hexVALUE)
        instruction_16bits = Interpreter(words[0])

    elif(len(words) == 2):  # 1 operand only
        # instructions .ORG, IN, OUT, PUSH, POP, JZ, JC, JMP, CALL
        # If instruction is "".ORG address" so, the address is words[1]
        if words[0] == ".ORG":
            # address in program is in hexa so we want to convert it to decimal
            address = int(words[1], base=16)
            instructionORG = True
            continue
        instruction_16bits = Interpreter(
            words[0], words[1])

    elif(len(words) == 3):  # 2 operands
        # instructions NOT, INC, DEC, MOV, LDM, LDD, STD
        instruction_16bits = Interpreter(
            words[0], words[1], words[2])

    elif(len(words) == 4):  # 3 operands
        # instructions ADD, IADD, SUB, AND, OR
        instruction_16bits = Interpreter(
            words[0], words[1], words[2], words[3])

    else:
        print("error in instruction: "+instruction+"\n"+"Cannot proceed\n")
        sys.exit("Error")

    # now we have instruction 16 bits
    # first check if we have a specific address made with ORG
    if instructionORG == True:
        # we have already calculated the specific address in Address
        instructionORG = False
    elif instructionORG == False:
        # increment last address
        address += 1
    # add 16 bit instruction to the instruction cache
    instCache[address] = str(instruction_16bits[0]) + "\n"

    # if the returned instruction_16bits list is of size 2 so the instruction was an immediate instruction
    if len(instruction_16bits) == 2:
        # this is the immediate value
        # it must follow the inst and to be in the next address
        address += 1
        instCache[address] = str(instruction_16bits[1]) + "\n"

# Write instCache in a file
instCacheFile = open("instCache.mem", "w")
for i in range(2**10):
    instCacheFile.write(instCache[i])
instCacheFile.close()
