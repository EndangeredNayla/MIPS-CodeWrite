
#Import python libraries
import struct
#from numpy import *
import n64crc
from os import path


#Return the value of a register based off of its name
#See https://en.wikibooks.org/wiki/MIPS_Assembly/Register_File
def register(name):
  if name[0] != '$': #Add $ to the register name if not there
    name = '$'+name 
  if name == '$zero' or name == '$r0': #Always zero
    return 0
  elif name == '$at': #Reserved for assembler
    return 1
  elif name == '$v0': #First and second return values, respectively
    return 2
  elif name == '$v1':
    return 3
  elif name == '$a0': #First four return arguents to functions
    return 4
  elif name == '$a1':
    return 5
  elif name == '$a2':
    return 6
  elif name == '$a3':
    return 7
  elif name == '$t0': #Temporary registers
    return 8
  elif name == '$t1':
    return 9
  elif name == '$t2':
    return 10
  elif name == '$t3':
    return 11
  elif name == '$t4':
    return 12
  elif name == '$t5':
    return 13
  elif name == '$t6':
    return 14
  elif name == '$t7':
    return 15
  elif name == '$s0': #Saved registers
    return 16
  elif name == '$s1':
    return 17
  elif name == '$s2':
    return 18
  elif name == '$s3':
    return 19
  elif name == '$s4':
    return 20
  elif name == '$s5':
    return 21
  elif name == '$s6':
    return 22
  elif name == '$s7':
    return 23
  elif name == '$t8': #More temporary registers
    return 24
  elif name == '$t9':
    return 25
  elif name == '$k0': #Reserved for kernel (operating system)
    return 26
  elif name == '$k1':
    return 27
  elif name == '$gp': #Global pointer
    return 28
  elif name == '$sp': #Stack pointer
    return 29
  elif name == '$fp': #Frame pointer
    return 30
  elif name == '$ra': #Return address
    return 31





