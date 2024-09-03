import terminal_output as TO
import time
import os
import init
import commit
import shlex
import stage
import checkout as chk
import path_shorten as ps
import status
import help

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
        help.help()
    elif commands[0] == "init":
        init.pastport_init(location=location)
    elif commands[0] == "add":
        # performs the staging mechanism
        # create the .stage file, and add the file(s)
        try:
            flag = commands[1].strip().lower()
            if flag == "-a":
                stage.pastport_stage(pastport_root_location=location, flag="-a", init=False)
            elif flag == "-p":
                stage.pastport_stage(pastport_root_location=location, flag="-p", init=False)
            TO.output(message="\u2705  Files added successfully for staging", color="g")
        except:
            TO.output(message="\u26a0  Missing flags in add command !!!", color="r")
        pass
    elif commands[0] == "status":
        untracked_files, deleted_files, modified_files =status.pastport_status(pastport_location=location)
        short_untrack_files = ps.path_shorten(paths=untracked_files)
        short_del_files = ps.path_shorten(paths=deleted_files)
        short_mod_files = ps.path_shorten(paths=modified_files)
        print()
        TO.output(message=f"Untracked File(s): {' | '.join(short_untrack_files)}", color="g")
        TO.output(message=f"Deleted Files(s): {' | '.join(short_del_files)}", color="r")
        TO.output(message=f"Modified File(s): {' | '.join(short_mod_files)}", color="p")
    elif commands[0] == "commit":
        # commit has three commands: commit <file/flag> <message>
        # make sure pastport is already initialized
        directory_file_list = os.listdir(location)
        if not ("pastport\u00b6" in directory_file_list and os.path.isdir(location + "/pastport\u00b6")):
            TO.output(message="\u26a0  PASTPORT has not been initialized in this directory !!!", color="r")
            continue
        # commit flags
        commit_message = "Untitled Commit Message"
        try:
            file_flag = commands[1].strip().lower()
            if file_flag == "-m":
                try:
                    commit_message = commands[2]
                except:
                    TO.output(message="\u26a0  [WARNING] Commit message was expected!!!, set to default message", color="r")
                if not commit_message:
                    commit_message = "Untitled Commit Message"
                    TO.output(message="\u26a0  [WARNING] Empty commit message provided, set to default message", color="r")
            else:
                TO.output(message="\u26a0  Invalid commit flags !!!", color="r")
                continue
        except:
            # TO.output(message="\u26a0  Provide which file(s)(in comma seperated format) that needs to commited and optional commit message", color='r')
            commit_message = input("commit message >>>> ")
        commit_message = commit_message.strip()
        file_paths_commit_ids = {}
        # get the files paths and commit ids from .stage file
        line = ""
        with open(location + "/pastport\u00b6/pastport.stage", "r") as stage_file:
            lines = stage_file.readlines()
            if not lines:
                TO.output(message="Stage the files before commit, use add command", color="r")
                continue
            line = lines[0]
            stage_data = line.split("\u00b6")
            for i in range(1, len(stage_data), 2):
                path = stage_data[i]
                c_id = stage_data[i+1]
                file_paths_commit_ids[os.path.abspath(path)] = c_id
        
        for file_path, commit_id in file_paths_commit_ids.items():
            commit.pastport_commit(file_location=file_path, commit_message=commit_message)
        # copy the content of .stage file to .stagelog  
        with open(location + "/pastport\u00b6/pastport.stagelog", "a") as stagelog_file:
            stagelog_file.write(line)
            stagelog_file.write(f"\u00b6{commit_message}")
            stagelog_file.write("\n")
        # empty .stage file
        stage_file = open(location + "/pastport\u00b6/pastport.stage", "w")
        stage_file.close()
        TO.output(message="\u2705  Commit operation successfull", color="g")
        

    elif commands[0] == "log":
        try:
            short_flag = commands[1]
            if short_flag not in ["-lp", "-sp"]:
                TO.output(message="\u26a0  [WARNING] Invalid flags in log command !!!", color="r")
        except:
            short_flag = "-lp"
        with open(location + "/pastport\u00b6/pastport.stagelog", "r") as stagelog_file:
                lines = stagelog_file.readlines()
                log_data = {}
                for line in lines:
                    stage_data = line.split("\u00b6")
                    stage_id = stage_data[0]
                    commit_mssg = stage_data[-1].strip("\n")
                    file_paths_stage = []
                    for j in range(1, len(stage_data) - 1, 2):
                        file_paths_stage.append(stage_data[j])
                    if short_flag == "-sp":
                        paths_short = ps.path_shorten(file_paths_stage)
                    else:
                        paths_short = file_paths_stage
                    log_data[stage_id] = [commit_mssg, paths_short]
                TO.output(message="{:20}\t{:20}\t{:20}".format("stage_id", "commit_mssg", "file(s)"))
                for stage_id, cid_paths in log_data.items():
                    commit_mssg, paths_short = cid_paths 
                    TO.output(message="{:20}\t{:20}\t{:20}".format(stage_id, commit_mssg, ' | '.join(paths_short)))
    elif commands[0] == "checkout":
        try:
            file_flag = commands[1]
        except:
            TO.output(message="\u26a0  Invalid checkout command, flags not provided !!!", color="r")
            continue
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
                if chk.pastport_checkout(new_file_location=path, commit_id=commit_id):
                    TO.output(f"\u2705  File: {path}, checkedout successfully", color="g")
                else:
                    TO.output(f"\u26a0  File: {path}, checkout attempt unsuccessfull", color="r")
        elif file_flag.lower() == "-s":
            # stage checkout
            try:
                stage_id = int(commands[2])
            except:
                TO.output(message=f"\u26a0  [Error] a valid stage id is required", color="r")
                continue
            # get the file path and commit id from .stagelog file
            stage_data = None
            with open(location + "/pastport\u00b6/pastport.stagelog", "r") as stagelog_file:
                lines = stagelog_file.readlines()
                try:
                    stage_line = lines[stage_id].rstrip("\n")
                except:
                    TO.output(message=f"\u26a0  [Error] Invalid stage id provided", color="r")
                    continue
                stage_data = stage_line.split("\u00b6")
            for i in range(1, len(stage_data) - 1, 2):
                path = stage_data[i]
                commit_id = int(stage_data[i + 1])
                if chk.pastport_checkout(new_file_location=path, commit_id=commit_id):
                    TO.output(f"\u2705  File: {path}, checkedout successfully", color="g")
                else:
                    TO.output(f"\u26a0  File: {path}, checkout attempt unsuccessfull", color="r")
        else:
            TO.output(message="\u26a0  Invalid flags in checkout command !!!", color="r")
            continue
    else:
        TO.output(message="\u26a0  Invalid Command, press 'h' for help", color="r")


