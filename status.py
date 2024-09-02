import os
import terminal_output as TO
import checkout
import reconstruct

def check_equal(file1_list, file2_list):
    file1 = [line.rstrip("\n") for line in file1_list]
    file2 = [line.rstrip("\n") for line in file2_list]
    return file1 == file2

def pastport_status(pastport_location):
    
    # untracked: any file whose old location in pastport forlder can not be found are considered untracked
    # deleted: file present in pastport folder but not in new folder location
    untracked_files = []
    deleted_files = []
    modified_files = []
    def status_recursion(loc):
        # checking for untracked files and modified files
        dir_new_file_list = os.listdir(loc)
        for dir_file in dir_new_file_list:
            new_file_location = loc + f"\{dir_file}"
            old_file_location = loc + f"\pastport\u00b6\{dir_file}"
            # untracked files checking
            if os.path.isfile(new_file_location) and not os.path.exists(old_file_location):
                untracked_files.append(new_file_location)
            # modified files checking
            if os.path.isfile(new_file_location) and os.path.isfile(old_file_location):
                file_name, extension = os.path.splitext(dir_file)
                try:
                    track_file_location = loc + f"/pastport\u00b6/{file_name}_{extension[1:]}.track"
                except:
                    TO.output(message="\u26a0  [Error] Contact Khritish Kumar Behera\n unavilable of .track file", color="r")
                    exit()
                
                constructed_file_lines = []
                new_file_lines = []
                with open(track_file_location, "r") as track_file:
                    lines = track_file.readlines()
                    track_line = lines[-1]
                    commit_data = checkout.extract_commit_data(tracked_line=track_line)
                    constructed_file_lines = reconstruct.reconstruct_file(old_file_location=old_file_location, commit_data=commit_data)
                with open(new_file_location, "r") as new_file:
                    new_file_lines = new_file.readlines()
                # print(new_file_location)
                # print(constructed_file_lines)
                # print(new_file_lines)
                if not check_equal(new_file_lines, constructed_file_lines):
                    modified_files.append(new_file_location)
                

        
        # checking for deleted files
        dir_old_file_list = os.listdir(loc + f"\pastport\u00b6")
        for dir_file in dir_old_file_list:
            old_file_location = loc + f"\pastport\u00b6" + f"\{dir_file}"
            new_file_location = loc + f"\{dir_file}"
            if os.path.isfile(old_file_location) and not os.path.exists(new_file_location):
                file_name_with_extension = os.path.basename(new_file_location)
                file_name, extension = os.path.splitext(file_name_with_extension)
                if extension not in [".stagelog", ".stage", ".track"]:
                    deleted_files.append(old_file_location)
        
        for dir_file in dir_new_file_list:
            if os.path.isdir(dir_file) and dir_file != "pastport\u00b6":
                status_recursion(loc + f"\{dir_file}")
    status_recursion(loc=pastport_location)
    return untracked_files, deleted_files, modified_files
# print(pastport_status(r"C:\Users\HP\Desktop\test"))