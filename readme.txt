The Nintendo 64 Gameshark Code Injector v3.3

by Triclon

E-mail - triclon@gmail.com
Website - https://triclon.neocities.org

This utility will inject Gameshark codes directly into most Nintendo 64 roms.  It is console compatible with a flashcart and works in most emulators.  Right after a game boots, the injector will run and copy the code handler, which runs through all the active codes continuously, into the Expansion Pak RAM.  The code handler hooks into the game's exception handler and will run continuously, applying active codes.  It will also run any F0 or F1 type codes at boot.  Unlike a real Gameshark, which is limited to a few hundred lines of code, this injector allows you to inject nearly unlimited lines of Gameshark codes.  


Requirements:

-Python 3 to run the Injector
-A Nintendo 64 ROM to patch
-An Expansion Pak and flash drive to play on console


Get Gameshark codes:

I highly recommend http://gamehacking.org, the primer archive of cheat codes on the internet.  You can export them in a variety of formats.


How to run:

Put your Gameshark codes into "gameshark_code.txt"

Copy a ROM into this directory and name it "rom.z64"

Open a terminal and type the following...

   python gameshark_code_injector.py

It will generate a rom called "rom_patched.z64"

Open your newly patched rom in your favorite emulator or copy to a flash drive for console and enjoy playing!


Supported Gameshark code types:

80, 81, D0, D1, D2, D3, F0, F1, A0, A1, FF, EE, DE


Troubleshooting:

If your game does not boot, check the following
-On emulator: Make sure the expansion pak (8 MB) is enabled.  Enable Interpreter Mode, or disabled "DynaRec" or Dynamic Recompiling modes of your emulator.
-On console: You will need the Expansion Pak (for the most part, see "Advanced Stuff" below for a possible workaround)
-If the injector gives you the error "ERROR: No exception handler found!" your rom is not compatible with the Gameshark Code Injector.  This is because not every rom boots the same way.  Please contact me with information about the rom you are trying to patch, and I will try to see if I can hardcode a solution.
-Sometimes if a game won't boot or Gameshark codes not work, be sure you are you using the proper enable/master codes.  These will be F0, F1, EE, FF, and/or DE type codes.  Be sure to include them.
-If the game uses the expansion pak and there is an enable code that looks like F0000319 0078 and it does not boot, you might also need to add the following additional enable code: FF780000 0000.


Wondering how Gameshark codes work?  Check out the following links:

EnHacklopedia - http://www.bsfree.org/hack/hacking_n64.html
The Secrets of Processional Gameshark Hacking - http://viper.shadowflareindustries.com/?file=hackv500c.html&cat=hax0r


Advanced Stuff:

-Making compatible without the expansion pak
For the most part, this Gameshark Code Injector uses the Expansion Pak RAM starting at 0x80400000 to store the active codes when the game is running.  However, it is possible to get it to run on console with just the Jumper Pak.  First you need to find a location in the RAM the game does not use.  You can search around with something like the Project 64 debugger memory viewer, or even the Gameshark's own memory viewer.  Be aware that you also must have sufficient space in ram to store the number of Gameshark codes you wish to inject.  Once you are sure you have found an area of RAM  you are confident the game will never use, you want to point to at the beginning of that location with an FF type enable code.  I will use the enable code FFXXXXXX 0000 where XXXXXX is the last 6 digits of the where in the ram I want to put my code handler.  For example, if my game does not use the last 1 kb of ram between 0x803FF000 and 0x80400000, I will include the enable code FF3FF000 0000.

-Limitations on the number of codes and reducing lag
The N64 Gameshark Code Injector allows a nearly unlimited amount of Gameshark codes to be injected into a rom.  There are a few limitations to this.  First is the amount of RAM available.  With each GS code taking up 3-4 bytes of memory, you could theoretically inject over 1 million GS codes into the 4 MB of Expansion Pak RAM.  Stress testing shows that over 25,000 lines of GS code starts to cause a game to lag on console.  Over 100,000 GS codes will lag the game enough to make it unplayable.  This probably is not so much of a problem for emulators.  The Code Injector will try to optimize 16 bit codes that are next to each other in ram that form 32 bit words (e.g. MIPS assembly type codes) to reduce the code handler size and lag.

-Arbitrary code injection-
F0 and F1 type Gameshark codes are run only at boot and directly from the ROM.  This means you can theoretically inject as many F0 and F1 type codes as you want with no RAM or lag limitations.  Oftentimes 80, 81, A0, or A1 type codes can be converted to F0 or F1 type codes.  If any of these codes are derived from MIPS assembly, you can probably simply replace the 8 or A with an F and it would work fine.  It is feasible that large ram hacks can be injected in this way.  Future versions might allow assembly injection, if this feature is requested enough.


Changelog
-Dec. 17, 2022 - v3.3 - Major bug fixes. DE type enable codes should now work correctly and fixed a bug where a bad gameshark code, comment, or empty line in the gameshark codes list would cause all the subsequent codes to not get injected.
-Dec. 16, 2022 - v3.2 - Fixed compatibility issue with Goldeneye involving not all exception handler hooks being used. I put in checks for each hook.  Might also fix other games.
-Nov. 29, 2022 - v3.1 - Added compatibility with Shadows of the Empire (U) v1.0, v1.1, & v1.2.
-Nov. 27, 2022 - v3.0 - Added compatibility for Mario Tennis (USA) and Perfect Dark (USA) with hardcoded solutions.  Future versions will hopefully increase compatibility further.  Modified how the Gameshark Code Injector runs at boot to for increased compatibility and in-game performance.  Now you can add comments and blank lines to your gameshark codes and the injector will ignore them instead of crashing.
-Dec. 7, 2021 - v2.0 - Now supports almost every game and many more code types including F0, F1, A0, A1, FF, EE, and DE.
-Oct. 29, 2021 - Mario Golf version created.
-Jan 6, 2020 - v1.0 - Initial Release (MK64 version)


Acknowledgements:

This Gameshark Code Injector is based on my Mario Kart 64 Gameshark Code Injector, on the prompting of sdqfsdf and Fancy247 to create a way to use gameshark codes to import Gameboy characters into Mario Golf. I later expanded it to to be compatible with more games and code types.  It took me a long time to figuring out how to get all the pieces of this injector to work, so I hope you enjoy it.

Additional thanks to...
-DKO for porting Parasyte's n64crc program from c to python.  Originally based on uCON64's N64 checksum algorithm by Andreas Sterbenz.
-Viper187 and Parasyte for writing EnHacklopedia (see link later in readme) which was invaluable in helping me learn how the Gameshark actually works.
-Micro500 for snippets of python code that I borrowed from his Micro Mountain code to read/write N64 roms in python.
-Datel and Interact for creating the Nintendo 64 Gameshark/Action Replay
