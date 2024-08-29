import os 
import terminal_output as to
import shutil
import commit_data_file as cdf
import stage

success_status = True
def pastport_init(location):
    # create the pastport metadata directory and inside its subdirectory
    create_metadata(location=location)

    
    if success_status:
        # create the current gloabl id file
        # with open(location + "/pastport\u00b6/global_commit_id.txt", "w") as global_commit_file:
        #     global_commit_file.write("0")

        to.output(message="\u2705  PASTPORT successfully initialized", color="g")

def create_metadata(location):
    global success_status
    try:
        directory_file_list = os.listdir(location)
        files_list = []
        directory_list = []
        for ele in directory_file_list:
            if os.path.isfile(location+f"\{ele}"):
                files_list.append(ele)
            elif os.path.isdir(location + f"\{ele}"):
                directory_list.append(ele)
        
        # recursivly create pastport metadata file inside subdirectories
        for directory in directory_list:
            if directory != "pastport\u00b6":
                create_metadata(location=location + f"/{directory}")
        os.mkdir(location + "/pastport\u00b6")
        
        # create the global track file for current working directory
        # create a copy of each file in pastport for commit 0
        # for commit 0 of each file, 
        # directory_name = os.path.basename(location)
        # with open(location + f"/pastport\u00b6/{directory_name}.track","w") as global_track_file:
        #     # global track file structure: <commit id>\u00b6<files in csv format>
        #     # e.g.: 0\u00b6file1.cpp,file2.c,file3.py
        #     global_track_file.write(f"0\u00b6"+",".join(files_list)+"\n")

        for file in files_list:
            # keep a copy of the initial version of the file inside pastport
            shutil.copy2(src=location + f"/{file}",dst=location + f"/pastport\u00b6/{file}")
            
            # generate its track_file
            file_name_with_extension = os.path.basename(location + f"\pastport\u00b6\{file}")
            file_name, extension = os.path.splitext(file_name_with_extension)
            with open(location + f"/pastport\u00b6/{file_name}_{extension[1:]}.track", "w") as track_file:
                track_file.write(f"0\u00b6Inititation of pastport\n")
        stage.pastport_stage(pastport_root_location=location, init=True)
    except:
        to.output(message="\u26a0  [WARNING] PASTPORT has already been initialized in this directory", color="r")
        success_status = False

     