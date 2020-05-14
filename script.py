#!/usr/bin/env python3
import os
import shutil

color = {
    "red": "\033[31m",
    "green": "\033[32m",
    "orange": "\033[33m",
    "purple": "\033[35m",
    "cyan": "\033[36m",
    "yellow": "\033[93m",
}

# colors off
# color = {
#     "red": "",
#     "green": "",
#     "orange": "",
#     "purple": "",
#     "cyan": "",
#     "yellow": "",
# }


def show_dirs():
    filelist = os.listdir(os.getcwd())
    filelist.sort()
    ind = len(filelist)
    if ind >= 1000:
        ind = 4
    elif ind >= 100:
        ind = 3
    elif ind >= 10:
        ind = 2
    else:
        ind = 1

    scr_width = int(os.popen("stty size", "r").read().split()[1])
    mlen = max(len(word) for word in filelist) + 1

    print(color["cyan"] + "Files in the current directory")

    if scr_width < mlen:
        mlen = scr_width

    line = ""
    lst = []
    for count, _file in enumerate(filelist, start=1):
        if os.path.isdir(_file):
            _file = _file + os.sep
            st = "[{0:>2}] {1:<{mlen}}".format(str(count), _file, mlen=mlen)
            if scr_width - (len(line) % scr_width) > len(st):
                line = line + color["cyan"] + st
            else:
                lst.append(line)
                line = color["cyan"] + st

        else:
            st = "[{0:>2}] {1:<{mlen}}".format(str(count), _file, mlen=mlen)
            if scr_width - (len(line) % scr_width) > len(st):
                line = line + color["green"] + st
            else:
                lst.append(line)
                line = color["green"] + st

    print("\n".join(lst))


def directory_ask():
    print(
        color["red"] + "Enter directory name:",
        color["green"],
        " 1. Custom directory",
        " 2. Current directory",
        "99. EXIT",
        sep="\n",
    )
    dir_select = int(input("select>> "))

    if dir_select == 1:
        print(color["orange"] + "Enter path of working directory...")
        os.chdir(str(input("path>> ")))
        print("here is the dir", os.getcwd())

    elif dir_select == 2:
        print("your working directory is", os.getcwd(), "\n")
    show_dirs()


def select_op():
    print(
        color["orange"],
        "Select the operation:",
        " 1. Rename",
        " 2. Delete",
        " 3. Copy",
        " 4. Move",
        " 5. Create new folder/s, file/s",
        " 9. enter into a directory",
        "99. EXIT",
        sep="\n",
    )
    selection = int(input("select>> "))
    show_dirs()
    return selection


def change_cwd():
    os.chdir(input("Enter the path>> "))
    print("Working directory is changed to:", os.getcwd())


class Operations:
    def __init__(self, files):
        self.files = files

    def get_index(self):
        max_i = len(self.files)
        indexes = []
        print(
            "Enter indexes eg. 3 6\n"
            + "Enter range eg. 2-9\n"
            + "Enter 'all' to select all files"
        )
        inp = input(">>")
        if inp == "all":
            for i in range(1, max_i + 1):
                indexes.append(i)
        else:
            for i in inp.split(" "):
                try:
                    indexes.append(int(i))
                except ValueError:
                    i = i.split("-")
                    for _ in range(int(i[0]), int(i[1]) + 1):
                        try:
                            indexes.append(_)
                        except ValueError:
                            print("ERROR enter proper values:")
                            return None
        return indexes

    def rename(self):
        print("Enter file indexes to rename>> ")
        indexes = self.get_index()
        if indexes == None:
            print("No file selected")
            return 0
        torename = list(map(lambda x: self.files[x - 1], indexes))
        for _file in torename:
            newname = str(input("rename " + _file + "as>> "))
            os.rename(_file, newname)

    def delete(self):
        print("Enter file indexes to delete>> ")
        indexes = self.get_index()
        if indexes == None:
            print("No file selected")
            return 0
        todelete = list(map(lambda x: self.files[x - 1], indexes))
        for i in todelete:
            try:
                os.remove(i)
            except IsADirectoryError:
                shutil.rmtree(i, ignore_errors=True)

    def copy(self):
        print("Enter file indexes to copy>> ")
        indexes = self.get_index()
        if indexes == None:
            print("No file selected")
            return 0
        tocopy = list(map(lambda x: self.files[x - 1], indexes))

        for i in tocopy:

            path = str(input("where to copy (path/same) >> "))
            command = "cp -arv " + copypath + " " + path
            os.system(command)

    def move(self):
        print("Enter file indexes to move>> ")
        indexes = self.get_index()
        if indexes == None:
            print("No file selected")
            return 0
        tomove = list(map(lambda x: self.files[x - 1], indexes))
        for i in tomove:
            command = "mv " + i + " " + input("where to move (path/same) >> ")
            os.system(command)

    def createdir(self):
        print(color["orange"], "")
        ask = int(
            input("what do you want to create 1. Folders   2. Files  >> ")
        )
        index = int(input("how many folders to create>> "))
        for i in range(index):
            if ask == 1:
                os.mkdir(input("enter name of folder >> "))
            elif ask == 2:
                command = "cat > " + input(
                    "Enter name of file along with extension>> "
                )
                os.system(command)

    def changefolder(self):
        change_cwd()


if __name__ == "__main__":
    while True:
        directory_ask()
        filelist = os.listdir(os.getcwd())
        filelist.sort()
        oper_files = Operations(filelist)
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
                oper_files.createdir()
            elif oprselection == 99:
                break
            else:
                continue
        except IndexError:
            continue