#MIPS Assembler function, feed it a command as a string and it returns the hex
#This is not really meant to be a 100% fully functional, but to help it make it easier for me to hack the game
#For commands see https://en.wikibooks.org/wiki/MIPS_Assembly/Instruction_Formats
#For information about instruction types see https://web.archive.org/web/20180101004911if_/http://www.cs.umd.edu/class/spring2003/cmsc311/Notes/Mips/format.html
def assembler(asm):
  asm = asm.replace(', ', ' ').replace(')','').replace('(','').replace(',',' ')
  words = asm.lower().split(' ')
  n_words = len(words)
  command = words[0]
  opcode = 0x00
  funct = 0x00
  reg_s = 0x00
  reg_t = 0x00
  reg_d = 0x00
  imm = 0x0000
  address = 0x000000
  shift_amount = 0x00
  if command == 'nop': #Do nothing
    return(0x00000000)
  elif command == 'cache': #Special handling of the cache command
    itype = 'I'
    funct = 0x2F
    reg_t = words[1] #Not a register in this case (CACHE is special)
    reg_s = register(words[2])
    imm = int(words[3], 16)
  elif command == 'add': #Add
    itype = 'R'
    funct = 0x20
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'addi': #Add Immediate 
    itype = 'I'
    opcode = 0x08
    reg_t = register(words[1])
    reg_s = register(words[2])
    imm = int(words[3], 16)
  elif command == 'addiu': #Add Unsigned Immediate
    itype = 'I'
    opcode = 0x09
    reg_t = register(words[1])
    reg_s = register(words[2])
    imm = int(words[3], 16)
  elif command == 'addu': #Add Unsigned
    itype = 'R'
    funct = 0x21
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'and': #Bitwise AND
    itype = 'R'
    funct = 0x24
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'andi': #Bitwise AND Immediate
    itype = 'I'
    opcode = 0x0C
    reg_t = register(words[1])
    reg_s = register(words[2])
    imm = int(words[3], 16)
  elif command == 'beq': #Branch if Equal
    itype = 'I'
    opcode = 0x04
    reg_s = register(words[1])
    reg_t = register(words[2])
    imm = int(words[3], 16)
  elif command == 'beqz': #Branch if Equal to Zero
    itype = 'I'
    opcode = 0x04
    reg_s = register(words[1])
    reg_t = 0
    imm = int(words[2], 16)
  elif command == 'blez': #Branch if Less Than or Equal to Zero
    itype = 'I'
    opcode = 0x06
    reg_s = register(words[1])
    imm = int(words[2], 16)
  elif command == 'bne': #Branch if Not Equal
    itype = 'I'
    opcode = 0x05
    reg_s = register(words[1])
    reg_t = register(words[2])
    imm = int(words[3], 16)
  elif command == 'bgtz': #Branch on Greater Than Zero
    itype = 'I'
    opcode = 0x07
    reg_s = register(words[1])
    imm = int(words[2], 16)
  elif command == 'div': #Divide
    itype = 'R'
    funct = 0x1A
    reg_s = register(words[1])
    reg_t = register(words[2])
  elif command == 'divu': #Unsigned Divide
    itype = 'R'
    funct = 0x1B
    reg_s = register(words[1])
    reg_t = register(words[2])
  elif command == 'j': #Jump to Address
    itype = 'J'
    opcode = 0x02
    address = int((int(words[1], 16) - 0x80000000)/4)
  elif command == 'jal': #Jump and Link
    itype = 'J'
    opcode = 0x03
    address = int((int(words[1], 16) - 0x80000000)/4)
  elif command == 'jalr': #Jump and Link Register
    itype = 'R'
    funct = 0x09
    reg_s = register(words[1])
    reg_d = register(words[2])
  elif command == 'jr': #Jump to Address in Register
    itype = 'R'
    funct = 0x08
    reg_s = register(words[1])
  elif command == 'lb': #Load Byte
    itype = 'I'
    opcode = 0x20
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  elif command == 'lbu': #Load Byte Unsigned
    itype = 'I'
    opcode = 0x24
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  elif command == 'lhu': #Load Halfword Unsigned
    itype = 'I'
    opcode = 0x25
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  elif command == 'lh': #Load Halfword 
    itype = 'I'
    opcode = 0x21
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  elif command == 'lui': #Load Upper Immediate
    itype = 'I'
    opcode = 0x0F
    reg_t = register(words[1])
    imm = int(words[2], 16)
  elif command == 'lw': #Load Word
    itype = 'I'
    opcode = 0x23
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  elif command == 'mfhi': #Move from HI Register
    itype = 'R'
    funct = 0x10
    reg_d = register(words[1])
  elif command == 'mthi': #Move to HI Register
    itype = 'R'
    funct = 0x11
    reg_s = register(words[1])
  elif command == 'mflo': #Move from LO Register
    itype = 'R'
    funct = 0x12
    reg_d = register(words[1])
  elif command == 'mtlo': #Move to LO Register
    itype = 'R'
    funct = 0x13
    reg_s = register(words[1])
  elif command == 'mfc0': #Move from Coprocessor 0
    itype = 'R'
    opcode = 0x10
  elif command == 'mult': #Multiply
    itype = 'R'
    funct = 0x18
    reg_s = register(words[1])
    reg_t = register(words[2])
  elif command == 'multu': #Unsigned Multiply
    itype = 'R'
    funct = 0x19
    reg_s = register(words[1])
    reg_t = register(words[2])
  elif command == 'nor': #Bitwise NOR (NOT-OR)
    itype = 'R'
    funct = 0x27
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'xor': #Bitwise XOR (Exclusive-OR)
    itype = 'R'
    funct = 0x26
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'or': #Bitwise OR
    itype = 'R'
    funct = 0x25
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'ori': #Bitwise OR Immediate
    itype = 'I'
    opcode = 0x0D
    reg_t = register(words[1])
    reg_s = register(words[2])
    imm = int(words[3], 16)
  elif command == 'sb': #Store Byte
    itype = 'I'
    opcode = 0x28
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  elif command == 'sh': #Store Halfword
    itype = 'I'
    opcode = 0x29
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  elif command == 'slt': #Set to 1 if Less Than
    itype = 'R'
    funct = 0x2A
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'slti': #Set to 1 if Less Than Immediate
    itype = 'I'
    opcode = 0x0A
    reg_t = register(words[1])
    reg_s = register(words[2])
    imm = int(words[3], 16)
  elif command == 'sltiu': #Set to 1 if Less Than Unsigned Immediate
    itype = 'I'
    opcode = 0x0B
    reg_t = register(words[1])
    reg_s = register(words[2])
    imm = int(words[3], 16)
  elif command == 'sltu': #Set to 1 if Less Than Unsigned
    itype = 'R'
    funct = 0x2B
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'sll': #Logical Shift Left
    itype = 'R'
    opcode = 0x00
    reg_d = register(words[1])
    reg_t = register(words[2])
    shift_amount = int(words[3], 16)
  elif command == 'srl': #Logical Shift Right (0-extended)
    itype = 'R'
    funct = 0x02
    reg_d = register(words[1])
    reg_t = register(words[2])
    shift_amount = int(words[3], 16)
  elif command == 'sra': #Arithmetic Shift Right (sign-extended)
    itype = 'R'
    funct = 0x03
    reg_d = register(words[1])
    reg_t = register(words[2])
    shift_amount = int(words[3], 16)
  elif command == 'sub': #Subtract
    itype = 'R'
    funct = 0x22
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'subu': #Unsigned Subtract
    itype = 'R'
    funct = 0x23
    reg_d = register(words[1])
    reg_s = register(words[2])
    reg_t = register(words[3])
  elif command == 'sw': #Store Word
    itype = 'I'
    opcode = 0x2B
    reg_t = register(words[1])
    imm = int(words[2], 16)
    reg_s = register(words[3])
  if itype == 'R':
    return(opcode*2**26 + reg_s*2**21 + reg_t*2**16 + reg_d*2**11 + shift_amount*2**6 + funct)
  elif itype == 'I':
    return(opcode*2**26 + reg_s*2**21 + reg_t*2**16 + imm)
  elif itype == 'J':
    return(opcode*2**26 + address)
  else:
    print('ERROR: Something went wrong with '+asm)
  return(result)

