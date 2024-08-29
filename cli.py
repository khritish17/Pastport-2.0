import terminal_output as TO
import time
import os
import init
import commit
import shlex
import checkout as chk

def welcome_mssg():
    t = 0.1
    time.sleep(t)
    TO.output("## ##        ##        ## ##     ## ## ##   ## ##       ##     ## ##     ## ## ##", color="b")
    time.sleep(t)
    TO.output("##   ##   ##    ##   ##     ##      ##      ##   ##   ##  ##   ##   ##      ##", color="b")
    time.sleep(t)
    TO.output("##   ##   ##    ##   ##             ##      ##   ##   ##  ##   ##   ##      ##", color="b")
    time.sleep(t)
    TO.output("## ##     ## ## ##     ## ##        ##      ## ##     ##  ##   ## ##        ##", color="b")
    time.sleep(t)
    TO.output("##        ##    ##          ##      ##      ##        ##  ##   ##   ##      ##", color="r")
    time.sleep(t)
    TO.output("##        ##    ##   ##     ##      ##      ##        ##  ##   ##   ##      ##", color="r")
    time.sleep(t)
    TO.output("##        ##    ##     ## ##        ##      ##          ##     ##   ##      ##", color="r")
    time.sleep(t+0.2)

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
        TO.output(message="\u26a0  [Error]: Invalid location detected. A valid location is required to proceed with booting up", color='r')
        print()
        TO.output(message="Press 'q' to terminate the application", color="red")
    else:
        TO.output(message="\u2705  PASTPORT boot-up successful !!!", color="g")
        break

# converting the location into absloute location
location = location.lower()
location = os.path.abspath(location)

