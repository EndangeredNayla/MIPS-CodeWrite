#Patch Gameshark Codes into 

#Modify these 
input_file = 'rom.z64'
output_file = 'rom_patched.z64'
gameshark_file = 'gameshark_codes.txt'


#Import python libraries
import sys
import mk64_lib


#Load rom
rom = mk64_lib.rom(input_file)
end_of_rom_address = rom.rom_end

c1, c2 = rom.get_crc()
print('Checking ROM Checksums')
print('c1= ', hex(c1))
print('c2= ', hex(c2))


#Open text file comtaining Gameshark codes
with open(gameshark_file) as f:
    gameshark_codes = f.read().splitlines()

#Convert gameshark to hex
gameshark_hex = mk64_lib.gameshark_to_hex(gameshark_codes)
boot_gameshark_hex = mk64_lib.gameshark_to_hex(gameshark_codes, boot=True)


#gameshark_code_engine_start_address = 0x80400000 #Normally the start of the expansion pack address, for non expansion pak enabled games
for gameshark_code in gameshark_codes:  #Check gameshark code list for specific enable codes
    code_type = gameshark_code[0:2]
    if code_type == 'FF':# But if an FF type code is specified, use that address instead
        gameshark_code_engine_start_address = 0x80000000 + int(gameshark_code[2:8], 16)
        print('FF type enable code detected.  Code engine will be loaded into ram at '+hex(gameshark_code_engine_start_address)+'.')
    if code_type == 'DE': #Support for DE type enable code that specify where the 1st MB of the game starts in ram, and the rom-to-ram conversion
        rom.ram_start = 0x80000000 + int(gameshark_code[2:8], 16)
        rom.rom_to_ram = rom.ram_start - 0x1000
        rom.ram_to_rom = -rom.rom_to_ram
        print('DE type enable code detected.  1st MB of game should load into ram at '+hex(rom.ram_start)+'.')





if c1 == 0x5001cf4f and c2 == 0xf30cb3bd: #MARIO TENNIS (USA)
    print('Found Mario Tennis (USA).  Use hardcoded boot hooks.')
    hardcoded_boot_hooks = True
    #Where to put the gameshark engine
    gameshark_code_engine_start_address = 0x80500000 #Normally the start of the expansion pack address, for non expansion pak enabled games
    #Exception handler info
    exception_handler_address = 0x800418F0
    #After decompression hook for after the game decompresses the 1st MB of the rom in the ram
    after_decompression_hook = 0x1070
    after_decompression_hook_overwrite = 0x8
elif (c1 == 0xddf460cc and c2 == 0x3ca634c0) or (c1 == 0x41f2b98f and c2 == 0xb458b466): #Perfect Dark USA (v1.0 and v1.1)
    print('Found Perfect Dark (USA).  Use hardcoded boot hooks.')
    hardcoded_boot_hooks = True
    #Where to put the gameshark engine
    gameshark_code_engine_start_address = 0x8075c000 #Normally the start of the expansion pack address, for non expansion pak enabled games
    #Exception handler info
    exception_handler_address = 0x80003500
    #After decompression hook for after the game decompresses the 1st MB of the rom in the ram
    after_decompression_hook = 0x16AC
    after_decompression_hook_overwrite = 0x10
elif c1==0x264d7e5c and c2==0x18874622:
    print('Found Shadows of the Empire (USA) v1.0.  Use hardcoded boot hooks.')
    hardcoded_boot_hooks = True
    #Where to put the gameshark engine
    gameshark_code_engine_start_address = 0x80500000  #Normally the start of the expansion pack address, for non expansion pak enabled games
    #Exception handler info
    exception_handler_address = 0x800C37C0
    #After decompression hook for after the game decompresses the 1st MB of the rom in the ram
    after_decompression_hook = 0x1D7C
    after_decompression_hook_overwrite = 0x8
elif c1==0x4147b091 and c2==0x63251060:
    print('Found Shadows of the Empire (USA) v1.1.  Use hardcoded boot hooks.')
    hardcoded_boot_hooks = True
    #Where to put the gameshark engine
    gameshark_code_engine_start_address = 0x80500000  #Normally the start of the expansion pack address, for non expansion pak enabled games
    #Exception handler info
    exception_handler_address = 0x800C3820
    #After decompression hook for after the game decompresses the 1st MB of the rom in the ram
    after_decompression_hook = 0x1D7C
    after_decompression_hook_overwrite = 0x8