#Convert asssembly (or hex) to gameshark code
def asm_to_gameshark(ram_address, asm):
  if len(asm) == 1: #Handle single lines
    asm = [asm]
  gameshark_code = [] #List to hold output
  current_byte = 0 #Track memory address where GS code is going
  for asm_line in asm: #Loop through each ASM instruction
    if type(asm_line) == str: #If ASM is a string
      asm_converted_to_hex = assembler(asm_line) #Run the assembler to convert asm to hex
    elif type(asm_line) == int: #If ASM already is in hex
      asm_converted_to_hex = asm_line #Just use the existing hex
    #asm_converted_to_hex_str = hex(asm_converted_to_hex)[2:].upper() #Convert hex for ASM instruction into a string
    asm_converted_to_hex_str = hex(asm_converted_to_hex)[2:].zfill(8).upper()
    if asm_converted_to_hex_str == '00000000': #Ensure NOPs are 1 line to shorten codes
      gameshark_code.append('81'+hex(ram_address+current_byte)[4:].upper()+' 2400') #Write first 16 bits of 32 bit ASM instruction as an 81 type gs code
      current_byte = current_byte + 4 #Increment current byte      
    else:
      gameshark_code.append('81'+hex(ram_address+current_byte)[4:].upper()+' '+asm_converted_to_hex_str[0:4]) #Write first 16 bits of 32 bit ASM instruction as an 81 type gs code
      current_byte = current_byte + 2 #Increment current byte
      gameshark_code.append('81'+hex(ram_address+current_byte)[4:].upper()+' '+asm_converted_to_hex_str[4:8]) #Write last 16 bits of 32 bit ASM instruction as an 81 type gs code
      current_byte = current_byte + 2
  return gameshark_code



#Functions to insert instrucitons or data into the rom, shamelessly ripped from Micro500's micro mountain python scirpt
def mem_read_u32_be(addr, data):
  return struct.unpack(">I",data[addr:addr+4])[0]
  
def mem_read_u16_be(addr, data):
  return struct.unpack(">H",data[addr:addr+2])[0]
  
def u16_to_le(data):
    return struct.pack("<H",data)

def u16_to_be(data):
    return struct.pack(">H",data)

def s16_to_be(data):
    return struct.pack(">h",data)

def u32_to_be(data):
    return struct.pack(">I",data)
  
def mem_fill(data, start_addr, end_addr, value):
  return data[0:start_addr] + (bytes([value] * (end_addr - start_addr))) + data[end_addr:len(data)]
  
