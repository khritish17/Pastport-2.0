import os 
import terminal_output as to
import shutil
import commit_data_file as cdf
import stage
import commit

success_status = True
def pastport_init(location):
    # create the pastport metadata directory and inside its subdirectory
    create_metadata(location=location)
    stage.pastport_stage(pastport_root_location=location, init=True)

    
    if success_status:
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

        for file in files_list:
            # commit the files
            commit.pastport_commit(file_location=location + f"/{file}", commit_message="Inititation of pastport")
        
    except:
        to.output(message="\u26a0  [WARNING] PASTPORT has already been initialized in this directory", color="r")
        success_status = False

     