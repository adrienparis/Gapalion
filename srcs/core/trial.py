
# -- coding: utf-8 --

class ExerciceResult:
    title = ""
    passed = False
    message = ""
    explanation = ""
    author = ""

class TrialInterface:
    def execute(self):
        pass

    @staticmethode
    def execute_all_trials(trials):
        '''sort trial by type'''
        pass


class Trial():
    def __init__(self, title, func):
        self.title = title
        self.explanation = ""
        self.author = ""
        self.email = ""
        self.image = "gears"
        
        self.func = func
        self.passed = False
        self.errors = []
    
    def loadTrial(self, module):
        if hasattr(module, '__author__'):
            if module.__author__ != "prenom NOM":
                self.author = unicode(module.__author__)
        if hasattr(module, '__email__'):
            self.email = unicode(module.__email__)
        if hasattr(module, 'explanation'):
            self.explanation = unicode(module.explanation)
        if hasattr(module, '__doc__'):
            self.explanation = unicode(module.__doc__)
        if hasattr(module, 'image'):
            if module.image != "":
                self.image = unicode(module.image)

    def start(self):
        self.passed, self.errors = False, []
        try:
            value = self.func()
        except Exception as e:
            e = str(e)
            print("FAILED : " + self.title)
            print("\t" + e)
            if self.author == "":
                errorMessage = ["This trial has failed because it was badly written",
                                "It has been written by an Anonymous author",
                                e,
                                "Please contact {} at {} to resolve this issue".format("Adrien PARIS", "a.paris.cs@gmail.com")]
            else:
                errorMessage = ["This trial has failed because it was badly written",
                                e,
                                "Please contact {} at {} to resolve this issue".format(self.author, self.email)]
            self.passed, self.errors = True, errorMessage
            return
        if len(value) == 2:
            if not type(value[0]) == type(True):
                print("first return value should be a bool")
                return
            if not isinstance(value[1], list):
                print("no error list")
                return
            self.passed, self.errors = value[0], value[1]
        else:
            print("no enough return value : " + self.title)
        

