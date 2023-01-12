# Clause structure
class Clause:
    def __init__(self, *args):
        if len(args) > 0:
            literals = args[0]
            id = args[1]
            self.literals = literals
            if len(literals) > 1:
                self.sentinels = [literals[0], literals[1]]
            else:
                self.sentinels = [literals[0]]
            self.value = None
            self.id = id
        else:
            self.literals = None
            self.sentinels = None
            self.value = None
            self.id = None

# Literal structure
class Literal:
    def __init__(self, key):
        self.key = str(key)
        self.value = None
        self.level = None
        self.decided = None
        self.propagated = None