def mem_write_u32_be(addr, value, data):
  return data[0:addr] + u32_to_be(value) + data[(addr+4):len(data)]

def mem_write_u16_be(addr, value, data):
  return data[0:addr] + u16_to_be(value) + data[(addr+2):len(data)]
  
def mem_write_u8_be(addr, value, data):
  return data[0:addr] + u8_to_be(value) + data[(addr+1):len(data)]

def mem_write_16(addr, value, data):
  return data[0:addr] + value + data[(addr+2):len(data)]

# #Convert Gameshark like script into ASM (AKA compile)
# def script_to_asm(script):
#   line = 1
#   script_to_asm = []
#   for script_line in script:
#     words = script_line.split().lower()
#     if words[1] == 'if':
#       #do stuff
#     elif words[1] == 'while':
#       #do stuff
#     elif words[1] == 'for':
#       #do stuff


#Convert any 50 type gameshark codes into their many codes equivilent
def convert_50_type_gameshark_codes(gameshark_codes):
  updated_gameshark_codes = []
  last_code_type = ''
  for i in range(len(gameshark_codes)):
    gameshark_code = gameshark_codes[i]
    if gameshark_code[0:2] == '50':
      next_gameshark_code = gameshark_codes[i+1]
      n_addresses = int(gameshark_code[4:6], 16)
      address_offset = int(gameshark_code[6:8], 16)
      increment_value = int(gameshark_code[9:13], 16)
      if increment_value >= 0x8000: #Handle using signed values to go negative
        increment_value = 0x8000 - increment_value
      code_type = next_gameshark_code[0:2]
      address = int(next_gameshark_code[2:8], 16)
      code_value = int(next_gameshark_code[9:13], 16)
      for j in range(n_addresses):
        updated_gameshark_codes.append((code_type + format(address + j*address_offset, '06x') + ' ' + format(code_value + j*increment_value, '04x')).upper())
    if gameshark_code[0:2] != '50':
      if i == 0:
        updated_gameshark_codes.append(gameshark_code)
      elif gameshark_codes[i-1][0:2] != '50':
        updated_gameshark_codes.append(gameshark_code)
  return updated_gameshark_codes




