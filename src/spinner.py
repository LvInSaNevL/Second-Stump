import sys
import time

def spinning_cursor():
    frames = ["◰", "◳", "◲", "◱"]
    while True:
        for cursor in frames:
            yield cursor

def main():
    spinner = spinning_cursor()
    while (True):
        # Fancy CLI keep alive indicator
        now = time.strftime('%H:%M:%S')
        currentMinute = time.strftime('%S')
        sys.stdout.write("\r{} Current time is {}".format(next(spinner), now))
        sys.stdout.flush()

        # Checking to do stuff
        if (currentMinute == "50"): print("50")
        if (currentMinute == "00"): print("00")
        if (currentMinute == "20"): print("20")
        if (currentMinute == "40"): print("40")

        # Just to slow down the CPU
        time.sleep(1)



main()