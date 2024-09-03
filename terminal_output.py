def output(message, color = "", ends = "\n"):
    if color.lower() == "red" or color.lower() == "r":
        print('\x1b[1;31;40m' + message + '\x1b[0m', end=ends)
    elif color.lower() == "green" or color.lower() == "g":
        print('\x1b[1;32;40m' + message + '\x1b[0m', end=ends)
    elif color.lower() == "amber" or color.lower() == "a":
        print('\x1b[1;33;40m' + message + '\x1b[0m', end=ends)
    elif color.lower() == "blue" or color.lower() == "b":
        print('\x1b[1;34;40m' + message + '\x1b[0m', end=ends)
    elif color.lower() == "pink" or color.lower() == "p":
        print('\x1b[1;35;40m' + message + '\x1b[0m', end=ends)
    elif color.lower() == "cyan" or color.lower() == "c":
        print('\x1b[1;36;40m' + message + '\x1b[0m', end=ends)
    else:
        print('\x1b[1;37;40m' + message + '\x1b[0m', end=ends)



