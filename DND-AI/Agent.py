from lib import *
import Condition_Base
import Player
from Action import Action

class Agent:
    def __init__(self, start_pos, AI_class, Team=True, Size=size.Medium):
        global AoO_Trigger
        self.pos = start_pos
        self.AI = AI_class
        self.team = Team  # True if on blue team
        self.Size = Size
        self.STR = 0
        self.DEX = 0
        self.CON = 0
        self.INT = 0
        self.WIS = 0
        self.CHA = 0
        # save stats are the BONUS, add them to the original when making saves
        self.STR_save = 0
        self.DEX_save = 0
        self.CON_save = 0
        self.INT_save = 0
        self.WIS_save = 0
        self.CHA_save = 0
        self.AC = 0
        self.HP_max = 0
        self.HP_now = 0
        self.move = 0
        self.prof = 0
        # as-yet-empty lists:
        self.Actions = [Action({"dash":0}, self.Dash, lambda _:True),
        Action({"dodge":0}, self.Dodge, lambda _:True),
        Action({"disengage":0}, self.Disengage, lambda _:True)
        ]
        self.Bonus_Actions = []
        self.Conditions = set()  # for passive stat changes
        self.SavingThrowTriggers = set()  # for save modifiers; these take (SourceEffect) and return (advantage, disadv, modifier)
        self.TurnStartTriggers = set()  # called by beginTurn
        self.TurnEndTriggers = set()  # called by endTurn
        self.IncomingTargetTriggers = set()  # for the pre-roll effects; these take (attacker, target, Attack) and return (advantage, disadv, modifier)
        self.OutgoingTargetTriggers = set()  # ^
        self.IncomingHitTriggers = set()  # for in-between rolling hit and rolling damage; these take (attacker, target, Attack, HitRoll) and return (Hitroll)
        self.OutgoingHitTriggers = set()  # ^
        self.IncomingDamageTriggers = set()  # for after confirming hit and rolling damage; these take (attacker, target, Attack, damage, dmg.Type) and... return damage?
        self.OutgoingDamageTriggers = set()  # ^
        # action economy flags:
        self.isDead = False
        self.hasDisengaged = False
        self.ActionOpen = True
        self.BonusOpen = True
        self.ReactionOpen = True
        self.MovementSpent = 0
        # Subscription to attacks of opprotunity:
        AoO_Trigger += self.MakeAoO
        # reference to corresponding sprite
        self.sprite = None

    def MakeAoO(self, target, delta):
        if self.ReactionOpen and self.team != target.team:
            response = self.AI.checkAoO(self, target, delta)  # response is None if not making one, or action index otherwise
            if response is None:
                return
            """Debugging really long turns"""
            print(f"{self.sprite.name} attempting AoO against {target.sprite.name}: \n"
            f"\t {self.sprite.name} at {self.pos}; target moved from {target.pos} to {[target.pos[i] + delta[i] for i in range(len(delta))]}"
            f"\n\t\t delta was {delta} ")
            self.Actions[response](target)
            self.ReactionOpen = False

    def Dash(self, _):
        self.MovementSpent-=self.move

    def Dodge(self, _):
        Condition_Base.Dodged(self)

    def Disengage(self, _):
        Condition_Base.Disengaged(self)

    def TakeHit(self, damage, kind):
        """Printing out more and better information; can remove later"""
        print(
            f"The {self.sprite.creature_type} {self.sprite.archetype_type} takes \u001b[38;2;204;120;50m{damage}\u001b[0m damage, going from \u001b[31m{self.HP_now}\u001b[0m down to \u001b[31m{self.HP_now - damage}\u001b[0m")
        self.HP_now -= damage
        if self.HP_now <= 0:
            self.Die()
        return True

    def Die(self):
        global redTeam, blueTeam, AoO_Trigger
        try: 
            self.isDead = True
            blueTeam.remove(self) if self.team else redTeam.remove(self)
            AoO_Trigger -= self.MakeAoO
        except: 
            print("Die was called but I done got got already")

    def Initiative(self):
        return d(20) + self.DEX

    def Step(self, delta):
        if not self.hasDisengaged:
            AoO_Trigger(self, delta)
        self.pos = add(self.pos, delta)
        self.MovementSpent += 1
        Player.refresh()
        Player.clock.tick(20*SimSpeed)

    def beginTurn(self):
        self.ActionOpen = True
        self.BonusOpen = True
        self.ReactionOpen = True
        self.MovementSpent = 0
        for trigger in self.TurnStartTriggers:
            trigger(self)

    def endTurn(self):
        for trigger in self.TurnEndTriggers:
            trigger(self)

    def take_turn(self):
        self.beginTurn()
        planForTurn = self.AI(self)  # call the AI assigned to the Agent, it returns a generator yielding actions for the rest of the turn
        for stepType, stepInd, stepArgs in planForTurn:
            #print(f"sT:{stepType}, sI:{stepInd}, sA:{stepArgs}")
            # each step should be either a move(0), an Action(1), or a Bonus Action(2)
            # print("Steptype: "+str(stepType))
            [[self.Step], self.Actions, self.Bonus_Actions][stepType][stepInd](stepArgs)
            if stepType == 1:
                self.ActionOpen = False
            elif stepType == 2:
                self.BonusOpen = False
            # debug long turns
            #print(f"stepType = {stepType}, ActionOpen set to {self.ActionOpen}")
            if self.isDead:
                return
        self.endTurn()

    def AttackMachinery(self, target, attack):
        Player.attacklaser(self, target, attack)
        r = dist(self, target)
        # check if within max range
        """if ("range" in attack.tags.keys() and attack.tags["range"][1] < r) or ("melee" in attack.tags.keys() and attack.tags["melee"]<r):
            print(f"melee attacks = {attack.tags['melee']} and r = {r}")
            return False"""
        # check adv/disadv
        Advantage = Disadvantage = False
        modifier = attack.tags["hitbonus"]()
        # if attack outside short range
        if "range" in attack.tags.keys() and (r <= 1 or r > attack.tags["range"][0]):
            Disadvantage = True
        for trigger in (target.IncomingTargetTriggers | self.OutgoingTargetTriggers):
            a, b, m = trigger(self, target, attack)
            Advantage = Advantage or a
            Disadvantage = Disadvantage or b
            modifier += m
        if Advantage == Disadvantage:
            HitRoll = d(20)
        elif Advantage:
            HitRoll = adv()
        elif Disadvantage:
            HitRoll = dis()
        HitRoll += modifier
        if HitRoll < target.AC:  # weed out the missed attacks; all lines after this are for "hitting" attacks
            """Printing out more and better information; can remove later"""
            print(f"It misses with a {HitRoll}!")
            return False
        for trigger in (target.IncomingHitTriggers | self.OutgoingHitTriggers):
            HitRoll = trigger(self, target, attack, HitRoll)  # any of these triggers might modify HitRoll
        if HitRoll < target.AC:  # weed out the attacks that were made to miss
            """Printing out more and better information; can remove later"""
            print(f"It misses with a {HitRoll}!")
            return False
        if hasattr(attack.tags["dmgtype"], "__getitem__"):  # if there are multiple damage types listed, we need to work over all of them
            for roll, kind in zip(attack.tags["dmgroll"], attack.tags["dmgtype"]):
                dmgRoll = roll()
                for trigger in (target.IncomingDamageTriggers | self.OutgoingDamageTriggers):
                    dmgRoll = trigger(self, target, attack, dmgRoll, kind)  # any of these triggers might modify damage
                """Printing out more and better information; can remove later"""
                article = "An" if HitRoll in [8, 11, 18] else "A"  # 'an' if number starts with a vowel
                print(f"{article} \u001b[38;2;204;120;50m{HitRoll}\u001b[0m successfuly hits for \u001b[38;2;204;120;50m{dmgRoll}\u001b[0m {attack.tags['dmgtype']} damage!")
                target.TakeHit(dmgRoll, kind)
        else:  # so there's only one damage roll + damage type so we just use them
            dmgRoll = attack.tags["dmgroll"]()
            for trigger in (target.IncomingDamageTriggers | self.OutgoingDamageTriggers):
                dmgRoll = trigger(self, target, attack, dmgRoll, attack.tags["dmgtype"])  # any of these triggers might modify damage
            """Printing out more and better information; can remove later"""
            article = "An" if HitRoll in [8, 11, 18] else "A"  # it was bothering me, okay?
            print(f"{article} \u001b[38;2;204;120;50m{HitRoll}\u001b[0m successfuly hits for \u001b[38;2;204;120;50m{dmgRoll}\u001b[0m {attack.tags['dmgtype']} damage!")
            target.TakeHit(dmgRoll, attack.tags["dmgtype"])
        return True

    def SaveMachinery(self, effect):
        modifier = [self.STR, self.DEX, self.CON, self.INT, self.WIS, self.CHA][effect.tags["stat"]]
        modifier += [self.STR_save, self.DEX_save, self.CON_save, self.INT_save, self.WIS_save, self.CHA_save][
            effect.tags["stat"]]
        Advantage, Disadvantage = False, False
        for trigger in self.SavingThrowTriggers:
            a, b, m = trigger(effect)
            Advantage = Advantage or a
            Disadvantage = Disadvantage or b
            modifier += m
        if Advantage == Disadvantage:
            SaveRoll = d(20)
        elif Advantage:
            SaveRoll = adv()
        elif Disadvantage:
            SaveRoll = dis()
        SaveRoll += modifier
        return SaveRoll >= effect.tags["DC"]

    def assign_Sprite(self, sprite):
        self.sprite = sprite