from Agent import *

class Salamander(Agent):
    def __init__(self, start_pos, AI_class, Team=True):
        Agent.__init__(self, start_pos, AI_class, Team, Size=size.Large)
        self.STR=4
        self.DEX=2
        self.CON=2
        self.INT=0
        self.WIS=0
        self.CHA=1
        self.AC=15
        self.HP_max=self.HP_now=90
        self.move=6
        self.prof=3
        #now build the actions:
        self.Actions = [
            Action({"melee":1, "dmg":27, "multi":(1, 3)}, self.multiattack, lambda _: True),
            Action({"melee":1, "dmg":16, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda:d(8, 2)+self.STR, lambda:d(6)), "dmgtype":(dmg.PIERCE_MUND, dmg.FIRE) }, self.spear_melee, lambda _: True),
            Action({"range":(4, 12), "dmg":14, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda:d(6, 2)+self.STR, lambda:d(6)), "dmgtype":(dmg.PIERCE_MUND, dmg.FIRE)}, self.spear_throw, lambda _: True),
            Action({"melee":2, "dmg":18, "hitbonus":(lambda:self.STR+self.prof), "dmgroll":(lambda: d(6, 2)+self.STR, lambda:d(6, 2)), "dmgtype":(dmg.BLUD_MUND, dmg.FIRE), "UniqueTailTag":self}, self.tail, lambda _: True),
            Action({"melee":2, "dmg":26, "multi":(2, 3)}, self.multiattack_range, lambda _: True),
            ] + self.Actions
        Salamander.HeatedBody(self)
    
    def TakeHit(self, damage, kind):
        if kind==dmg.FIRE:
            damage=0
        if kind in (dmg.BLUD_MUND, dmg.PIERCE_MUND, dmg.SLASH_MUND):
            damage = damage//2
        if kind==dmg.COLD:
            damage*=2
        return super().TakeHit(damage, kind)
        
    def multiattack(self, target):
        self.tail(target)
        self.spear_melee(target)

    def multiattack_range(self, target):
        self.tail(target)
        self.spear_throw(target)

    def spear_melee(self, target):
        if self.AttackMachinery(target, self.Actions[1]):
            pass

    def spear_throw(self, target):
        if self.AttackMachinery(target, self.Actions[2]):
            pass
    
    def tail(self, target):
        if self.AttackMachinery(target, self.Actions[3]):
            Salamander.TailGrapple(target, self)

    class TailGrapple(Condition_Base.Restrained):
        def __init__(self, carrier, salam):
            super().__init__(carrier)
            self.lockon = self.STG_autohit(carrier, salam)

        def remove(self):
            super().remove()
            self.lockon.remove()

        class STG_autohit(Condition_Base.Condition):
            def __init__(self, carrier, salam):
                super().__init__(carrier)
                carrier.IncomingTargetTriggers.add(self)
                self.origin = salam

            def __call__(self, attacker, target, attack):
                if "UniqueTailTag" in attack.tags.keys() and attacker==self.origin:
                    return False, False, 10000
                return False, False, 0
        
    class HeatedBody(Condition_Base.Condition):
        def __init__(self, carrier):
            super().__init__(carrier)
            carrier.IncomingHitTriggers.add(self)

        def __call__(self, attacker, target, Attack, HitRoll):
            if "melee" in Attack.tags.keys() and dist(attacker, target)<=1:
                dmgRoll=d(6, 2)
                for trigger in (target.IncomingDamageTriggers | self.carrier.OutgoingDamageTriggers):
                    dmgRoll = trigger(self.carrier, target, Action({}, lambda: None, lambda _: True), dmgRoll, dmg.FIER)  # any of these triggers might modify damage
                attacker.TakeHit(d(6, 2), dmg.FIRE)
            return HitRoll