# -- coding: utf-8 --
import os
import io


class Scope(object):
    def __init__(self, parent=None):
        self.condition = None
        self.start = (0, 0, "MAIN")
        self.end = (0, 0, "ENDMAIN")
        self.content = []

        self.parent = None
        self.childrens = []
        self.setParent(parent)

    def setParent(self, parent):
        self.parent = parent
        if parent is not None:
            parent.__addChildren(self)

    def addChildren(self, child):
        if child is None:
            return
        child.setParent(self)

    def __addChildren(self, child):
        self.childrens.append(child)

    @staticmethod
    def __getBaliseFromHtml(html):
        balises = []
        i = -1
        while(True):
            i = html.find('{%', i + 1)
            j = html.find('%}', i + 1)
            if i == -1:
                break
            b = (i, j + 2, html[i + 2:j].split())
            balises.append(b)
        return balises

    def close(self, balise, html):
        self.end = balise
        start = self.start
        for c in self.childrens:
            if start[1] != c.start[0]:
                self.content.append(html[start[1]:c.start[0]])
            self.content.append(c)
            start = c.end
        self.content.append(html[start[1]:self.end[0]])

    @staticmethod
    def getScopesFromHtml(html):
        balises = Scope.__getBaliseFromHtml(html)

        current = Scope()
        for b in balises:
            if b[2][0].upper().startswith("END"):
                #close scope
                current.close(b, html)

                current = current.parent
            else:
                #open scope
                current = Scope(parent=current)
                current.condition = b[2]
                current.start = b
        current.close((len(html), len(html), "MAIN"), html)
        return current

    @staticmethod
    def splitnonalpha(s):
        pos = 1
        while pos < len(s) and (s[pos].isalpha() or s[pos] == "_"):
            pos+=1
        return (s[:pos], s[pos:])

    @staticmethod
    def getValueContext(name, context):
        #get first word
        s, e = Scope.splitnonalpha(name)
        if s in context:
            command = """context["{}"]{}""".format(s, e)
            return eval(command)
        return name

    @staticmethod
    def loadContextualHtml(html, context):
        v = []
        j = -1
        i = -1
        while(True):
            i = html.find('{{', i + 1)
            j = html.find('}}', i + 1)
            if i == -1:
                break
            name = html[i + 2:j].replace(" ", "")
            v = Scope.getValueContext(name, context)
            if v != None:
                html = html[:i] + unicode(v) +  html[j + 2:]
        return html 

    def runScopeChildrenContext(self, context):
        html = ""
        for c in self.content:
            if type(c) == Scope:
                html += c.runContext(context)
            else:
                html += Scope.loadContextualHtml(c, context)
        return html

    def runContext(self, context):
        html = ""
        if self.condition is None:
            html += self.runScopeChildrenContext(context)
        elif self.condition[0].upper() == "FOR":
            posIn = self.condition.index("in")
            vars = self.condition[1:posIn]
            listFor = self.condition[posIn + 1]
            listFor = Scope.getValueContext(listFor, context)
            listFor = [] if listFor is None else listFor
            for args in listFor:
                if len(vars) == 1:
                    context[vars[0]] = args
                    html += self.runScopeChildrenContext(context)
        elif self.condition[0].upper() == "IF":
            cond = self.condition[1:]
            for i, c in enumerate(cond):
                #if it's a variable, change it to it's value
                if c[0].isalpha() or c[0] == "_":
                    result = Scope.getValueContext(c, context)
                    cond[i] = str(result)
            # evaluate the condition
            command = " ".join(cond)
            v = eval(command)
            if v:
                html += self.runScopeChildrenContext(context)
        else:
            html += self.runScopeChildrenContext(context)
        html = os.linesep.join([s for s in html.splitlines() if s])
        return html

    def __repr__(self):
        return str(self.content)
