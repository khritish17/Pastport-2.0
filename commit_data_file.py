import lcs as LCS
import os
import terminal_output as to 

def commit_data_file(old_file_location, new_file_location):
    old_file_location = os.path.abspath(old_file_location)
    new_file_location = os.path.abspath(new_file_location)
    
    if (not os.path.exists(old_file_location)) or (not os.path.exists(new_file_location)):
        to.output(message="\u26a0  Invalid file location detected [cdf] !!!",color="r")
        exit()

    old_file = open(old_file_location, "r")
    old_file_lines = old_file.readlines()
    old_file.close()

    new_file = open(new_file_location, "r")
    new_file_lines = new_file.readlines()
    new_file.close()
    
    commit_data = {}
    for i in range(max(len(old_file_lines), len(new_file_lines))):
        try:
            old_line = old_file_lines[i]
            old_line = old_line.rstrip("\n")
        except:
            old_line = ""
        try:
            new_line = new_file_lines[i]
            new_line = new_line.rstrip("\n")
        except:
            new_line = ""
        _, cd = LCS.LongestCommonSubsequences(old_line=old_line, new_line=new_line)
        commit_data[i] = cd
    return commit_data
