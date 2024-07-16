How to go from a keymap.c to a hex file and upload it.

First. Place the keymap.c in a new folder under your keyboard folder in keyboards/ergodox_ez/keymaps.

Use the command

qmk compile -kb <keyboard> -km <keymap>

Example:

qmk compile -kb ergodox_ez -km keymap_qwerty_code

to compile the keymap (.c-file) to a .hex-file.
This will be stored in

/home/bugger/qmk_firmware

Then start the Teensy loader in 

/home/bugger/Documents/Thuis/keyboard/software_teensy/

by calling 

./teensy &

or calling 
/home/bugger/Documents/Thuis/keyboard/software_teensy/teensy &


Then a GUI pops up. Load the .hex file, and upload it to the keyboard.