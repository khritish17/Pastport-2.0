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
    description = "Sets up the PASTPORT system, creates required directories, and configures version control tracking"
    example = ["init"]
    print_message(count = 1,command=command, description=description, example=example)
    
    # ADD command
    command = "add"
    description = "To streamline the commit process, group files that need to be committed together. This ensures that during checkout, all related files are retrieved automatically, eliminating the need for manual selection"
    sub_commands_description = {}
    sub_commands_description["add -a"] = "Add all files in the current directory and its subdirectories for grouping"
    sub_commands_description["add -p"] = "Add only the specified files for grouping"
    example = ["add -a", "add -p"]
    print_message(count = 2,command=command, description=description, sub_commands_description=sub_commands_description, example=example)

    # STATUS command
    command = "status"
    description = "Displays the status of files in the working directory and its subdirectories, highlighting modified, untracked, and deleted files"
    example = ["status"]
    print_message(count = 3, command=command, description=description, example=example)

    # COMMIT command
    command = "commit"
    description = "Commits the staged files to the repository"
    sub_commands_description = {}
    sub_commands_description['commit'] = "Commits the staged changes to the repository, prompting for a commit message afterward"
    sub_commands_description['commit -m "<Your commit message>"'] = "Commits the staged changes to the repository with the provided commit message enclosed in double quotes"
    example = ["add -a", "add -p"]
    print_message(count = 4, command=command, description=description, sub_commands_description=sub_commands_description, example=example)

    # LOG command
    command = "log"
    description = "Shows a list of committed files, including their stage, commit ID, and associated files"
    sub_commands_description = {}
    sub_commands_description['log'] = "Shows the full path (absolute location) of the files"
    sub_commands_description['log -sp'] = "Shows a shortened version of the file paths for better readability"
    sub_commands_description['log -lp'] = "Equivalent to the 'log' command"
    example = ["log", "log -sp", "log -lp"]
    print_message(count = 5, command=command, description=description, sub_commands_description=sub_commands_description, example=example)

    # CHECKOUT command
    command = "checkout"
    description = "Restores previous versions of files"
    sub_commands_description = {}
    sub_commands_description["checkout -s <stage id>"] = "Restores files to a specific version based on the provided stage ID and commit ID"
    sub_commands_description['checkout -p “<file1 path>, <file1 commit id>, <file2 path>, <file2 commit id>”'] = "Restores individual files to a specified version based on the commit ID and file path"
    example = ["checkout -s 3", 'checkout -p "D:\Codes\Projects\Pastport 2\cli.py,2"']
    print_message(count = 6, command=command, description=description, sub_commands_description=sub_commands_description, example=example)
