import lcs as l
import os

def reconstruct(old_line, commit_data_line):
    """
        [1] Generates the new line from old line and commit data
    """
    # here each individual line and its commit data are required
    old_line = old_line.split(" ")
    insertion, deletion = commit_data_line
    constructed_line = [None]*(len(old_line) + len(insertion) - len(deletion))
    # remove the words which needs to be deleted from old line
    for del_word, del_index in deletion[::-1]:
        old_line.pop(del_index)
    
    # insert the words which needs to be inserted in the constructed line
    for ins_word, ins_index in insertion:
        constructed_line[ins_index] = ins_word
    for i in range(len(constructed_line)):
        if constructed_line[i] == None:
            constructed_line[i] = old_line.pop(0)
    return " ".join(constructed_line)

def reconstruct_file(old_file_location, commit_data):
    # assuming the old_file_location is valid 
    # assuming commit_data is valid in reference with the file
    new_file = []
    old_file = open(old_file_location, "r")
    old_lines = old_file.readlines()
    old_file.close()
    for i in range(max(len(old_lines), len(commit_data))):
        try:
            old_line = old_lines[i]
        except:
            old_line = ""
        try:
            commit_data_line = commit_data[i]
        except:
            print("Error in line 37: recontruct.py")
        constructed_line = reconstruct(old_line=old_line, commit_data_line=commit_data_line)
        new_file.append(constructed_line)
    return new_file

# o, n = "Hey there whatsup man", "Hey there whatsup man"
# lcs, cd = l.LongestCommonSubsequences(old_line=o, new_line=n)
# print(reconstruct(old_line=o, commit_data_line=cd))