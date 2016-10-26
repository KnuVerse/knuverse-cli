from __future__ import print_function
import sys
import threading
import curses
from time import sleep
from datetime import datetime

import colorama
from colorama import Fore
colorama.init(autoreset=True)

from cli.lib.recorder import record_to_file


def _draw_pinpad(screen, pin_mapping):

    cell_size = 15
    pinpad_width = cell_size * 3 + 4  # 3 cells plus 4 cell dividers
    pinpad_height = 20

    y, x = screen.getmaxyx()
    y = (y - pinpad_height) // 2
    x = (x - pinpad_width) // 2

    def draw_line(y, x):
        screen.addstr(y, x, "-" * pinpad_width)
        y += 1
        return y, x

    def draw_separator(y, x, separator=("", "", "")):
        screen.addstr(y, x, "|%s|%s|%s|" % tuple([s.center(cell_size) for s in separator]))
        y += 1
        return y, x

    def draw_words(y, x, separator):
        screen.addstr(y, x, "|%s|%s|%s|" % tuple([pin_mapping.get(i).center(cell_size) if i != " " else " ".center(cell_size) for i in separator]))
        y += 1
        return y, x

    pinpad = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        [" ", "0", " "]
    ]

    for row in pinpad:
        y, x = draw_line(y, x)
        y, x = draw_separator(y, x, separator=row)
        y, x = draw_separator(y, x)
        y, x = draw_words(y, x, row)
        y, x = draw_separator(y, x)

    draw_line(y, x)
    screen.refresh()


def _draw_word(screen, display):

    y, x = screen.getmaxyx()
    y //= 2
    x //= 2

    screen.addstr(y, x, display)
    screen.refresh()


def verification(api, client_name, mode=None):

    client = api.get_client_info(client_name)

    # Make sure client is enrolled
    if client.get("state") != "enrolled":
        print("%s must enroll before verifying." % client_name)
        return

    ver = api.start_verification(client.get("id"), mode=mode)
    ver_id = ver.get("verification_id")

    # Get length of verification. We need this to know how long to record
    ver_length = 0
    for frame in ver.get("animation"):
        ver_length += frame.get("duration")
    audio_length = float(ver_length) / 1000 + 1

    # Begin the recorder in a separate thread
    t = threading.Thread(target=record_to_file, args=("/tmp/verification.wav", audio_length))
    t.daemon = True
    t.start()

    # TODO Initial pause
    # Display the animation
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    try:
        for frame in ver.get("animation"):
            if frame.get("pinpad_display"):
                _draw_pinpad(screen, frame.get("pinpad_display"))
            else:
                _draw_word(screen, frame.get("display"))
            screen.erase()
            sleep(float(frame.get("duration")) / 1000)
    except curses.error:
        print("Terminal window size is too small.")
        sys.exit(1)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        screen.erase()
    # Wait for the recorder thread to finish
    t.join()

    # Upload verification audio
    api.upload_verification_resource(
        ver_id,
        audio_file="/tmp/verification.wav",
    )

    # Display the verification results
    print("Processing...", end="")
    ver = api.get_verification_resource(ver_id)
    while ver.get("state") != "completed":
        sleep(1)
        ver = api.get_verification_resource(ver_id)
    if ver.get("verified"):
        print(Fore.GREEN + "Verified")
    else:
        print(Fore.RED + "Rejected")
    return
