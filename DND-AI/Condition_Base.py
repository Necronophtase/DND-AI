from lib import *

class Condition: #need to add hash and equ functions for use in sets
    def __init__(self, carrier):
        self.carrier = carrier

    def remove(self):
        self.carrier.Conditions.remove(self)

class Prone(Condition): #prone affects incoming attacks, so it goes in IncomingTargetTriggers
    def __init__(self, carrier):
        super().__init__(carrier)
        carrier.IncomingTargetTriggers.add(self)
        self.twin = Prone.Outgoing(carrier)

    def __call__(self, attacker, target, attack):
        return "melee" in attack.tags.keys(), "range" in attack.tags.keys(), 0
    
    def remove(self):
        self.carrier.IncomingTargetTriggers.remove(self)
        self.twin.remove()

    class Outgoing(Condition): #it also hinders outgoing attacks so this part goes in OutgoingTargetTriggers
        def __init__(self, carrier):
            super().__init__(carrier)
            carrier.OutgoingTargetTriggers.add(self)
            self.OldSpeed = carrier.move
            carrier.move = 1
            
        def __call__(self, attacker, target, attack):
            return False, True, 0

        def remove(self):
            self.carrier.OutgoingTargetTriggers.remove(self)
            self.carrier.move = self.OldSpeed

class Grappled(Condition):
    def __init__(self, carrier):
        super().__init__(carrier)
        self.oldSpeed = carrier.move
        carrier.move=0
        carrier.Conditions.add(self)
    
    def remove(self):
        self.carrier.Conditions.remove(self)
        self.carrier.move=self.oldSpeed

class Restrained(Condition): #the external face of this is the save-effect and root
    def __init__(self, carrier):
        super().__init__(carrier)
        carrier.SavingThrowTriggers.add(self)
        self.incoming = Restrained.Incoming(carrier)
        self.outgoing = Restrained.Outgoing(carrier)
        self.oldSpeed = carrier.move
        carrier.move = 0

    def remove(self, carrier):
        carrier.SavingThrowTriggers.remove(self)
        self.incoming.remove()
        self.outgoing.remove()
        carrier.move = self.oldSpeed

    def __call__(self, effect):
        return False, effect.tags["stat"]==1, 0 #gives disadvantage if the save is DEX

    class Incoming(Condition):
        def __init__(self, carrier):
            super().__init__(carrier)
            carrier.IncomingTargetTriggers.add(self)
        
        def remove(self):
            self.carrier.IncomingTargetTriggers.remove(self)

        def __call__(self, attacker, target, attack):
            return True, False, 0
    
    class Outgoing(Condition):
        def __init__(self, carrier):
            super().__init__(carrier)
            carrier.OutgoingTargetTriggers.add(self)
        
        def remove(self):
            self.carrier.OutgoingTargetTriggers.remove(self)

        def __call__(self, attacker, target, attack):
            return False, True, 0

class Duration_Turnstart(Condition):
    def __init__(self, carrier, ticks):
        super().__init__(carrier)
        self.ticks=ticks
        carrier.TurnStartTriggers.add(self)
    
    def remove(self):
        self.carrier.TurnStartTriggers.remove(self)
    
    def __call__(self):
        ticks-=1
        if ticks==0:
            self.remove()

class Duration_Turnstart_Coupled(Duration_Turnstart):
    def __init__(self, carrier, ticks, StuffToRemove):
        super().__init__(carrier, ticks)
        self.thingz = StuffToRemove

    def remove(self):
        for thing in self.thingz:
            thing.remove()
        super().remove()

class Dodged(Condition):
    def __init__(self, carrier):
        super().__init__(carrier)
        carrier.IncomingTargetTriggers.add(self)
        Duration_Turnstart_Coupled(carrier, 1, [self])

    def __call__(self, a, b, c):
        return False, True, 0

    def remove(self):
        self.carrier.IncomingTargetTriggers.remove(self)

class Disengaged(Duration_Turnstart):
    def __init__(self, carrier):
        super().__init__(carrier, 1)
        carrier.hasDisengaged = True

    def remove(self):
        self.carrier.hasDisengaged = False
        return super().remove()

