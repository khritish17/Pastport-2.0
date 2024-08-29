import os
import terminal_output as TO
def pastport_stage(pastport_root_location, init = False):
    pastport_root_location = os.path.abspath(pastport_root_location).lower()
    file_paths_commit_ids = {}
    if not init:
        file_count = 1
        # continuously asks user for the file paths
        TO.output(message="Provide the paths of the file(s) for staging", color="g")
        while True:
            TO.output(message="Press y/Y when done with file(s)", color="b")
            file_path = input(f"File {file_count} path >>> ")
            file_path = file_path.strip().lower()
            if file_path == "y":
                break
            file_path = os.path.abspath(file_path)
            if os.path.exists(file_path) and (pastport_root_location in file_path):
                file_paths_commit_ids[file_path] = get_last_commit_id(file_path) + 1
                file_count += 1
            else:
                TO.output(message="\u26a0  [WARNING] Invalid file path detected!!!", color="r")
        # open the .stagelog file and the get the last stage id
        stage_id = None
        with open(pastport_root_location + "/pastport\u00b6/pastport.stagelog", "r") as stagelog_file:
            last_line = stagelog_file.readlines()[-1]
            stage_id = int(last_line.split("\u00b6")[0]) + 1
        # here .stage file has data indicating commit has not been made yet
        with open(pastport_root_location + "/pastport\u00b6/pastport.stage", "w") as stage_file:
            stage_file.write(str(stage_id))
            for path, cm_id in file_paths_commit_ids.items():
                stage_file.write(f"\u00b6{path}\u00b6{cm_id}")
    else:
        
        def stage_recursion(loc):
            dir_file_list = os.listdir(loc)
            for dir_file in dir_file_list:
                if os.path.isfile(loc + f"\{dir_file}"):
                    file_paths_commit_ids[loc + f"\{dir_file}"] = 0
                elif dir_file != "pastport\u00b6":
                    stage_recursion(loc + f"\{dir_file}")
        stage_recursion(pastport_root_location)
        stage_id = str(0)
        with open(pastport_root_location + "/pastport\u00b6/pastport.stagelog", "w") as stage_file:
            stage_file.write(stage_id)
            for path, cm_id in file_paths_commit_ids.items():
                stage_file.write(f"\u00b6{path}\u00b6{cm_id}")
            stage_file.write("\n")
        # just create an empty .stage file indicating commit has been made (ideally its made upon inititation in init.py)
        # no need to commit through the function
        stage_file = open(pastport_root_location + "/pastport\u00b6/pastport.stage", "w")
        stage_file.close()
    
    # opens the .stage file
    # appends the following:
    # stage id, file paths, computed commit id of files

    pass

def get_last_commit_id(new_file_location):
    new_file_location = os.path.abspath(new_file_location)
    # go to its pastport directory
    file_name_with_extension = os.path.basename(new_file_location)
    file_name, extension = os.path.splitext(file_name_with_extension)
    track_file_location = os.path.dirname(new_file_location) + "/pastport\u00b6" + f"/{file_name}_{extension[1:]}.track"
    if os.path.exists(track_file_location):
        with open(track_file_location, "r") as track_file:
            last_line = track_file.readlines()[-1]
            commit_id = int(last_line.split("\u00b6")[0])
            return commit_id
    else:
        # new file/untracked, hence return -1 so that it will become 0 commit id as next commit id
        return -1

# pastport_stage(r"C:\Users\HP\Desktop\test")