while True:
    commands = input("pastport >>> ")
    commands = shlex.split(commands.strip().lower())
    # commands = commands.strip().lower().split(" ")
    
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
    elif commands[0] == "add":
        # performs the staging mechanism
        # create the .stage file, and add the file(s)
        pass
    elif commands[0] == "status":
        pass
    elif commands[0] == "commit":
        # commit has three commands: commit <file/flag> <message>
        # make sure pastport is already initialized
        directory_file_list = os.listdir(location)
        if not ("pastport\u00b6" in directory_file_list and os.path.isdir(location + "/pastport\u00b6")):
            TO.output(message="\u26a0  PASTPORT has not been initialized in this directory !!!", color="r")
            continue
        # commit flags
        try:
            file_flag = commands[1]
            if file_flag.lower() == "-a":
                commit_message = input("commit message >>>> ")
                if not commit_message:
                    commit_message = "Untitled commit"
                # represents all files need to be commited, every file in the directory and sub-directories
                def commit_file_all(path):
                    dir_file_list = os.listdir(path)
                    directories = []
                    files = []
                    for dir_file in dir_file_list:
                        if os.path.isfile(path + f"/{dir_file}"):
                            files.append(dir_file)
                        elif dir_file != "pastport\u00b6" and os.path.isdir(path + f"/{dir_file}"):
                            directories.append(dir_file)
                    # first commit the files
                    for file in files:
                        commit.pastport_commit(file_location = path + f"/{file}", commit_message=commit_message)
                    for dir_ in directories:
                        commit_file_all(path + f"\{dir_}")
                commit_file_all(path=location)
                TO.output("\u2705  Files committed successfully", color="g")
            elif file_flag.lower() == "-p":
                # only commit the files whose path are provided
                # these file locations are comma seperated
                # make sure that paths are inside the parent directory
                try:
                    paths = commands[2]
                    paths = paths.split(",")
                    # for loc in paths:
                    for i in range(len(paths)):
                        loc = paths[i]
                        loc = os.path.abspath(loc)
                        if not os.path.isfile(loc):
                            TO.output(message=f"\u26a0  [Error]: The specified path does not correspond to a file \n {loc}", color="r")
                            continue
                        if not os.path.exists(loc):
                            TO.output(message=f"\u26a0  [Error]: Invalid path detected.\nFile path: '{loc}'", color="r")
                            continue
                        if location not in loc:
                            TO.output(message=f"\u26a0  Error: The path does not reside within the working PASTPORT directory\nCurrent working directory: {location}\nFile path:'{loc}'", color="r")
                            continue
                        base_name = os.path.basename(loc)
                        TO.output(f"[{i + 1}] File: {base_name}\nPath: {loc}")
                        commit_message = input(f"commit message >>>> ")
                        print()
                        if not commit_message:
                            commit_message = "Untitled commit"
                        commit.pastport_commit(file_location=loc, commit_message=commit_message)
                    TO.output("\u2705  Commit files successful", color="g")

                except:
                    TO.output(message="\u26a0  [Error]: Invalid command!!!", color="r")
                    continue
            elif file_flag.lower() == "-f":
                # only commit those file whose file name are provided, and are in the root directory
                try:
                    files = commands[2]
                    files = files.split(",")
                    for i in range(len(files)):
                        file = files[i]
                        if not os.path.exists(location + f"/{file}"):
                            TO.output(message=f"\u26a0  [WARNING] File #{i + 1} does not exist\nFile:{file}\nPath:{location}/{file}", color="r")
                            continue
                        TO.output(f"[{i + 1}] File: {file}\nPath: {location}/{file}")
                        commit_message = input(f"commit message >>>> ")
                        print()
                        if not commit_message:
                            commit_message = "Untitled commit"
                        commit.pastport_commit(file_location=location + f"/{file}", commit_message=commit_message)
                    TO.output("\u2705  Files committed successfully", color="g")
                except:
                    TO.output(message="\u26a0  File(s) not found!!!", color="r")
                    continue

            else:
                TO.output(message="\u26a0  Invalid flags in commit command !!!", color="r")
        except:
            # TO.output(message="\u26a0  Provide which file(s)(in comma seperated format) that needs to commited and optional commit message", color='r')
            TO.output(message="\u26a0  Invalid command: missing commit flags !!!", color="r")
    elif commands[0] == "log":
        pass
    elif commands[0] == "checkout":
        file_flag = commands[1]
        if file_flag.lower() == "-p":
            # this represents that the file(s) whose path is given will be reverted back to its commit id version 
            paths_commit_ids = commands[2].split(",")
            if len(paths_commit_ids) % 2 != 0:
                TO.output(message="\u26a0  Paths and commit ids are not in pairs", color="r")
                continue
            i = -1
            while i < len(paths_commit_ids) - 1:
                i += 1
                path = paths_commit_ids[i]
                path = os.path.abspath(path)
                if not os.path.exists(path):
                    TO.output(message=f"\u26a0  [WARNING] File does not exist, skiping these path!!!\nFile: {path}", color="r")
                    i += 1
                    continue
                if location not in path:
                    TO.output(message=f"\u26a0  [Error] File does not reside within the working PASTPORT directory, skiping these path!!!\nFile: {path}", color="r")
                    i += 1
                    continue
                i += 1
                commit_id = int(paths_commit_ids[i])
                chk.pastport_checkout(new_file_location=path, commit_id=commit_id)
        elif file_flag.lower() == "-f":
            files_commit_ids = commands[2].split(",")
            if len(files_commit_ids) % 2 != 0:
                TO.output(message="\u26a0  Files and commit ids are not in pairs", color="r")
                continue
            i = -1
            while i < len(files_commit_ids) - 1:
                i += 1
                file = files_commit_ids[i]
                path = location + f"/{file}"
                path = os.path.abspath(path)
                if not os.path.exists(path):
                    TO.output(message=f"\u26a0  [WARNING] File does not exist, skiping these path!!!\nFile: {path}", color="r")
                    i += 1
                    continue
                if location not in path:
                    TO.output(message=f"\u26a0  [Error] File does not reside within the working PASTPORT directory, skiping these path!!!\nFile: {path}", color="r")
                    i += 1
                    continue
                i += 1
                commit_id = int(files_commit_ids[i])
                chk.pastport_checkout(new_file_location=path, commit_id=commit_id)
        else:
            TO.output(message="\u26a0  Invalid flags in checkout command !!!", color="r")
    else:
        TO.output(message="\u26a0  Invalid Command, press 'h' for help", color="r")


