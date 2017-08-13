import sys, json, psutil, os, subprocess, time

def read_file(file):
    contents = ""
    with open(file, 'r') as f:
        contents += f.read().strip()
    return contents

def gen_segment(output, icon, text, colour, bg_colour):
    # Separator Arrow
    output.append({
        "separator": False,
        "separator_block_width": 0,
        "full_text": u"\ue0b2",
        "color": bg_colour
    })
    # Lil hack for the background colour of the separator
    if len(output) > 1:
        output[-1]["background"] = output[-2]["background"]

    # Segment content
    output.append({
        "separator": False,
        "separator_block_width": 0,
        "full_text": " %s %s " % (icon, text),
        "color": colour,
        "background": bg_colour
    })

def get_battery_stats(default_colour):
    battery_path = "/sys/class/power_supply/"
    batteries = [battery_path + f for f in os.listdir(battery_path) if "BAT" in f and not os.path.isfile(battery_path + f)]

    for battery in batteries:
        charge_max = int(read_file(battery + "/charge_full"))
        charge_current = int(read_file(battery + "/charge_now"))
        charge_percent = charge_current * 100 / charge_max;
        status = read_file(battery + "/status")
        return ((u"\uf242" if status == "Discharging" else u"\uf1e6"), ("{:0>4.1f}%").format(charge_percent), charge_percent > 5 and default_colour or '#FF0000')

def get_network_status():
    cmd = subprocess.run("iw dev wlo1 link | grep -Po '(?<=SSID\: ).*'", shell=True, stdout=subprocess.PIPE)
    connection = str(cmd.stdout.strip().strip())[2:-1]
    return (u"\uf1eb", connection) if connection else (u"\uf127", "None")

def get_sound_status():
    cmd = subprocess.run("amixer sget Master | grep -Eo [[:digit:]]+%\|\[o[n\|f]+\]", shell=True, stdout=subprocess.PIPE)
    data = [l.strip() for l in str(cmd.stdout.strip())[2:-1].split("\\n")]
    return ((u"\uf026" if data[0] == "0%" or data[1] == "[off]" else u"\uf028"), "{:0>3}".format(data[0]))

def get_backlight_status():
    backlight_path = "/sys/class/backlight/"
    backlights = [backlight_path + f for f in os.listdir(backlight_path) if "backlight" in f and not os.path.isfile(backlight_path + f)]
    redshift_not_running = subprocess.run("pgrep redshift", shell=True, stdout=subprocess.PIPE).returncode

    for backlight in backlights:
        actual_brightness = int(read_file(backlight + "/actual_brightness"))
        max_brightness = int(read_file(backlight + "/max_brightness"))
        return (u"\uf185" + ("" if redshift_not_running else u"\uf06c"), ("{:0>2.0f}%").format(actual_brightness * 100 / max_brightness))

def print(str):
    sys.__stdout__.write(str)
    sys.__stdout__.flush()

def main():
    print("{\"version\": 1, \"custom_workspace\": true}\n[\n[],")

    shade_1_fg = os.environ['FG']
    shade_1_bg = os.environ['BGL']
    shade_2_bg = os.environ['BGD']
    shade_2_fg = os.environ['FG']

    # Flashing clock colon
    ticker = ":"

    # Initial sleep
    time.sleep(1)

    while True:
        output = []

        # Elements go here
        # Current Network
        gen_segment(output, *get_network_status(), shade_1_fg, shade_1_bg)

        # Memory
        gen_segment(output, u"\uf233", "{:0>4.1f}%".format(psutil.virtual_memory().percent), shade_2_fg, shade_2_bg)

        # CPU Usage
        gen_segment(output, u"\uf0e4", "{:0>4.1f}%".format(psutil.cpu_percent()), shade_1_fg, shade_1_bg)

        # Battery
        gen_segment(output, *get_battery_stats(shade_2_fg), shade_2_bg)

        # Volume
        gen_segment(output, *get_sound_status(), shade_1_fg, shade_1_bg)

        # Backlight
        gen_segment(output, *get_backlight_status(), shade_2_fg, shade_2_bg)

        # Clock
        ticker = " " if ticker == ":" else ":"
        gen_segment(output, u"\uf017", time.strftime("%d/%m %I" + ticker + "%M%p"), shade_1_fg, shade_1_bg)

        print(json.dumps(output, separators=(", ", ": ")) + ",")
        time.sleep(1)

main()
