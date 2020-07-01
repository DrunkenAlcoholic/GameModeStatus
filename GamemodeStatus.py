#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep
import subprocess

# Main Thread for monitoring "gamemoded -s"
class GameModeStatusLoop(Thread):
    def __init__(self, interval):
        Thread.__init__(self)
        # set as daemon so thread dies when program dies
        self.daemon = True
        self.interval = interval
        self.status = ""
        self.start()

    def run(self):
        while True:
            # Get current status
            currentstatus = self.GameModeStatus()
            # Have we notified user of status alread?
            if currentstatus != self.status:
                self.SendNotification(
                    "<b>GameMode</b>", "<i>" + currentstatus + "</i>", "input-gaming"
                )
                # Set the status to current status if different
                self.status = currentstatus
            # Pause the loop
            sleep(self.interval)

    # Check status of gamemode
    def GameModeStatus(self):
        # Execute gamemoded and get output
        result = subprocess.run(["gamemoded", "-s"], stdout=subprocess.PIPE)
        return result.stdout.decode().strip()

    # Send notification to user
    def SendNotification(self, title, message, icon):
        subprocess.run(["notify-send", title, "-i", icon, message])
        return


# Return True if package name exsist, checking lowercase
def IsPackageInstalled(pkgname):
    installed = False
    for package in packages:
        if package.lower().startswith(pkgname.lower()):
            installed = True
    return installed


# Main
if __name__ == "__main__":
    # Set directory with package listing
    pkglocation = "/var/lib/eopkg/package"
    # List directory names a.k.a installed packages
    packages = os.listdir(pkglocation)
    # Check to make sure gamemode package is installed
    if IsPackageInstalled("gamemode"):
        # Start monitoring Thread
        GameModeStatusLoop(2)
        while True:
            sleep(1)
    else:
        print(
            "Error: gamemode package not found, please install gamemode package before running GamemodeStatus.py"
        )


