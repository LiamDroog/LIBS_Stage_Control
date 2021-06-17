###################################################
README.txt
Information for utilizing the stage control program
###################################################
# Author:   Liam Droog
# Email:    droog@ualberta.ca
# Year:     2021
# Version:  V.1.0.0
###################################################

Launching from somewhere other than parent directory:

    Right click and create a shortcut for Launcher.bat to launch from anywhere on your system (desktop, likely.)
    Don't take it out of it's folder, otherwise it won't work!

First installation steps:

    Upon first installation, open a terminal window in the /LIBS_Stage_Control directory and run
    # pip install -r Requirements.txt
    You'll need to install h5py separately for python 3.8.10 because we can't have nice things.
    Either by whl or by pip it should work. If not, manually install everything until something breaks

From there, connect the stage control and to the computer via USB, and to power (12v/ max 4A).

###########################################################
DO NOT LEAVE CONTROL BOARD POWER PLUGGED IN WHEN NOT IN USE
###########################################################

It has a weird habit of dumping current into the steppers and everything gets super hot if left plugged in,
leading to stepper motor burnout. There is also no limit switch currently implemented - if something goes south,
best course of action is to kill power to the board, be it by disconnecting power from the wall or from the board input.

To run the stage control, run Launcher.bat and follow the prompts. An outline lies below:

COM/BAUD settings:

    COM port is the usb port that the stage is connected to. Make note of which are present *without* the stage
    connected and then you'll be able to tell which it is when you connect the board and relaunch as it'll be new.

    Baud rate for the board is 112500. Other values won't work properly.

Startup File:

    Location of the startup file - to see more regarding that, open the startup file with any text editor.
    Default is Config/startup.txt, and shouldn't change.
    To learn more, and to add more parameters if need be, see
    https://drive.google.com/file/d/1_hdJo_EgqaWKUi6HbuQ6sbPqiyw507D5/view?usp=sharing
    If this is inaccessible, contact Liam at droog@ualberta.ca for a copy


Now that the stage control is loaded, you can move the stage to your heart's desire!

Important Buttons:
    - Set home
        Sets current stage position to [0, 0] as reference home
    - Go home
        Goes to set home
    - 10, 1, 0.1, 0.01, 0.001
        These change the rate at which the stage moves whenever jogged. This stage has a resolution of around
        50 micron, so anything above 0.01 should be alright. Currently, using 0.001 doesn't do much.


Important notes:
    - Native units are in mm
    - Movement can be 'jogged' with the arrow keys. Don't hold them down excessivly, or risk running the stage
      into one of it's ends
    - This also takes in Gcode commands in the CLI on the right.

TL;DR of Gcode:
    - Most used command will be G0 X12.34 Y56.78
      where after X and Y are the respective coordinates that you wish to go to. Spacing is important (that is, spaces
      between 'G0' and 'X' and between 'X' and 'Y' are paramount to smooth operation
    For example, if you wish to go to X=1.22, Y=-4.52, the command would be: 'G0 X1.22 Y-4.52'
    Then, off it goes! There is a rabbit hole of Gcode, but most of it is not relevant for our uses (at least for LIBS)

Congratulations, you made it to the end of the readme file!
Have a potato. Happy lasering!


                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                ▓▓▓▓▓▓▒▒▓▓▒▒▓▓▒▒▓▓▓▓▓▓
              ▓▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            ▓▓▒▒▓▓▒▒▓▓▓▓▒▒▓▓▓▓▒▒▓▓▓▓▒▒▓▓▓▓
          ▒▒▓▓▓▓▓▓▒▒▓▓▒▒▓▓▓▓▓▓▓▓▒▒▓▓▒▒▒▒▓▓
        ▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓
      ▓▓▓▓▓▓▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓
      ▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▒▒▓▓██
    ▓▓▒▒▒▒▒▒▓▓▓▓▒▒▒▒▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▒▒▒▒▓▓██
    ▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
  ▓▓▓▓▒▒▓▓▒▒▒▒▓▓▓▓▒▒▓▓▓▓▓▓▓▓▒▒▓▓▒▒▓▓▓▓▓▓████
  ▒▒▓▓▒▒▓▓▒▒▒▒▓▓▒▒▒▒▒▒▓▓▓▓▒▒▓▓▒▒▓▓▓▓▓▓▓▓████
▓▓▓▓▓▓▒▒▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
▒▒▒▒▒▒▓▓▓▓▒▒▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
▒▒▒▒▒▒▓▓▓▓▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
▓▓▒▒▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████
  ▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████
  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████
    ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████
      ████▓▓██████████████
        ██████████████

