elif c1==0x4dd7ed54 and c2==0x74f9287d:
    print('Found Shadows of the Empire (USA) v1.2.  Use hardcoded boot hooks.')
    hardcoded_boot_hooks = True
    #Where to put the gameshark engine
    gameshark_code_engine_start_address = 0x80500000  #Normally the start of the expansion pack address, for non expansion pak enabled games
    #Exception handler info
    exception_handler_address = 0x800C3FE0
    #After decompression hook for after the game decompresses the 1st MB of the rom in the ram
    after_decompression_hook = 0x1D7C
    after_decompression_hook_overwrite = 0x8
elif c1==0x1fbaf161 and c2==0x2c1c54f1: #1080 Snowboarding (U/JP)
    print('1080 Snowboarding (U/JP) Found.  Use hardcoded exception handler adderess since auto finding it does not work.')
    rom.ram_start = 0x80000400
    rom.rom_to_ram = rom.ram_start - 0x1000
    #rom.ram_to_rom = -rom.rom_to_ram
    exception_handler_preamble_hook = 0xE4F6D4 + rom.rom_to_ram
    exception_handler_address = exception_handler_preamble_hook + 0x8 
    gameshark_code_engine_start_address = 0x80500000
    hardcoded_boot_hooks = False
else: #If rom has no hardcoded solution, first try to find the exception handler and patch that, this is the default behavior for most games
    print('Trying to find exception handler in ROM.')
    try:
        exception_handler_preamble_hook = rom.get_address(0x03400008) + rom.rom_to_ram #- 0x100000
    except:
        print('ERROR: No exception handler found!  Unfortantely patching this rom will not work.')
        print('Make sure your rom is Big Endian (.z64) format.  If you are sure it is, please')
        print('contact Triclon with information about the rom you are trying to patch to see')
        print('if a hardcoded solution can be found as the current version of the gameshark code')
        print('injector is not compatible with this rom.')
        sys.exit(1) # exiting with a non zero value is better for returning from an error
    exception_handler_address = exception_handler_preamble_hook + 0x8 #- 0x100000
    gameshark_code_engine_start_address = 0x80500000
    hardcoded_boot_hooks = False
    print('Exception handler found in rom!')
    print('Exception handler rom address: '+hex(exception_handler_address - rom.rom_to_ram))
    print('Exception handler ram address: '+hex(exception_handler_address))
    print('Will hook into that.')


if hardcoded_boot_hooks: #Set a few things if the boot hooks are hardcoded (e.g. Mario Tennis (USA))
    exception_handler_preamble_hook = exception_handler_address - 0x8 
    after_decompression_overwritten_instrictions = rom.get_instructions(after_decompression_hook, after_decompression_hook_overwrite)



#BOOT HOOK USED FOR ALL(?) GAMES
boot_hook = 0x1000
boot_hook_overwrite = 0x50 #Most (ALL?) games including Zelda OOT
boot_overwritten_instrictions = rom.get_instructions(boot_hook, boot_hook_overwrite)






romaddr_hex_str = format(end_of_rom_address + 0xB0000000, '08x')  #The rest of this code creates the code to copy from rom into ram using dma copy
ramaddr_hex_str = format(gameshark_code_engine_start_address, '08x')
# exceptionhadlerjumpbackaddr_hex_str = format(exception_handler_preamble_jumpback_address, '08x')



