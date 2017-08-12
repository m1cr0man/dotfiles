import os, random, sys
from subprocess import call
from time import time

def set_bg(new_bg):
    new_bg = new_bg.replace(" ", r"\ ").replace("'", r"\'")
    if sys.argv[1] == "sway":
        call("sway output LVDS-1 bg \"%s\" fill; sway output eDP-1 bg \"%s\" fill" % (new_bg, new_bg), shell=True)
    else:
        call("feh --bg-fill %s" % (new_bg), shell=True)

def main():
    path = "/home/lucas/Pictures/Desktop Backgrounds/Current Selection/v1/"
    save_path = "/home/lucas/.config/sway/Atomic-Suitcase/seen_bgs.txt"
    interval = 12 * 3600 # Seconds

    # Load seen backgrounds
    seen_bgs = []
    if os.path.exists(save_path):
        with open(save_path, "r") as save_file:
            seen_bgs = [bg.strip() for bg in save_file]

        # Use the last background if the interval hasn't passed
        # Check for the override flag though
        if "-f" not in sys.argv and os.path.getmtime(save_path) + interval > time():
            return set_bg(path + seen_bgs[-1])

    # Find all backgrounds
    bgs = [f for f in os.listdir(path) if os.path.isfile(path + f) and f not in seen_bgs]

    # Reset if we've seen them all
    if not len(bgs):
        os.remove(save_path)
        bgs = seen_bgs
        seen_bgs = []

    current_img = random.choice(bgs)

    # Save this background to the save file
    with open(save_path, "a") as save_file:
        save_file.write(current_img + "\n")

    set_bg(path + current_img.replace(" ", r"\ ").replace("'", r"\'"))

main()
