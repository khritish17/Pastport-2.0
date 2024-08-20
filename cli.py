import terminal_output as TO
import time
import os
import init
import commit
def welcome_mssg():
    TO.output("## ##        ##        ## ##     ## ## ##   ## ##       ##     ## ##     ## ## ##", color="b")
    TO.output("##   ##   ##    ##   ##     ##      ##      ##   ##   ##  ##   ##   ##      ##", color="b")
    TO.output("##   ##   ##    ##   ##             ##      ##   ##   ##  ##   ##   ##      ##", color="b")
    TO.output("## ##     ## ## ##     ## ##        ##      ## ##     ##  ##   ## ##        ##", color="b")
    TO.output("##        ##    ##          ##      ##      ##        ##  ##   ##   ##      ##", color="r")
    TO.output("##        ##    ##   ##     ##      ##      ##        ##  ##   ##   ##      ##", color="r")
    TO.output("##        ##    ##     ## ##        ##      ##          ##     ##   ##      ##", color="r")
welcome_mssg()
print()
TO.output("PASTPORT COMMAND LINE INTERFACE version 2.0\n---Authored by Khritish Kumar Behera---", "g")
time.sleep(1)
TO.output("Boot up the PASTPORT application by specifying the directory location.")
location = ""

while True:
    location = input("Location >> ")
    if location == "q":
        exit()
    if not os.path.exists(location):
        TO.output(message="\u26a0  Invalid location detected !!!, a valid location is essential to boot up", color='r')
        print()
        TO.output(message="To terminate the application, press 'q'", color="red")
    else:
        TO.output(message="\u2705  Pastport Boot up successful !!!", color="g")
        break

# converting the location into absloute location
location = os.path.abspath(location)

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
        init.pastport_init(location=location)
    elif commands[0] == "status":
        pass
    elif commands[0] == "commit":
        # commit has three commands: commit <file/flag> <message>
        # make sure pastport is already initialized
        directory_file_list = os.listdir(location)
        if not ("pastport\u00b6" in directory_file_list and os.path.isdir(location + "/pastport\u00b6")):
            TO.output(message="\u26a0  Pastport is not initialized in this directory !!!", color="r")
            continue
        # commit flags
        try:
            file_flag = commands[1]
            if file_flag.lower() == "-a":
                # represents all files need to be commited, every file in the directory and sub-directories
                print("all file")
            elif file_flag.lower() == "-p":
                # only commit the files whose path are provided
                print("file path is provided")
            elif file_flag.lower() == "-f":
                # only commit those file whose file name are provided, and are in the root directory
                print("direct file is provided in the root directory")
            else:
                TO.output(message="\u26a0  Invalid flags in commit, !!!", color="r")
        except:
            # TO.output(message="\u26a0  Provide which file(s)(in comma seperated format) that needs to commited and optional commit message", color='r')
            TO.output(message="\u26a0  Invalid command, missing commit flags !!!", color="r")
    elif commands[0] == "log":
        pass
    elif commands[0] == "checkout":
        pass
    else:
        TO.output(message="Invalid Command, press 'h' for help", color="r")