# #Inset code into rom to copy using DMA copy
payload_code = [
    'LUI $k0 0x8000', #Overwrite jump at 0x80000008 to set it back to 'JR $K0' (If hook exists)
    'LB $k0 0x0008 $k0',
    'ORI $k1 $zero 0x08',
    'BNE $k0 $k1 0x4', #Check if hook exists and ignore if it doesn't
    'LUI $k0 0x8000',
    'LUI $k1 0x0340', #Put the hex 0x03400008 for instruction 'JR $K0' into $k1
    'ORI $k1 $k1 0x0008',
    'SW $k1 0x0008 $k0', 

    'LUI $k0 0x8000', #Overwrite jump at 0x80000088 to set it back to 'JR $K0' (If hook exists)
    'LB $k0 0x0088 $k0',
    'ORI $k1 $zero 0x08',
    'BNE $k0 $k1 0x4',  #Check if hook exists and ignore if it doesn't
    'LUI $k0 0x8000',
    'LUI $k1 0x0340', #Put the hex 0x03400008 for instruction 'JR $K0' into $k1
    'ORI $k1 $k1 0x0008',
    'SW $k1 0x0088 $k0', #Overwrite jump at 0x80000088 to set it back to 'JR $K0'

    'LUI $k0 0x8000', #Overwrite jump at 0x80000108 to set it back to 'JR $K0'
    'LB $k0 0x0108 $k0',
    'ORI $k1 $zero 0x08',
    'BNE $k0 $k1 0x4', #Check if hook exists and ignore if it doesn't
    'LUI $k0 0x8000',
    'LUI $k1 0x0340', #Put the hex 0x03400008 for instruction 'JR $K0' into $k1
    'ORI $k1 $k1 0x0108',
    'SW $k1 0x0108 $k0', #Overwrite jump at 0x80000108 to set it back to 'JR $K0'

    #'SW $k1 0x0128 $k0', #Overwrite jump at 0x80000128 to set it back to 'JR $K0'
    'LUI $k0 0x'+format(exception_handler_preamble_hook, '08x')[0:4], #Overwrite exception handler preamble which will eventually get 'JR $K0' copied to 0x80000128
    'ORI $k0 $k0 0x'+format(exception_handler_preamble_hook, '08x')[4:8],
    'SW $k1 0x0000 $k0',
    'LUI $k1 0x'+format(0x08000000 + int((gameshark_code_engine_start_address + 0x7C - 0x80000000)/4), '08x')[0:4], #Put the hex jump to gameshark_hex at 0x80000188 overwriting the jump to this code
    'ORI $k1 $k1 0x'+format(0x08000000 + int((gameshark_code_engine_start_address + 0x7C - 0x80000000)/4), '08x')[4:8],
    'LUI $k0 0x8000',
    'SW $k1 0x0188 $k0', #Overwrite jump at 0x80000188 to set it back to 'JR $K0'
    ]+ gameshark_hex + [
    # 'J 0x80000120', #Jump back to exception handler
    #'j '+hex(exception_handler_address), #Add jump back to exception handler
    'LUI $k0 '+format(exception_handler_address, '08x')[0:4],
    'ORI $k0 $k0 '+format(exception_handler_address, '08x')[4:8],
    'JR $k0',
    'nop',
    #0x12345678, #Add key to check if gameshark code is properly copied to ram
    ]
rom.insert_code(end_of_rom_address, payload_code)

if hardcoded_boot_hooks: #If game needs to use hardcoded boot hooks

    stuff_to_run_after_decompression = [
        #Set jump to gameshark code, $a0 is the memory location of uncompressed code, $a1 is the jump instruction 'J 0x80400000' which in hex is 
        'addiu $sp $sp 0xFFC0', #-0x40
        'sw $A0 0x0000 $sp',
        'sw $A1 0x0004 $sp',
        'sw $A2 0x0008 $sp',
        'sw $A3 0x000C $sp',
         # #################
        'LUI $a0 0x'+hex(exception_handler_preamble_hook)[2:6],
        'ORI $a0 $a0 0x'+hex(exception_handler_preamble_hook)[6:10],

        'LW $a3 0x0000 $a0', #Make sure exception handler preamble is actually loaded (check for the preamble hook being "JR $RA"), needed for hooks that run a few times before data can be decompressed e.g. Perfect Dark
        'LUI $a2 0x0340',
        'ORI $a2 $a2 0x0008',      
        'BNE $a2 $a3 0x3',

        #'LUI $a1 0x0810',
        'LUI $a1 0x'+format(0x08000000+int((gameshark_code_engine_start_address-0x80000000)/4),'08x')[0:4],
        'ORI $a1 $a1 0x'+format(0x08000000+int((gameshark_code_engine_start_address-0x80000000)/4),'08x')[4:8],
        'SW $a1 0x0000 $a0',
         # #################
        'lw $A0 0x0000 $sp',  #First Load registers from stack
        'lw $A1 0x0004 $sp',
        'lw $A2 0x0008 $sp',
        'lw $A3 0x000C $sp',
        'addiu $sp $sp 0x40',
    ] + after_decompression_overwritten_instrictions #Run overwritten instructions which include a jump on where to go
    
    size_hex_str = format(int(len(payload_code)*4 + len(stuff_to_run_after_decompression)*4 - 4), '08x')
else:
    size_hex_str = format(int(len(payload_code)*4 - 4), '08x')


