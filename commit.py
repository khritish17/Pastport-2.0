import os
import terminal_output as to
import commit_data_file as cdf
import shutil

def pastport_commit(file_location, commit_message = "Untitled Commit Message"):
    # assuming the file location is valid
    # assuming the commit_is is valid and not ambigious
    # we need the commit data, which required the old file and the new file
    new_file_location = os.path.abspath(file_location)
    old_file_location = os.path.dirname(new_file_location) + "/pastport\u00b6/" + os.path.basename(new_file_location)
    if os.path.exists(old_file_location):
        file_name, ext_name = os.path.splitext(os.path.basename(new_file_location))
        track_file_location = os.path.dirname(new_file_location) + f"/pastport\u00b6/{file_name}_{ext_name[1:]}.track"
        
        # commit data line wise
        commit_data = cdf.commit_data_file(old_file_location=old_file_location, new_file_location=new_file_location)
        track_file = open(track_file_location, "r")
        track_lines = track_file.readlines()
        track_file.close()
        last_commit_id = int(track_lines[-1].split("\u00b6")[0])
    else:
        # trying to commit new files
        file_name, ext_name = os.path.splitext(os.path.basename(new_file_location))
        files_dirs = os.listdir(os.path.dirname(new_file_location))
        if "pastport\u00b6" not in files_dirs:
            os.mkdir(os.path.dirname(new_file_location) + "/pastport\u00b6")
        shutil.copy2(src=new_file_location, dst=os.path.dirname(new_file_location) + f"/pastport\u00b6/{file_name}{ext_name}")
        track_file_location = os.path.dirname(new_file_location) + f"/pastport\u00b6/{file_name}_{ext_name[1:]}.track"
        with open(track_file_location, "w") as track_file:
            track_file.write(f"0\u00b6Inititation of pastport\n")
        last_commit_id = 0
        return 
    
    with open(track_file_location, "a") as track_file:
        # write the commit id
        track_file.write(f"{last_commit_id + 1}")

        # write the commit data
        for line_number, commit_data_line in commit_data.items():
            insertion = commit_data_line[0]
            ins_len = len(insertion)
            deletion = commit_data_line[1]
            del_len = len(deletion)
            track_file.write(f"\u00b6{line_number}\u00b6{ins_len}\u00b6{del_len}")
            # inserting the insertion array
            for ins_word, ins_index in insertion:
                track_file.write(f"\u00b6{ins_word}\u00b6{ins_index}")
            
            # inserting the deletion array
            for del_word, del_index in deletion:
                track_file.write(f"\u00b6{del_word}\u00b6{del_index}")

        # end the line with new line character
        track_file.write(f"\u00b6{commit_message}\n")

# pastport_commit(r"C:\Users\HP\Desktop\test\New Text Document.txt")# 