#Convert gameshark codes to asm/hex
def gameshark_to_hex(gameshark_codes, boot=False): #, rom_jumps=False, end_of_rom_address=0x0):
    gameshark_codes = convert_50_type_gameshark_codes(gameshark_codes)
    line = 1
    last_code_type = '80'
    int_last_mem_address = 000000
    code_before_last_code_type = '80'
    code_value = 0000
    gameshark_hex = []
    for gameshark_code in gameshark_codes: #Build the code handler
      code_type = gameshark_code[0:2]
      mem_address = gameshark_code[2:8]
      try:
        int_mem_address = int(gameshark_code[2:8], 16)
        mem_address_suffix = int(gameshark_code[4:8], 16)
        if mem_address_suffix >= 0x8000:
          mem_address_prefix = 0x8001 + int(gameshark_code[2:4], 16)
        else:
          mem_address_prefix = 0x8000 + int(gameshark_code[2:4], 16)
        if code_type == '80' or code_type == 'A0' or code_type == 'F0' or code_type == 'D0' or code_type == 'D2':
          code_value = int(gameshark_code[11:13], 16)
        elif code_type == '81' or code_type == 'A1' or code_type == 'F1' or code_type == 'D1' or code_type == 'D3':
          code_value = int(gameshark_code[9:13], 16)
        if boot == False:
          if (code_type == '81' or code_type == 'A1') and (last_code_type == '81' or last_code_type == 'A1') and code_type_before_last_code_type[0] != 'D' and int_mem_address - int_last_mem_address == 2 and int_last_mem_address % 4 == 0: #For two 81 type codes that combined write a word to memory, write the actual word to memory 
            gameshark_hex = gameshark_hex[:-3] #Remove previous 81 code
            gameshark_hex.append(0x3C1A0000 + mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0x3C1B0000 + last_code_value) #LUI $K1 0xXXXX
            gameshark_hex.append(0x377B0000+code_value) #ORI $K1 $K1 0x0000
            gameshark_hex.append(0xAF5B0000+last_mem_address_suffix) #SW $K1 0xXXXX ($K0)
          elif code_type == '81' and code_value == '2400' and int_mem_address % 4 == 0 and last_code_type[0] != 'D': #Use $zero for NOPs
            gameshark_hex.append(0x3C1A0000+mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0xAF400000+last_mem_address_suffix) #SW $zero 0xXXXX ($K0)
          elif code_type == '80' or code_type == 'A0':
            gameshark_hex.append(0x3C1A0000+mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0x241B0000+code_value) #ADDIU $K1 $ZERO, 0x00XX
            gameshark_hex.append(0xA35B0000+mem_address_suffix) #SB $K1 0xXXXX ($K0)
            if last_code_type[0] == 'D': #If last code type was a conditional, add a NOP
              gameshark_hex.append(0x00000000) #Do nothing
          elif code_type == '81' or code_type == 'A1':
            gameshark_hex.append(0x3C1A0000+mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0x241B0000+code_value) #ADDIU $K1 $ZERO 0xXXXX
            gameshark_hex.append(0xA75B0000+mem_address_suffix) #SH $K1 0xXXXX ($K0)
            if last_code_type[0] == 'D': #If last code type was a conditional, add a NOP
              gameshark_hex.append(0x00000000) #Do nothing
          elif code_type == 'D0':
            gameshark_hex.append(0x3C1A0000+mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0x935A0000+mem_address_suffix) #LBU $K0 0x0000 ($K0)
            gameshark_hex.append(0x241B0000+code_value) #ADDIU $K1 $ZERO 0x00XX
            gameshark_hex.append(0x175B0003) #BNE $K0 $K1 0x0004
          elif code_type == 'D1':
            gameshark_hex.append(0x3C1A0000+mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0x975A0000+mem_address_suffix) #LHU $K0 0xXXXX ($K0)
            gameshark_hex.append(0x241B0000+code_value) #ADDIU $K1 $ZERO 0xXXXX
            gameshark_hex.append(0x175B0003) #BNE $K0 $K1 0x0004
          elif code_type == 'D2':
            gameshark_hex.append(0x3C1A0000+mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0x935A0000+mem_address_suffix) #LBU $K0 0x0000 ($K0)
            gameshark_hex.append(0x241B0000+code_value) #ADDIU $K1 $ZERO 0x00??
            gameshark_hex.append(0x135B0003) #BEQ $K0 $K1 0x0004
          elif code_type == 'D3':
            gameshark_hex.append(0x3C1A0000+mem_address_prefix) #LUI $K0 0xXXXX
            gameshark_hex.append(0x975A0000+mem_address_suffix) #LHU $K0 0x0000 ($K0)
            gameshark_hex.append(0x241B0000+code_value) #ADDIU $K1, $ZERO, 0xXXXX
            gameshark_hex.append(0x135B0003)#BEQ $K0, $K1, 0x0004
          elif code_type == 'F0' or code_type == 'F1' or code_type == 'EE' or code_type == 'FF' or code_type == 'DE':
            0 #Do nothing
          else:
            print('WARNING:  Line '+str(line)+ '('+gameshark_code+') in Gameshark code list is invalid.')
        elif boot == True:
          if (code_type == 'F1') and (last_code_type == 'F1') and int_mem_address - int_last_mem_address == 2 and int_last_mem_address % 4 == 0: #For two F1 type codes that combined write a word to memory, write the actual word to memory
            gameshark_hex = gameshark_hex[:-3] #Remove previous F1 code
            gameshark_hex.append(0x3C040000+mem_address_prefix) #LUI $a0 0xXXXX
            gameshark_hex.append(0x3C050000+last_code_value) #LUI $a1 0xXXXX
            gameshark_hex.append(0x34A50000+code_value) #ORI $a1 $a1 0x0000
            gameshark_hex.append(0xAC850000+last_mem_address_suffix) #SW $a1 0xXXXX ($a0)
          elif code_type == 'F0': #8 bit write at boot
            gameshark_hex.append(0x3C040000+mem_address_prefix) #LUI $a0 0xXXXX
            gameshark_hex.append(0x24050000+code_value) #ADDIU $a1 $ZERO, 0x00XX
            gameshark_hex.append(0xA0850000+mem_address_suffix) #SB $a1 0xXXXX ($a0)
          elif code_type == 'F1': #16 bit write at boot
            gameshark_hex.append(0x3C040000+mem_address_prefix) #LUI $a0 0xXXXX
            gameshark_hex.append(0x24050000+code_value) #ADDIU $a1 $ZERO 0xXXXX
            gameshark_hex.append(0xA4850000+mem_address_suffix) #SH $a1 0xXXXX ($a0)
          elif code_type == 'EE': #Disable expansion pak
            gameshark_hex.append(0x3C048000) #LUI $a0 0x8000 
            gameshark_hex.append(0x3C050040) #LUI $a1 0x0040
            gameshark_hex.append(0xAC850318) #SW $a1 0x0318 ($a0)
        line = line + 1
        code_type_before_last_code_type = last_code_type
        last_code_type = code_type
        int_last_mem_address = int_mem_address
        last_mem_address_suffix = mem_address_suffix
        last_code_value = code_value
        # if rom_jumps and line % 5 and line != 0: #Add in jumps if running directly from rom to force the N64 to load the codes into the N64 cache, needed to work on console when running from rom
        #   size_gs_codes = len(gameshark_hex)*4 #Get size of gs hex instructions
        #   jump_to_this_rom_address = format(end_of_rom_address + len(gameshark_hex)*4 + 0x10 + 0xB0000000, '08x') #Set up address to jump to (really just two instructions below the jump)
        #   code = [
        #     'LUI $k0 0x'+jump_to_this_rom_address[0:4],
        #     'ORI $k0 $k0 0x'+jump_to_this_rom_address[4:8],
        #     'JR $k0',
        #     'NOP',
        #   ]
        #   gameshark_hex = gameshark_hex + code #Append jump  to gameshark hex
      except:
        print('Ignoring line '+str(line)+' which does not appear to be a Gameshark code: "'+gameshark_code+'"')

    gameshark_hex.append(0x00000000)
    return gameshark_hex



