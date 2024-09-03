import terminal_output as TO
def help():
    # init command help
    TO.output(message="[1] 'init' command:", color="c")
    print("Initializes the PASTPORT system, creates the necessary directory structure and tracking files for version control")
    print("Sample Output:")
    TO.output(message="init", color="b")
    print()

    # status command help
    TO.output(message="[2] 'status' command:", color="c")
    print("Provides functionality to check the status of the working directory, identifying modified, untracked, and deleted files")
    print("Sample Output:")
    TO.output(message="status", color="b")
    print()

    # commit command help
    TO.output(message="[3] 'commit <message>' command:", color="c")
    print("Saves the current version of the whole directory")
    print("Sample Output:")
    TO.output(message="commit 'This is the first commit message' ", color="b")
    print()

    # log command help
    TO.output(message="[4] 'log' command:", color="c")
    print("Keeps track of all commits made till now.")
    print("Sample Output:")
    TO.output(message="log", color="b")
    print()

    # checkout command help
    TO.output(message="[5] 'checkout <commit number>' command:", color="c")
    print("Allows to revert back to a specific version by specifying the commit nums")
    print("Sample Output:")
    TO.output(message="checkout 1", color="b")
    print()