import terminal_output as TO

def print_message(count = 0, command = "", description = "", sub_commands_description = {}, example = []):
    TO.output(message=f"[{count}]")
    TO.output(message = f"Command:\u26a1  '{command}'", color="c")
    print("Description:", end=" ")
    TO.output(message=description, color="g")
    for cmds, desc in sub_commands_description.items():
        TO.output(message=f"\u26a1  {cmds}:", ends= " ")
        TO.output(message=desc, color="b")
    if example:
        TO.output(message="Example:")
        for ex in example:
            TO.output(message="\u26a1  >>> " + ex)
    print()

def help():
    # INIT command
    command = "init"
    description = "Initializes the PASTPORT system, creates the necessary directory structure and tracking files for version control"
    example = ["init"]
    print_message(count = 1,command=command, description=description, example=example)
    
    # ADD command
    command = "add"
    description = "Before making a commit, file(s) which are supposed to be commited, needs to be commited in a batch so that during checkout one does not have to worry about individual files that need to checkout manually"
    sub_commands_description = {}
    sub_commands_description["add -a"] = "Stage every file(s) in the current directory and all its sub directories"
    sub_commands_description["add -p"] = "Stage only those file(s) whose location has been provided"
    example = ["add -a", "add -p"]
    print_message(count = 2,command=command, description=description, sub_commands_description=sub_commands_description, example=example)

    # STATUS command
    command = "status"
    description = "Provides functionality to check the status of the working directory, identifying modified, untracked, and deleted files"
    example = ["status"]
    print_message(count = 3, command=command, description=description, example=example)

    # COMMIT command
    command = "commit"
    description = "Saves the current version of the file(s) which are staged"
    sub_commands_description = {}
    sub_commands_description['commit'] = "Commits the current version of the staged file, asks for commit message later"
    sub_commands_description['commit -m "<Your commit message>"'] = "Commits the current version of the staged file, while commit message is provided within the double quotes"
    example = ["add -a", "add -p"]
    print_message(count = 4, command=command, description=description, sub_commands_description=sub_commands_description, example=example)

    # LOG command
    command = "log"
    description = "Displays all those file(s) which are commited, including its stage and commit id, and file(s) which took part in the commit"
    sub_commands_description = {}
    sub_commands_description['log'] = "Displays the absolute location of the file(s)"
    sub_commands_description['log -sp'] = "Displays the shorten location of the file(s)"
    sub_commands_description['log -lp'] = "Same as 'log' command"
    example = ["log", "log -sp", "log -lp"]
    print_message(count = 5, command=command, description=description, sub_commands_description=sub_commands_description, example=example)

    # CHECKOUT command
    command = "checkout"
    description = "Reverts the files to go back to different versions of the file(s)"
    sub_commands_description = {}
    sub_commands_description["checkout -s <stage id>"] = "Allows the file(s) used during the given stage id, to revert back to version according tp the commid id used in the stage id"
    sub_commands_description['checkout -p “<file1 path>, <file1 commit id>, <file2 path>, <file2 commit id>”'] = "Allows individual file(s) irrespective of stage to revert back to the version specified by commit id and file path"
    example = ["checkout -s 3", 'checkout -p "D:\Codes\Projects\Pastport 2\cli.py,2"']
    print_message(count = 6, command=command, description=description, sub_commands_description=sub_commands_description, example=example)