#Class handles everything for patching a rom
class rom:
  def __init__(self, file_name): 
    self.load(file_name)
    self.rom_to_ram = mem_read_u32_be(0x8, self.data) - 0x1000 #Grab converstion of RAM to ROM (negative to go ROM to RAM) from ram address of the bootcode at 0x8 in the rom
    self.ram_start = mem_read_u32_be(0x8, self.data)
    print('Rom-to-ram = ', hex(self.rom_to_ram))
    print('Start ram is ', hex(self.ram_start))
    self.ram_to_rom = - self.rom_to_ram
    self.rom_end = len(self.data) #Count the number of bytes in the rom
    self.file_name = path.split(file_name)[-1] #Save filename of rom, only grabbing the last part of a path
  def load(self, file_name): #Load rom data from file (.z64)
    rom_file = open(file_name, 'rb')
    self.data = rom_file.read()
    rom_file.close()
  def save(self, file_name, checksum=True): #Save a patched rom
    if checksum:
      self.fix_checksum() #Fix checksum before saving patched rom (important this is the last step before saving the rom)
    patched_rom_file = open(file_name, 'wb')
    patched_rom_file.write(self.data)
    patched_rom_file.close()
  def insert_hex(self, addr, hexcode): #Insert 32 bit MIPs instruction(s) or data in hex format into rom
      if type(hexcode) == int:  #If there is only one line
        self.data =  mem_write_u32_be(addr, hexcode, self.data)#Insert a single 32 bit value into ram
      else: #If there are multiple lines
        for line in hexcode: #Loop through each line
          self.data =  mem_write_u32_be(addr, line, self.data)#Insert a single 32 bit value into ram
          addr += 4 #Go to next line
  def insert_code(self, addr, code):
      try:
        if type(code) == int:
          self.data =  mem_write_u32_be(addr, code, self.data)#Insert a single 32 bit value into ram
        elif type(code) == str:  #If there is only one line
          self.data =  mem_write_u32_be(addr, assembler(code), self.data)#Insert a single 32 bit value into ram
      except:
        print('INSERT CODE ERROR: ', hex(code))
      else: #If there are multiple lines
        line_number = 0
        for line in code: #Loop through each line
          line_number += 1
          try:
            if type(line) == int:
              self.data =  mem_write_u32_be(addr, line, self.data)#Insert a single 32 bit value into ram
              #print('Inserting ', '0x'+format(line, '08x').upper(), ' into rom at ', '0x'+format(addr, '08x').upper())
            elif type(line) == str:
              self.data =  mem_write_u32_be(addr, assembler(line), self.data)#Insert a single 32 bit value into ram
              #print('Inserting ', line, ';', '0x'+format(assembler(line), '08x').upper(), ' into rom at ', '0x'+format(addr, '08x').upper())
          except:
            if type(line) == int:
              print('INSERT CODE ERROR ON LINE '+str(line_number)+': ', hex(line))
            else:
              print('INSERT CODE ERROR ON LINE '+str(line_number)+': ', line)
          addr += 4 #Go to next line  
  def insert_codeblock(self, hook_addr, codeblock_addr, codeblock, jump_addr=0, offset=0, ignore_offset=False): #Insert a block of custom code with a hook (and custom jump back if you want)
    hook_instructions = [0x08000000 + int((codeblock_addr + self.rom_to_ram - 0x80000000)/4),0x00000000]
    self.insert_code(hook_addr, hook_instructions)
    if jump_addr == 0: #If no jump address is specified, just jump back to right after the hook
      jump_back = [0x08000000 + 1 + int((hook_addr + self.rom_to_ram - 0x80000000)/4), 0x00000000]
    else: #Else use the specified jump address
      jump_back = [0x08000000 + int((jump_addr + self.rom_to_ram - 0x80000000)/4), 0x00000000]
    self.insert_code(codeblock_addr, codeblock + jump_back)    
  def insert_gameshark(self, hook_addr, codehandler_addr, gameshark_codes): #Insert a gameshark code handler engine along with desired codes
    gameshark_hex = gameshark_to_hex(gameshark_codes)
    self.insert_codeblock(hook_addr, codehandler_addr, gameshark_hex) #Insert the gameshark code handler block into the rom with a hook
  def fix_checksum(self):   #Fix checksum for rom, shamelessly ripped from Micro500's micro mountain python scirpt
      c1, c2 = n64crc.crc(self.data)
      self.data = mem_write_u32_be(0x10, c1, self.data)
      self.data = mem_write_u32_be(0x14, c2, self.data)
  def get_crc(self): #Get the checksum and return c1 and c2, used for checking what rom it is
    c1, c2 = n64crc.crc(self.data)
    return c1, c2
  def disable_internal_aa(self): #Loops through entire rom and disables internal AA from the F3DEX microcode (see https://www.assembler-games.com/threads/is-it-possible-to-disable-anti-aliasing-in-n64-games-via-gameshark-cheats.59916/page-3#post-860932)
    rom_size = len(self.data)
    for addr in range(0x0, rom_size, 0x4): #Loop through entire rom
      instruction = mem_read_u32_be(addr, self.data)
      if instruction == 0xB900031D:
        print('------------')
        next_instruction =  mem_read_u32_be(addr + 0x4, self.data)
        # if next_instruction & (1 << 3): #If 3rd bit is set (internal AA is on)
        #   print('Changed ', hex(next_instruction))
        #   next_instruction = next_instruction - 0x8 #Turn internal AA off
        #   print('into ', hex(next_instruction))
        #   self.data = mem_write_u32_be(addr + 0x4, next_instruction, self.data)
        if  (next_instruction & (1 << 4)): #If 3rd bit is set (internal AA is on)
          print('Changed ', hex(next_instruction))
          next_instruction = next_instruction - 0x10   #do some random ass thing
          print('into ', hex(next_instruction))
          self.data = mem_write_u32_be(addr + 0x4, next_instruction, self.data)
  def get_address(self, instruction): #Grab and return the rom address of an instruction
    if not type(instruction) == int: #Convert instruction to hex if not done already
      intruction = assembler(instruction)
    rom_size = len(self.data)
    for addr in range(0x0, rom_size, 0x4): #Loop through entire rom
      if instruction == mem_read_u32_be(addr, self.data): #If the instruction matches, return the address
        return(addr)
  def get_instruction(self, rom_address): #Returns an instruction at a given rom address
    instruction = mem_read_u32_be(rom_address, self.data)
    return instruction
  def get_instructions(self, rom_address, size): #Returns a set of instructions given a rom address and size in number of bytes
    instructions = []
    for i in range(0x0, size, 0x4):
      instruction = mem_read_u32_be(rom_address + i, self.data)
      instructions.append(instruction)
    return instructions