import os
import copy
from typing import List

class item(object):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.name = ""
        self.path = ""
        self.isDir = False
        self.isFile = False
        self.obligation = '+' # +:could !:should -:should'nt be here
        self.depth = 0
        self.parent = None
        self.setParent(parent)
        self.children = []

        self.missing = False
        self.unwanted = False

    def __addChild(self, child):
        self.children.append(child)
    def __delChild(self, child):
        self.children.remove(child)
    def setParent(self, parent):
        if self.parent is not None:
            self.parent.__delChild(self)
        self.parent = parent
        if self.parent is not None:
            self.parent.__addChild(self)
    def addChild(self, child):
        child.setParent(self)
    def deleteChild(self, child):
        child.setParent(None)

    def setValueToChild(self, name: str, value: any):
        item.__setattr__(self, name, value)
        for c in self.children:
            c.setValueToChild(name, value)

    def getParentFromDepth(self, depth):
        if self.parent is None:
            return self
        if self.depth < depth:
            return self
        return self.parent.getParentFromDepth(depth)

    def toStrFullPath(self):
        if self.parent is None:
            return ''
        return self.parent.toStrFullPath() + "/" + self.name

    def print(self, depth: int = 0):
        mistake = "❌" * self.unwanted + "⭕" * self.missing + "✅" * (not (self.unwanted + self.missing))
        typeChar = "📂" if self.isDir else "📄" if self.isFile else "🗿"
        print(mistake + "—" * depth + typeChar + self.name)
        if self.isDir:
            for c in self.children:
                c.print(depth + 1)

    def printToFile(self, file, depth: int = 0):
        
        mistake = "✅" if not (self.unwanted or self.missing) else "❌"
        mistake += "🗑" * self.unwanted + "📌" * self.missing
        typeChar = "📂" if self.isDir else "📄" if self.isFile else "🗿"
        # print(mistake + "—" * depth + typeChar + self.name)
        name = "  " * depth + typeChar + self.name
        l = [name + "—" * (80 - len(name)) + "\t" + mistake + "\n"]
        if self.isDir:
            for c in self.children:
                l += c.printToFile(file, depth + 1)
        if depth == 0:
            with open(file, "w+", encoding="utf-8") as f:
                f.writelines(l)
        return l


    def toStr(self, depth: int = 0) -> str:
        typeChar = "/" if self.isDir else "&" if self.isFile else "?"
        line = " " * depth + typeChar + self.obligation + self.name + "\n"
        if self.isDir:
            for c in self.children:
                line += c.toStr(depth + 1)
        return line

    def isIn(self, others: List['item']) -> bool:
        for o in others:
            if o.name == "*":
                print(self.name, o.name, item.matchnmatch(self.name, o.name))
            if item.matchnmatch(self.name, o.name):
                return True
        return False
    
    @staticmethod
    def matchnmatch(a, b) -> bool:
        if len(a) == 0:
            return False
        if len(b) == 0:
            return True
        if a[0] == b[0]:
            return item.matchnmatch(a, b[1:])
        if b[0] == '*':
            return item.matchnmatch(a, b[1:])
        if a[0] != b[0]:
            return item.matchnmatch(a[1:], b)


    def compareTo(self, other: 'item'):
        if other == None:
            print("{} is None".format(self.name))
            return
        if self.name != other.name:
            print("{} != {}".format(self.name, other.name))
        for c in self.children:
            if not c.isIn([x for x in other.children if x.obligation != '-']):
                # print("unwanted : {}".format(c.toStrFullPath()))
                c.setValueToChild("unwanted", True)
                continue
            for oc in other.children:
                if oc == None:
                    print("{} is None".format(c.toStrFullPath()))
                    continue
                if c.name == oc.name:
                    if not ((c.isFile and oc.isFile) or (c.isDir and oc.isDir)):
                        print("{} and {} are not the same kind of file/directory".format(c.name, oc.name))
                    c.compareTo(oc)
        for oc in other.children:
            if oc.name not in [x.name for x in self.children if oc.obligation != '!']:
                # print("missing : {}".format(oc.toStrFullPath()))
                c = copy.deepcopy(oc)
                c.setValueToChild("missing", True)
                self.addChild(c)
        return self

    def __str__(self) -> str:
        return self.name + " " + str(self.depth)

    @staticmethod
    def getTreeFromPath(path: str, depth: int=0) -> 'item':
        if not os.path.isdir(path) and not os.path.isfile(path):
            return
        file = item()
        file.name = os.path.basename(path)
        file.path = path
        file.isDir = os.path.isdir(path)
        file.isFile = os.path.isfile(path)

        if file.isDir:
            childrens = os.listdir(path)
            for c in childrens:
                p = os.path.join(path, c)
                file.addChild(item.getTreeFromPath(p, depth + 1))
        return file

    @staticmethod
    def getTreeFromFile(path: str, depth: int=0) -> 'item':
        with open(path, "r") as f:
            try:
                lines = f.readlines()
                prev = None
                for l in lines:
                    if len(l.strip()) < 2:
                        continue
                    depth = len(l) - len(l.lstrip(' '))
                    if prev is None:
                        current = item()
                    else:
                        current = item(prev.getParentFromDepth(depth))
                    cmd = l.lstrip(' ')
                    current.isDir = True if cmd[0] == "/" else False
                    current.isFile = True if cmd[0] == "&" else False
                    current.name = cmd[2:].rstrip()
                    current.depth = depth
                    current.obligation = cmd[1]
                    # print(current.name, current.depth, str(current.parent))
                    prev = current
                return current.getParentFromDepth(0)
            except:
                print("Error reading file")
                return item()
        return item()

    @staticmethod
    def load(file):
        with open(file, "r") as f:
            pass
    def save(self, file: str):
        if not file.endswith(".tree"):
            file += ".tree"
        with open(file, "w+") as f:
            f.write(self.toStr())
            

def listFolder(path, depht=0):
    l = [os.path.basename(path)]
    childrens = os.listdir(path)
    for c in childrens:
        p = os.path.join(path, c)
        if os.path.isdir(p):
            print(" " * depht + c)
            l.append(listFolder(p, depht + 1))
        if os.path.isfile(p):
            print(" " * (depht + 1) + c)
            l.append(c)
    return l
        

# print(listFolder(r"Q:\bank\bankCS\ressources\projectTemplate\nomDuProjet"))
# projectFolder = item.getTreeFromPath(r"Q:\bank\bankCS\ressources\projectTemplate\nomDuProjet")
# print(projectFolder.toStr())
# projectFolder.save(r"S:\a.paris\Atelier\Gapalion\resources\drills\folders\cs-template")

# projectFolder = item.getTreeFromFile(r"projectTemplate\template.tree")
# item.getTreeFromFile(r"projectTemplate\template.tree").compareTo(item.getTreeFromPath(r"projectTemplate\nomDuProjet"))
# item.getTreeFromPath(r"D:\creative seed\projet\pnl").compareTo(item.getTreeFromFile(r"projectTemplate\template.tree")).print()
# item.getTreeFromPath(r"projectTemplate\nomDuProjet").compareTo(item.getTreeFromFile(r"projectTemplate\template.tree")).print()
# item.getTreeFromPath(r"D:\creative seed\projet\pfa").compareTo(item.getTreeFromFile(r"projectTemplate\template.tree")).printToFile("pfa.tree")
item.getTreeFromPath(r"S:\a.paris\Atelier\sosuke").compareTo(item.getTreeFromFile(r"resources\drills\folders\cs-template.tree")).printToFile("sosuke.result")

