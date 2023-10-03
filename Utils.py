colorCode = {
    "purple" : '\033[95m',
    "blue" : '\033[94m',
    "cyan" : '\033[96m',
    "green" : '\033[92m',
    "yellow" : '\033[93m',
    "red" : '\033[91m',
    "end" : '\033[0m'
}

#Print with color function
def printc(text, color = ''):
    if color.lower() in colorCode:
        print(colorCode[color].lower() + text + colorCode["end"])
    else:
        print(text)

#Input with color function
def inputc(text, color = ''):
    result = ""
    if color.lower() in colorCode:
        result = input(colorCode[color].lower() + text + colorCode["end"])
    else:
        result = input(text)

    return result

