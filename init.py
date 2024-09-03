import os 
import terminal_output as to
import stage
import commit

success_status = True
def pastport_init(location):
    # create the pastport metadata directory and make an initial commit for all the files present 
    create_metadata(location=location)
    # once init process (including the initial commit of all file(s)), write it to the .stagelog file
    stage.pastport_stage(pastport_root_location=location, init=True)

    # if the init process was successfull, print a success message to the terminal
    if success_status:
        to.output(message="\u2705  PASTPORT successfully initialized", color="g")

def create_metadata(location):
    global success_status
    try:
        # list all the files and folders in the given location
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
            # ignore traversing the meta data directories
            if directory != "pastport\u00b6":
                create_metadata(location=location + f"/{directory}")
        # for every location visited (except the metadata directory), create the the metadata directory
        os.mkdir(location + "/pastport\u00b6")

        for file in files_list:
            # make the initial commit of the file(s)
            commit.pastport_commit(file_location=location + f"/{file}", commit_message="Inititation of pastport")
        
    except:
        # in case of initializing the pastport which has already been initialized, issue a warning message
        to.output(message="\u26a0  [WARNING] PASTPORT has already been initialized at this location", color="r")
        success_status = False

     