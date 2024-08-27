import os
import reconstruct as re
import terminal_output as TO

def pastport_checkout(new_file_location, commit_id):
    new_file_location = os.path.abspath(new_file_location)
    file_name_with_extension = os.path.basename(new_file_location)
    file_name, extension = os.path.splitext(file_name_with_extension)
    track_file_location = os.path.dirname(new_file_location) + f"/pastport\u00b6/{file_name}_{extension[1:]}.track"
    old_file_location = os.path.dirname(new_file_location) + f"/pastport\u00b6/{file_name_with_extension}"
    
    commit_data = {}
    with open(track_file_location, "r") as track_file:
        try:
            track_line = track_file.readlines()[commit_id]
        except:
            TO.output(message="\u26a0  [Error]: Invalid commit id!!!", color="r")
            return 
        commit_data = extract_commit_data(tracked_line=track_line)
    new_file_lines = re.reconstruct_file(old_file_location=old_file_location, commit_data=commit_data)
    with open(new_file_location, "w") as new_file:
        for new_line in new_file_lines:
            new_file.write(new_line + "\n")


def extract_commit_data(tracked_line):
    tracked_line = tracked_line.strip("\n")
    cd = {}
    tracking_data = tracked_line.split("\u00b6")
    commit_message = tracking_data[-1]
    pointer = 0
    while pointer < len(tracking_data) - 2:
        pointer += 1
        line_number = int(tracking_data[pointer])
        insertion = []
        deletion = []
        
        pointer += 1
        ins_len = int(tracking_data[pointer])
        
        pointer += 1
        del_len = int(tracking_data[pointer])
        for _ in range(ins_len):
            pointer += 1
            ins_word = tracking_data[pointer]
            pointer += 1
            ins_index = int(tracking_data[pointer])
            insertion.append((ins_word, ins_index))
        for _ in range(del_len):
            pointer += 1
            del_word = tracking_data[pointer]
            pointer += 1
            del_index = int(tracking_data[pointer])
            deletion.append((del_word, del_index))
        cd[line_number] = [insertion, deletion]
    return cd

# pastport_checkout(r"C:\Users\HP\Desktop\test\New Text Document.txt", 4)