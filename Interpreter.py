import sys
import string


def Convert_Hex_Binary(hexaString: str) -> str:
    binaryStrinng = bin(eval('0x'+hexaString))
    if(len(binaryStrinng)-2 < 16):
        binaryStrinng = "0"*(16-(len(binaryStrinng)-2)) + \
            binaryStrinng[-(len(binaryStrinng)-2):]
        return binaryStrinng
    else:
        return binaryStrinng[-16:]


def Register_Interpreter(RegisterName: str) -> str:
    # this function takes the register name and returns a string containing 3 bits that identify the register number
    # example "R1" -> "001"  ,  "R7" -> "111"
    regNum = RegisterName[1]
    if regNum == "0":
        return "000"
    elif regNum == "1":
        return "001"
    elif regNum == "2":
        return "010"
    elif regNum == "3":
        return "011"
    elif regNum == "4":
        return "100"
    elif regNum == "5":
        return "101"
    elif regNum == "6":
        return "110"
    elif regNum == "7":
        return "111"
    else:
        print("error in register name: "+RegisterName+"\n"+"Cannot proceed\n")
        sys.exit("Error")


def Interpreter(instruction: str, operand1: str = None, operand2: str = None, operand3: str = None):
    instructions_16bitList = []
    instructions_16bitList.append("")
    if operand1 is None and operand2 is None and operand3 is None:
        # instructions: NOP, SETC, CLRC, RET, RTI, hexVALUE
        # NOP instruction
        if instruction == "NOP":
            instructions_16bitList[0] = "00000" + "0"*11
        # SETC instruction
        elif instruction == "SETC":
            instructions_16bitList[0] = "00001" + "0"*11
        # CLRC instruction
        elif instruction == "CLRC":
            instructions_16bitList[0] = "00011" + "0"*11
        # RET instruction
        elif instruction == "RET":
            instructions_16bitList[0] = "11100" + "0"*11
        # RTI instruction
        elif instruction == "RTI":
            instructions_16bitList[0] = "11101" + "0"*11
        # hexadecimal value
        elif all(c in string.hexdigits for c in instruction):
            hexVal = Convert_Hex_Binary(instruction)
            instructions_16bitList[0] = hexVal
        else:
            print("error in instruction: "+instruction+"\n"+"Cannot proceed\n")
            sys.exit("Error")
    elif operand1 != None and operand2 != None and operand3 != None:
        # instructions: ADD, IADD, SUB, AND, OR
        # ADD instruction: Add Rdst,Rsrc1,Rsrc2
        if instruction == "ADD":
            rs = Register_Interpreter(operand2)  # Rsrc1
            rt = Register_Interpreter(operand3)  # Rsrc2
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "01000" + rs + rt + rd + "00"
        # IADD instruction: IADD Rdst,Rsrc1,Imm
        elif instruction == "IADD":
            rs = Register_Interpreter(operand2)  # Rsrc1
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "01010" + rs + "000" + rd + "00"
            # check if the operand 3 (hexadecimal value) has letter h in it and remove it
            for c in operand3:
                if c == 'h' or c == 'H':
                    operand3 = operand3.replace(c, '')
            # immmediate value
            if all(c in string.hexdigits for c in operand3):
                immediateValue = Convert_Hex_Binary(operand3)
                instructions_16bitList.append(immediateValue)    # Imm
            else:
                print("error in instruction: "+instruction +
                      ": immediate value missing\n")
                sys.exit("Error")
        # SUB instruction: SUB Rdst,Rsrc1,Rsrc2
        elif instruction == "SUB":
            rs = Register_Interpreter(operand2)  # Rsrc1
            rt = Register_Interpreter(operand3)  # Rsrc2
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "01001" + rs + rt + rd + "00"
        # AND instruction: AND Rdst,Rsrc1,Rsrc2
        elif instruction == "AND":
            rs = Register_Interpreter(operand2)  # Rsrc1
            rt = Register_Interpreter(operand3)  # Rsrc2
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "01011" + rs + rt + rd + "00"
        # OR instruction
        elif instruction == "OR":
            rs = Register_Interpreter(operand2)  # Rsrc1
            rt = Register_Interpreter(operand3)  # Rsrc2
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "01100" + rs + rt + rd + "00"
        else:
            print("error in instruction: "+instruction+"\n"+"Cannot proceed\n")
            sys.exit("Error")
    else:
        # instructions: IN, OUT, PUSH, POP, JZ, JC, JMP, CALL
        # IN instruction: IN Rdst
        if instruction == "IN":
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "00100" + "000"+"000" + rd + "00"
        # OUT instruction: OUT Rsrc
        elif instruction == "OUT":
            rs = Register_Interpreter(operand1)  # Rsrc
            instructions_16bitList[0] = "00101" + \
                rs + "000"+"000" + \
                "00"  # changed place to rs for forwarding unit to detect data hazard   # changed*******
        # PUSH instruction: PUSH Rrsc1
        elif instruction == "PUSH":
            rt = Register_Interpreter(operand1)  # Rsrc1
            instructions_16bitList[0] = "10000" + "000" + rt + "000"+"00"
        # POP instruction: POP Rdst
        elif instruction == "POP":
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "10001" + "000"+"000" + rd + "00"
        # JZ instruction: JZ Rdst
        elif instruction == "JZ":
            rs = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "11000" + rs + "000"+"000" + "00"
        # JC instruction: JC Rdst
        elif instruction == "JC":
            rs = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "11001" + rs + "000"+"000" + "00"
        # JMP instruction: JMP Rdst
        elif instruction == "JMP":
            rs = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "11010" + rs + "000"+"000" + "00"
        # CALL instruction: CALL Rdst
        elif instruction == "CALL":
            rs = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "11011" + rs + "000"+"000" + "00"

        # instructions: NOT, INC, DEC, MOV, SWAP, LDM, LDD, STD
        # NOT instruction: NOT Rdst,Rsrc
        elif instruction == "NOT":
            rs = Register_Interpreter(operand2)  # Rsrc
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "00010" + rs + "000" + rd + "00"
        # INC instruction: INC Rdst,Rsrc
        elif instruction == "INC":
            rs = Register_Interpreter(operand2)  # Rsrc
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "00110" + rs + "000"+rd+"00"
        # DEC instruction: DEC Rdst,Rsrc
        elif instruction == "DEC":
            rs = Register_Interpreter(operand2)  # Rsrc
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "00111" + rs + "000"+rd+"00"
        # MOV instruction: MOV Rdst,Rsrc1
        elif instruction == "MOV":
            rs = Register_Interpreter(operand2)  # Rsrc1
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "01111" + rs + "000"+rd+"00"
        # LDM instruction: LDM Rdst,IMM
        elif instruction == "LDM":
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "10010" + "000"+"000" + rd + "00"
            # immmediate value
            # check if the operand 2 (hexadecimal value) has letter h in it and remove it
            for c in operand2:
                if c == 'h' or c == 'H':
                    operand2 = operand2.replace(c, '')
            # check if the operand 2 is all hexadecimal digits
            if all(c in string.hexdigits for c in operand2):
                immediateValue = Convert_Hex_Binary(operand2)
                instructions_16bitList.append(immediateValue)  # IMM
            else:
                print("error in instruction: "+instruction +
                      ": immediate value missing\n")
                sys.exit("Error")
        # LDD instruction: LDD Rdst,Rsrc1
        elif instruction == "LDD":
            rs = Register_Interpreter(operand2)  # Rsrc1
            rd = Register_Interpreter(operand1)  # Rdst
            instructions_16bitList[0] = "10011" + \
                rs + "000" + rd + "00"  # swaped and used rs and rd  # changedd***********
        # STD instruction: STD Rsrc2,Rsrc1
        elif instruction == "STD":
            rs = Register_Interpreter(operand1)  # Rsrc2
            rt = Register_Interpreter(operand2)  # Rsrc1
            instructions_16bitList[0] = "10100" + \
                rs + rt + "000"+"00"  # swaped and used rs and rt    # changed***********
        else:
            print("error in instruction: "+instruction+" its operands: op1= " +
                  operand1+" op2="+operand2+" op3="+operand3+"\nCannot proceed\n")
            sys.exit("Error")
    return instructions_16bitList
