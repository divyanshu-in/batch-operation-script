import os

tag = "test"

currentwd = os.getcwd()

class colors: 

    class fg: 
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        purple='\033[35m'
        cyan='\033[36m'
        yellow='\033[93m'
    

def directoryask():
    print(colors.fg.red, "enter directory name:",colors.fg.green, "1. Custom directory", "2. Current directory", "99. EXIT", sep='\n', end='\n\n')
    dirSelect = int(input("select>> "))
    
    if dirSelect == 1:
        print(colors.fg.orange, "Enter path of working directory...")
        os.chdir(str(input("select>> ")))
        print("here is the dir", )

    elif dirSelect == 2:
        print("your working directory is", os.getcwd())
    showDirectories()
    
def selectOP():
    print(colors.fg.orange,"select the operation", "1. Rename", "2. Delete", "3. Copy", "4. Move", "5. Create new folder/s, file/s", "9. enter into a directory", "99. EXIT", sep="\n", end='\n\n')
    print('\n')
    selection = int(input("select>> "))
    showDirectories()
    return selection

def showDirectories():
    filelist = os.listdir(os.curdir)
    filelist.sort()
    index = 1
    for i in filelist:
        
        print(colors.fg.cyan,str(index) + ". " + i)
        index += 1

class operations:

    def __init__(self, files):
        self.files = files

    showDirectories()        

    def rename(self):

        indexes = list(map(int, ((input("enter file indexes to rename>> ").split(" ")))))
        torename = list(map(lambda x: self.files[x - 1], indexes))
        for i in torename:
            newname = str(input("rename " + i + "as>> " ))
            os.rename (i, newname)
    
    def delete(self):
        indexes = list(map(int, ((input("enter file indexes to delete>> ").split(" ")))))
        todelete = list(map(lambda x: self.files[x - 1], indexes))
        for i in todelete:
            try:
                os.remove(i)
            except IsADirectoryError:
                os.rmdir(i)

    def copy(self):
        indexes = list(map(int, ((input("enter file indexes to copy>> ").split(" ")))))
        tocopy = list(map(lambda x: self.files[x - 1], indexes))

        for i in tocopy:

            path = str(input("where to copy (path/same) >> "))
            command = 'cp -arv ' + copypath + " " + path
            os.system(command)


    def move(self):
        indexes = list(map(int, ((input("enter file indexes to move>> ").split(" ")))))
        tomove = list(map(lambda x: self.files[x - 1], indexes))
        for i in tomove:
            command = "mv " + i + " " + input("where to move (path/same) >> ")
            os.system(command)

    def createdir(self):
        print(colors.fg.orange, "")
        ask = int(input("what do you want to create 1. Folders   2. Files  >> "))
        index = int(input("how many folders to create>> "))
        for i in range(index):
            if ask == 1:
                os.mkdir(input("enter name of folder >> "))
            elif ask ==2:
                command = 'cat > ' + input("Enter name of file along with extension>> ")
                os.system(command)
                
    def changefolder(self):
        changeCWD()

def changeCWD():
    os.chdir(input("Enter the path>> "))
    print("working directory is changed to", os.getcwd())



if __name__ == "__main__":
    while True:
        directoryask()
        filelist = os.listdir(os.getcwd())
        filelist.sort()

        oprselection = selectOP()
        if oprselection ==1:
            operations(filelist).rename()
        elif oprselection == 2:
            operations(filelist).delete()
        elif oprselection == 3:
            operations(filelist).copy()
        elif oprselection == 4:
            operations(filelist).move()
        elif oprselection == 5:
            operations(filelist).createdir()
        elif oprselection == 99:
            break
