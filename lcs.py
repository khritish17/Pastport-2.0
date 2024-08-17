def LongestCommonSubsequences(old_line, new_line):
    '''
        [1] It finds the longest common consequences between the old and new line
        [2] Generates the commit data, such that new line is generated from old line and commit data
        returns LCS, commit data
    '''
    old_line = old_line.split(" ")
    new_line = new_line.split(" ")

    dp = [[0 for j in range(len(new_line) + 1)] for i in range(len(old_line) + 1)]
    for i in range(1, len(old_line) + 1):
        for j in range(1, len(new_line) + 1):
            if old_line[i - 1] == new_line[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1 
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])
    
    # backtrack to get the common parts
    i, j = len(dp) -1, len(dp[0]) - 1
    lcs = []
    while i != 0 and j != 0:
        old_line_word = old_line[i - 1] # i - 1 because dp is 1 length more in both sides
        new_line_word = new_line[j - 1]

        if old_line_word == new_line_word:
            i, j = i - 1, j - 1
            lcs = [(old_line_word, i, j)] + lcs # (common word, old_line_index, new_line_index)
        else:
            if dp[i][j-1] >= dp[i - 1][j]:
                j -= 1
            else:
                i -= 1
    
    commit_data_line = [] # will hold (insertion, deleteion)
    deletion = [(old_line[i], i) for i in range(len(old_line))]
    insertion = [(new_line[i], i) for i in range(len(new_line))]
    for common_word, old_index, new_index in lcs[::-1]:
        deletion.pop(old_index)
        insertion.pop(new_index)
    commit_data_line = [insertion, deletion]
    return lcs, commit_data_line