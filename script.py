#!/usr/bin/env python3
import os
import shutil
import sys


color = {
    "red": "\033[31m",  # for errors
    "green": "\033[32m",
    "yellow": "\033[33m",  # for input
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",  # for indication
    "reset": "\033[0m",
}


# TODO: add usage of a global variable to hold the path
global_path = ""


def show_dirs(path=os.getcwd()):
    """
    Prints the files and directories in the specified path in column
    
    This function prints the files and folders in equally sapced columns
    according to the screen width
    
    Parameters: 
    path (str): Path of the directory (default = os.getcwd())
  
    Returns: 
    None 
    """
    print(color["cyan"] + "Contents of the current directory")
    filelist = os.listdir(path)
    filelist.sort(key=lambda x: x.lower())
    # index padding
    ind = len(filelist)
    if ind >= 1000:
        ind = 4
    elif ind >= 100:
        ind = 3
    elif ind >= 10:
        ind = 2
    else:
        ind = 1

    scr_width = int(os.get_terminal_size()[0])
    try:
        mlen = max(len(word) for word in filelist) + 1
    except ValueError:
        mlen = 1
    cols = scr_width // mlen

    if scr_width < mlen:
        mlen = scr_width

    line = ""
    lst = []
    for count, _file in enumerate(filelist, start=1):
        last = True  # last line
        # directories(blue)
        if os.path.isdir(path + os.sep + _file):
            _file = _file + os.sep
            st = "[{0:>{ind}}] {1:<{mlen}}".format(
                str(count), _file, mlen=mlen, ind=ind
            )
            if scr_width - (abs(len(line) - cols * 5) % scr_width) > len(st):
                line = line + color["blue"] + st
            else:
                lst.append(line)
                line = color["blue"] + st
                last = False
        # executeable files(yellow)
        elif os.access(path + os.sep + _file, os.X_OK):
            st = "[{0:>{ind}}] {1:<{mlen}}".format(
                str(count), _file, mlen=mlen, ind=ind
            )
            if scr_width - (abs(len(line) - cols * 5) % scr_width) > len(st):
                line = line + color["yellow"] + st
            else:
                lst.append(line)
                line = color["yellow"] + st
                last = False
        # other files(green)
        else:
            st = "[{0:>{ind}}] {1:<{mlen}}".format(
                str(count), _file, mlen=mlen, ind=ind
            )
            if scr_width - (abs(len(line) - cols * 5) % scr_width) > len(st):
                line = line + color["green"] + st
            else:
                lst.append(line)
                line = color["green"] + st
                last = False
    # append the last line to the list
    if last:
        lst.append(line)

    print("\n".join(lst))


def navmodedir():

    # TODO: complete docstring
    """
    short desc
    
    desc
    
    Parameters: 
    None
  
    Returns: 
    None 
    """
    print(color["cyan"] + "Current working directory is> " + os.getcwd())
    while True:
        show_dirs(os.getcwd())
        print(
            color["yellow"],
            "Enter directory index to move inside",
            "Press 'u' to exit current directory",
            "'x' to exit nav mode",
            "",
            sep="\n",
        )
        dir_action = input("Select >> ").lower()
        if dir_action.strip().isnumeric():
            _files = os.listdir(os.getcwd())
            _files.sort(key=lambda x: x.lower())
            filename = _files[int(dir_action) - 1]
            print(filename)
            os.chdir(str(os.getcwd()) + os.sep + filename)
            print(color["cyan"], "directory ->>> ", os.getcwd())
        elif dir_action == "u":
            foldername = os.path.split(os.getcwd())[0]
            os.chdir(foldername)
            print(color["cyan"], "directory ->>> ", os.getcwd())
        elif dir_action == "x":
            break
        else:
            print(color["red"] + "INVALID INPUT   !!! " + color["reset"])
            continue


def directory_ask(change_dir=False):

    # TODO: complete docstring
    """
    short desc
    
    desc
    
    Parameters: 
    change_dir (bool): 
  
    Returns: 
    None 
    """
    if not change_dir:
        print(
            color["red"],
            "Stay in {} [y]/n?".format(os.getcwd()),
            "or",
            "press r to enter navigation mode ",
            sep="\n",
        )
        a = input(color["red"] + "Select >> ")
        if a.lower() == "n":
            print(color["yellow"] + "Enter full path of the directory...")
            os.chdir(str(input("path>> ")))
        elif a.lower() == "r":
            navmodedir()
        else:
            pass

    else:
        print(color["yellow"] + "Enter full path of the directory...")
        os.chdir(str(input("path>> ")))
    show_dirs(os.getcwd())


def select_op():

    # TODO: complete docstring
    """
    short desc
    
    desc
    
    Parameters: 
    None
  
    Returns: 
    None 
    """
    print(
        color["yellow"] + "Select the operation:",
        " 1. Rename",
        " 2. Delete",
        " 3. Copy",
        " 4. Move",
        " 5. Create new folder/s, file/s",
        " 6. Enter into a directory",
        " 7. Enter navigation mode",
        " 9. Change directory",
        "99. EXIT",
        sep="\n",
    )
    selection = int(input("select>> "))
    show_dirs(os.getcwd())
    return selection


