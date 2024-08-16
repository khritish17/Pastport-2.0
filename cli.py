import terminal_output as TO
import time
import os

TO.output("PASTPORT COMMAND LINE INTERFACE (PRT CLI) version 2\n---Authored by Khritish Kumar Behera---", "g")
time.sleep(1)
TO.output("Boot up the PASTPORT application by specifying the directory location.")
location = ""

while True:
    location = input("Location >> ")
    if location == "q":
        exit()
    if not os.path.exists(location):
        TO.output(message="Invalid location detected !!!, a valid location is essential to boot up", color='r')
        print()
        TO.output(message="To terminate the application, press 'q'", color="red")
    else:
        TO.output(message="Pastport Boot up successful !!!", color="g")
        break

while True:
    commands = input("pastport >>> ")
    commands = commands.strip().lower().split(" ")
    
    if commands[0] == "q" or commands[0] == "quit":
        break
    if commands[0] == "h" or commands[0] == "help":
        # init command help
        TO.output(message="[1] 'init' command:", color="c")
        print("Initializes the PASTPORT system, creates the necessary directory structure and tracking files for version control")
        print("Sample Output:")
        TO.output(message="init", color="b")
        print()

        # status command help
        TO.output(message="[2] 'status' command:", color="c")
        print("Provides functionality to check the status of the working directory, identifying modified, untracked, and deleted files")
        print("Sample Output:")
        TO.output(message="status", color="b")
        print()

        # commit command help
        TO.output(message="[3] 'commit <message>' command:", color="c")
        print("Saves the current version of the whole directory")
        print("Sample Output:")
        TO.output(message="commit 'This is the first commit message' ", color="b")
        print()

        # log command help
        TO.output(message="[4] 'log' command:", color="c")
        print("Keeps track of all commits made till now.")
        print("Sample Output:")
        TO.output(message="log", color="b")
        print()

        # checkout command help
        TO.output(message="[5] 'checkout <commit number>' command:", color="c")
        print("Allows to revert back to a specific version by specifying the commit nums")
        print("Sample Output:")
        TO.output(message="checkout 1", color="b")
        print()
    elif commands[0] == "init":
        pass
    elif commands[0] == "status":
        pass
    elif commands[0] == "commit":
        pass
    elif commands[0] == "log":
        pass
    elif commands[0] == "checkout":
        pass
    else:
        TO.output(message="Invalid Command, press 'h' for help", color="r")

