class Action:
    def __init__(self, Tags, Call, Check):
        self.tags  = Tags
        self.call  = Call
        self.check = Check #these are attributes instead of methods so I can reassign them at the object level
    def __call__(self, target):
        self.call(target)