#Run boot code that was overwritten (starts at 0x6E0 and ends at 0x76C in rom)
stuff_to_run_at_boot = [
    #Store registers
    'addiu $sp $sp 0xFFC0', #-0x40
    'sw $A0 0x0000 $sp',
    'sw $A1 0x0004 $sp',
    'sw $A2 0x0008 $sp',
    'sw $A3 0x000C $sp',
    'sw $t0 0x0014 $sp',
    'sw $t1 0x0018 $sp',
    ] + boot_gameshark_hex  + [ #Add gameshark hex (F0 and F1 type codes usually) at boot
    #Initialize variables
    'lui $a0 0x'+romaddr_hex_str[0:4], #Load ROM source  //Inputs for DMA copy flipped from MK64 to Mario Golf
    'ori $a0 $a0 0x'+romaddr_hex_str[4:8],
    'lui $a1 0x'+ramaddr_hex_str[0:4],  #Load RAM destination
    'ori $a1 $a1 0x'+ramaddr_hex_str[4:8],
    'lui $a2 0x'+size_hex_str[0:4], #Load size
    'ori $a2 $a2 0x'+size_hex_str[4:8],
    'ori $t0 $zero 0x00', #Set index to zero
    ##Copy from ram to rom loop
    'lw $t1 0x0000 $a0', #Load from rom
    'addi $a0 $a0 0x4', #incriment rom address
    'sw $t1 0x0000 $a1', #Store to ram
    'addi $a1 $a1 0x4', #Incriment ram address
    'bne $t0 $a2 0xFFFB', #Do while index < size
    'addi $t0 $t0 0x4', #Increment index

    # #################
    # #Jump to copy code now in ram which will overwrite the above "run copy code"
    'lw $A0 0x0000 $sp',  #First Load registers from stack
    'lw $A1 0x0004 $sp',
    'lw $A2 0x0008 $sp',
    'lw $A3 0x000C $sp',
    'lw $t0 0x0014 $sp',
    'lw $t1 0x0018 $sp',
    'addiu $sp $sp 0x40',
] + boot_overwritten_instrictions #+ [ #Run instructions that were overwritten right after boot, they include a JR $T2 which will jump to wherever it needs to go, essentially jumping back from my boot hook without the need for me to do anything


if hardcoded_boot_hooks: #If game needs to use hardcoded boot hooks

    rom.insert_code(end_of_rom_address + len(payload_code)*4, stuff_to_run_after_decompression)

    #Insert jump to code that will run after decompression to put in a jump in the exception handler preamble
    rom.insert_code(after_decompression_hook, ['J '+hex(gameshark_code_engine_start_address + len(payload_code)*4), 'NOP'])
    # jump_here_hex = format(gameshark_code_engine_start_address + len(payload_code)*4, '08x')
    # code = [
    #     'LUI $t9 0x'+jump_here_hex[0:4],
    #     'ORI $t9 $t9 '+jump_here_hex[4:8],
    #     'JR $t9',
    #     'NOP',
    # ]
    # rom.insert_code(after_decompression_hook, code)


    #Hook intserted into the boot to jump to the bit of code in the rom to copy the gameshark hex to the 
    jump_to_boot_code = [
        'lui $t9 0x'+hex(end_of_rom_address + len(payload_code)*4 + len(stuff_to_run_after_decompression)*4+ 0xB0000000)[2:6],
        'ori $t9 $t9 0x'+hex(end_of_rom_address + len(payload_code)*4+ len(stuff_to_run_after_decompression)*4 + 0xB0000000)[6:10],
        'jr $t9',
        'nop',
    ]

    rom.insert_code(boot_hook, jump_to_boot_code)

    rom.insert_code(end_of_rom_address + len(payload_code)*4 + len(stuff_to_run_after_decompression)*4, stuff_to_run_at_boot)

else: #If game has an exception handler that can be found in the ram

    #Insert exception handler preamble hook into the rom since the exception handler was found in the rom
    code = ['j 0x'+ramaddr_hex_str]#, 'nop']
    rom.insert_code(exception_handler_preamble_hook + rom.ram_to_rom, code)

    #Hook intserted into the boot to jump to the bit of code in the rom to copy the gameshark hex to the 
    jump_to_boot_code = [
        'lui $t9 0x'+hex(end_of_rom_address + len(payload_code)*4 + 0xB0000000)[2:6],
        'ori $t9 $t9 0x'+hex(end_of_rom_address + len(payload_code)*4 + 0xB0000000)[6:10],
        'jr $t9',
        'nop',
    ]

    rom.insert_code(boot_hook, jump_to_boot_code)

    rom.insert_code(end_of_rom_address + len(payload_code)*4, stuff_to_run_at_boot)



#Save rom
rom.save(output_file, checksum=True)