class Operations:
    def __init__(self, files):
        self.files = files

    def get_index(self):
        max_ind = len(self.files)
        indexes = []
        print(
            color["yellow"]
            + "Enter indexes eg. '7' or '3 6'\n"
            + "Enter range eg. '2-9'\n"
            + "Enter 'all' to select all files"
            + "Enter 'x' to exit"
        )
        inp = input(">> ")
        if inp.lower().strip() == "all":
            for ind in range(1, max_ind + 1):
                indexes.append(ind)
        elif inp.lower().strip() == "x":
            return -1
        else:
            for ind in inp.split(" "):
                try:
                    indexes.append(int(ind))
                except ValueError:
                    ind = ind.split("-")
                    for i in range(int(ind[0]), int(ind[1]) + 1):
                        try:
                            indexes.append(i)
                        except ValueError:
                            return None
        return indexes

    def rename(self):
        while True:
            print(color["yellow"] + "Enter file indexes to rename")
            indexes = self.get_index()
            if indexes is None:
                print(color["red"] + "ERROR No file selected"+color["reset"])
                continue
            elif indexes == -1:
                break
            print(color["yellow"])
            dont_over = (
                input("Overwrite prexisting files [y]/n?").strip().lower()
                == "n"
            )
            torename = list(map(lambda x: self.files[x - 1], indexes))
            for _file in torename:
                newname = str(input("Rename '" + _file + "' as>> "))
                if dont_over:
                    if os.path.exists(newname):
                        if (
                            input(_file + " already exists overwrite y/[n]?")
                            .strip().lower() == "y"
                        ):
                            os.rename(_file, newname)
                        else:
                            continue
                else:
                    os.rename(_file, newname)
            break

    def delete(self):
        while True:
            print("Enter file indexes to delete")
            indexes = self.get_index()
            if indexes is None:
                print(color["red"] + "ERROR No file selected"+color["reset"])
                continue
            elif indexes == -1:
                break
            todelete = list(map(lambda x: self.files[x - 1], indexes))
            print(color["yellow"])
            del_confirm = (
                input("Ask confirmaton to delete y/[n]?").strip().lower()
                == "y"
            )
            for i in todelete:
                if os.path.isdir(i):
                    if del_confirm:
                        if (input("Delete directory "+ i +" [y]/n?").strip().lower() == "n"):
                            continue
                    shutil.rmtree(i, ignore_errors=True)
                else:
                    if del_confirm:
                        if (input("Delete file "+ i +" [y]/n?").strip().lower() == "n"):
                            continue
                    os.remove(i)
            break

    def copy(self):
        print("Enter file indexes to copy")
        indexes = self.get_index()
        if indexes is None:
            print(color["red"] + "ERROR No file selected")
            return 0
        tocopy = list(map(lambda x: self.files[x - 1], indexes))
        for i in tocopy:
            path = str(input("where to copy (path/same) >> "))
            shutil.copy(i, path)

    def move(self):
        print("Enter file indexes to move")
        indexes = self.get_index()
        if indexes is None:
            print(color["red"] + "ERROR No file selected")
            return 0
        tomove = list(map(lambda x: self.files[x - 1], indexes))
        for i in tomove:
            path = input("where to move (path/same) >> ")
            shutil.move(i, path)

    def enter_dir(self):
        files = self.files
        dir_index = int(input("Enter directory index >>"))
        filename = files[int(dir_index) - 1]
        os.chdir(str(os.getcwd()) + os.sep + filename)
        show_dirs(os.getcwd())

    @staticmethod
    def create():
        print(
            color["yellow"]
            + "Select 1. to create Directories\n"
            + "       2. to create files\n"
        )
        ask = int(input(">> "))
        index = int(input("How many folders to create>> "))
        for i in range(index):
            if ask == 1:
                os.mkdir(input("Enter name of folder [{}]>> ".format(i + 1)))
            elif ask == 2:
                fname = input("Enter name of file along with extension>> ")
                if not os.path.exists(fname):
                    with open(fname, "w+"):
                        pass
                else:
                    print(color["red"] + "ERROR File already exists")


def main(path=os.getcwd()):
    print(
        color["magenta"],
        r"""
  _           _       _                                  _   _             
 | |__   __ _| |_ ___| |__     ___  _ __   ___ _ __ __ _| |_(_) ___  _ __  
 | '_ \ / _` | __/ __| '_ \   / _ \| '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \ 
 | |_) | (_| | || (__| | | | | (_) | |_) |  __/ | | (_| | |_| | (_) | | | |
 |_.__/ \__,_|\__\___|_| |_|  \___/| .__/ \___|_|  \__,_|\__|_|\___/|_| |_|
                                   |_|                                     
                _       _   
  ___  ___ _ __(_)_ __ | |_ 
 / __|/ __| '__| | '_ \| __|
 \__ \ (__| |  | | |_) | |_ 
 |___/\___|_|  |_| .__/ \__|
               |_|    
        """,
    )
    filelist = os.listdir(path)
    filelist.sort(key=lambda x: x.lower())
    oper_files = Operations(filelist)
    while True:
        oprselection = select_op()
        try:
            if oprselection == 1:
                oper_files.rename()
            elif oprselection == 2:
                oper_files.delete()
            elif oprselection == 3:
                oper_files.copy()
            elif oprselection == 4:
                oper_files.move()
            elif oprselection == 5:
                oper_files.create()
            elif oprselection == 6:
                oper_files.enter_dir()
            elif oprselection == 7:
                navmodedir()
            elif oprselection == 9:
                directory_ask(True)
            elif oprselection == 99:
                break
            else:
                continue
        except IndexError:
            continue


if __name__ == "__main__":
    try:
        if os.path.isdir(sys.argv[1]):
            os.chdir(sys.argv[1])
    except IndexError:
        pass
    directory_ask(False)
    main()

else:
    pass
