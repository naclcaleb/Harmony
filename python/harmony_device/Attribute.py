class Attribute:

    name = ""
    description = ""
    getter = None
    setter = None

    def __init__(self):
        pass
    def summary(self):
        print("Attribute '{}':\n\n{}'".format(self.name, self.description))
        print()
        print("Has getter: {}".format("Yes" if (self.getter != None) else "No"))
        print("Has setter: {}".format("Yes" if (self.setter != None) else "No"))
    def as_json(self):
        return {
            "name": self.name,
            "description": self.description
        }
