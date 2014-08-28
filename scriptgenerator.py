#!/usr/bin/python

# parse from custom scripting lanugage into LSL commands for OpenSim
# to be used by AI for performing plays

# available commands:

#   enter    fname      lname       ...      entry_point
#   exit     fname      lname       ...      exit_point
#   move     fname      lname       ...      destination
#   turn     fname      lname       ...      direction
#   fname    lname:     quote
#   wait     seconds    ...

# usage: ./scriptgenerator.py input_file output_file

from sys import argv
from shutil import copy
import random

# Mappings to different locations on stage
locations = {
    "sl" : "<237.1858, 159.4924, 41.4582>", # stage left
    "sr" : "<239.1398, 175.7619, 41.4582>", # stage right
    "bl" : "<239.6852, 163.2641, 41.4582>", # back left
    "bc" : "<240.5841, 168.0781, 41.4582>", # back center
    "br" : "<241.2923, 172.3245, 41.4582>", # back right
    "cl" : "<236.9230, 163.8010, 41.4582>", # center left
    "cs" : "<237.8219, 168.6150, 41.4582>", # center stage
    "cr" : "<238.5301, 172.8613, 41.4582>", # center right
    "fl" : "<234.1923, 164.3317, 41.4582>", # front left
    "fc" : "<235.0912, 169.1457, 41.4582>", # front center
    "fr" : "<235.7994, 173.3921, 41.4582>"  # front right
}

# angles corresponding to different directions relative to stage
dirs = {
    "right" : "70.750",    # right
    "front" : "160.750",   # front
    "left"  : "258.750",   # left
    "back"  : "340.750"    # back
}

curtain = {
    "up" : "<234.2045, 168.1162, 55.0000>",
    "down" : "<234.2045, 168.1162, 47.6135>"

}

appearances = {
	1  : "appearance5e90b629-e431-40f9-8343-f58303ff243e",
	2  : "appearance6c871777-89ae-4377-9309-b043e89eeba1",
	3  : "appearance6d90c106-7881-4628-8416-5fe5aa0f7ed7",
	4  : "appearance37c3e21d-b823-4ff4-bb41-ed0b4d045d0c",
	5  : "appearance584bf18b-1451-4010-9155-963ad9a56647",
	6  : "appearancea7f73e6e-c2a9-4551-b9ec-d1e42cb38caa",
	7  : "appearancea3694c96-5f74-40e1-981a-c6796c771224",
	8  : "appearanceb23c39a3-70f0-4d57-bdcb-13d987b65c7d",
	9  : "appearancec6647a3f-ee26-4b3f-bee7-22b3380930b2",
	10 : "appearancedb4099f0-ab21-4dc1-abfb-eeba28e84102",
	11 : "appearancef10483d4-9e54-4a09-8cf2-4e6cbc912223"
}
	

def main():

    script = open(argv[1], "r") # open input file for reading
    lsl = open(argv[2], "a")    # open output file for writing

    copy('./moveNPC.cs', argv[2])  # copy moveNPC.cs into output file to access moveNPC method 

    # Write header
    lsl.write("\n");
    lsl.write("default {\n")
    lsl.write("    touch_start(integer total_number) {\n")
    lsl.write("        // raise the curtain\n")
    lsl.write("        llSetPrimitiveParams([PRIM_POSITION, " + curtain["up"] + "]);\n")
    lsl.write("\n")

    for line in script:
        # remove \n at the end of the line if there is one
        if (line[-1] == "\n"):
            words = line[:-1].lstrip().split(" ")
        else:
            words = line.lstrip().split(" ")

        if (words[0] == ""):
            lsl.write("\n")
        elif (words[0] == "enter"):
            lsl.write(enter(words[1], words[2], words[-1]))
        elif (words[0] == "exit"):
            lsl.write(exit(words[1], words[2], words[-1]))
        elif (words[0] == "move"):
            lsl.write(move(words[1], words[2], words[-1]))
        elif (words[0] == "turn"):
            lsl.write(turn(words[1], words[2], words[-1]))
        elif (words[1][-1] == ":"):
            lsl.write(say(words[0], words[1][:-1], " ".join(words[2:])))
        elif (words[0] == "wait"):
            lsl.write(wait(words[1]))
        elif len(words) is not 1:
            lsl.write("        //" + line)

    # Write footer
    lsl.write("        // lower the curtain\n")
    lsl.write("        llSetPrimitiveParams([PRIM_POSITION, " + curtain["down"] + "]);\n")
    lsl.write("    }\n")
    lsl.write("}\n")

    lsl.close()
    script.close()

# spawn a new NPC at this location.
def enter(fname, lname, location):
    return """\
        // %s %s spawns at %s
        vector %s%sPos = %s; 
        // use one of 12 random appearances 
        key %s%s = osNpcCreate("%s", "%s", %s%sPos, "%s"); 

""" % (fname, lname, location, fname, lname, locations[location], fname, lname, fname, lname, fname, lname, appearances[random.randint(1, 11)])

# move this NPC to this location and despawn it
def exit(fname, lname, exit_point):
    return """%s\
        //%s %s despawns
        osNpcRemove(%s%s);
        %s%s = NULL_KEY;

""" % (move(fname, lname, exit_point), fname, lname, fname, lname, fname, lname)

# move this NPC to this location
def move(fname, lname, dest):
    return """\
        //%s %s moves to %s
        moveNpc(%s%s, %s);

""" % (fname, lname, dest, fname, lname, locations[dest])

# turn this NPC so it is facing this direction
def turn(fname, lname, dir):
    return """\
        // %s %s faces %s
        osNpcSetRot(%s%s, llEuler2Rot(<0, 0, %s> * DEG_TO_RAD));

""" % (fname, lname, dir, fname, lname, dirs[dir])

# make this NPC say some dialogue
def say(fname, lname, quote):
    return """\
        //%s %s says \"%s\"
        osNpcSay(%s%s, \"%s\");

""" % (fname, lname, quote, fname, lname, quote)

# wait this many seconds. Creates dramatic tension between characters and makes audience feel awkward.
# May also indicate somebody forgot their line or missed their cue.
def wait(seconds):
    return """\
        //The stage goes silent
        llSleep(%s);

""" % (seconds)

if __name__ == "__main__":
    main()

