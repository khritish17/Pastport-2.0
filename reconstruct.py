import lcs as l

def reconstruct(old_line, commit_data_line):
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

    

# o, n = "Hey there whatsup man", "Hi whatsup my man"
# lcs, cd = l.LCS(old_line=o, new_line=n)
# print(reconstruct(old_line=o, commit_data_line=cd))