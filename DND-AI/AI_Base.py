from Agent import Agent
from lib import *
class AI():
    def __call__(self, pawn):
        return []
    def checkAoO(self, pawn, target, delta):
        enemyDist = dist(pawn, target)
        newEnemyDist = dist_points(pawn.pos, [target.pos[i]+delta[i] for i in range(len(target.pos))]) #TODO
        dmg=0
        dmgInd=None
        for i in range(len(pawn.Actions)):
            if ("melee" in pawn.Actions[i].tags.keys()) and not ("multi" in pawn.Actions[i].tags.keys()) \
             and (enemyDist<=pawn.Actions[i].tags["melee"]) and newEnemyDist>pawn.Actions[i].tags["melee"] \
              and (dmg<pawn.Actions[i].tags["dmg"]):
                dmg=pawn.Actions[i].tags["dmg"]
                dmgInd=i
        return dmgInd

def BasicMelee(pawn, enemyList):
    if not pawn.ActionOpen:
        return None
    dmg=0
    dmgInd=None
    target=None
    for enemy in enemyList:
        r=dist(pawn, enemy)
        #print(f"pawn = {pawn.pos}\n enemy = {enemy.pos}\n r= {r}")
        for i in range(len(pawn.Actions)):
            if  ("melee" in pawn.Actions[i].tags.keys()) and (dmg<pawn.Actions[i].tags["dmg"]) and (pawn.Actions[i].tags["melee"]>=r):
                #print(f"r= {r}, while range is: {pawn.Actions[i].tags['melee']} ")
                dmg=pawn.Actions[i].tags["dmg"]
                dmgInd=i
                target = enemy
    if dmgInd is None:
        return None
    return (1, dmgInd, target)

def ShortRangeShot(pawn, enemyList):
    if not pawn.ActionOpen:
        return None
    for enemy in enemyList:
        r=dist(pawn, enemy)
        dmg=0
        dmgInd=None
        for i in range(len(pawn.Actions)):
            if ("range" in pawn.Actions[i].tags.keys()) and (r <= pawn.Actions[i].tags["range"][0]) and dmg<pawn.Actions[i].tags["dmg"]:
                
                dmg=pawn.Actions[i].tags["dmg"]
                dmgInd=i
        if dmgInd is not None:
            return (1, dmgInd, enemy)

def LongRangeShot(pawn, enemyList):
    if not pawn.ActionOpen:
        return None
    for enemy in enemyList: 
        r=dist(pawn, enemy)
        dmg=0
        dmgInd=None
        for i in range(len(pawn.Actions)):
            if ("range" in pawn.Actions[i].tags.keys()) and (r <= pawn.Actions[i].tags["range"][1]) and dmg<pawn.Actions[i].tags["dmg"]:
                dmg=pawn.Actions[i].tags["dmg"]
                dmgInd=i
        if dmgInd is not None:
            return (1, dmgInd, enemy)

def Approach(pawn, target):
    global redTeam, blueTeam
    if pawn.MovementSpent>=pawn.move or dist(pawn, target)<=1:
        return None
    enemyList = redTeam if pawn.team else blueTeam
    x=target.pos[0]-pawn.pos[0] #TODO
    y=target.pos[1]-pawn.pos[1]
    if abs(x)>=abs(y):
        delta = (x/abs(x), 0, 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            #print(f"returned: {delta} at 0")
            return 0, 0, delta
        # break puts us here e.g. x-direction is blocked so lets try y
        delta = (0, y/abs(y), 0) if y!=0 else (0, 1, 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            #print(f"returned: {delta} at 1")
            return 0, 0, delta
        # break puts us here e.g. both directions are blocked so return None b/c we can't move
        return None
    else: # if we get here then abs(y)>abs(x)
        delta = (0, y/abs(y), 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            #print(f"returned: {delta} at 2")
            return 0, 0, delta
        # break puts us here e.g. y-direction is blocked so lets try x
        delta = (x/abs(x), 0, 0) if x!=0 else (1, 0, 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            #print(f"returned: {delta} at 3")
            return 0, 0, delta
        # break puts us here e.g. both directions are blocked so return None b/c we can't move
        return None

def Flee(pawn, target): 
    global redTeam, blueTeam
    if pawn.MovementSpent>=pawn.move:
        return None
    enemyList = redTeam if pawn.team else blueTeam
    x=pawn.pos[0]-target.pos[0]
    y=pawn.pos[1]-target.pos[1]
    if abs(x)>=abs(y):
        delta = (x/abs(x), 0, 0) if x!=0 else (1, 0, 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            return 0, 0, delta
        # break puts us here e.g. x-direction is blocked so lets try y
        delta = (0, y/abs(y), 0) if y!=0 else (0, 1, 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            return 0, 0, delta
        # break puts us here e.g. both directions are blocked so return None b/c we can't move
        return None
    else: # if we get here then abs(y)>abs(x)
        delta = (0, y/abs(y), 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            return 0, 0, delta
        # break puts us here e.g. y-direction is blocked so lets try x
        delta = (x/abs(x), 0, 0) if x!=0 else (1, 0, 0)
        newpos = add(pawn.pos, delta)
        for enemy in enemyList:
            if enemy.pos == newpos:
                break
        else: # for-else executes if not broken e.g. there's no one there
            return 0, 0, delta
        # break puts us here e.g. both directions are blocked so return None b/c we can't move
        return None

def Enemy_Within(pawn, enemyList, rad):
    for enemy in enemyList:
        if dist(pawn, enemy)<=rad:
            return True
    return False

def Closest_Foe(pawn, enemyList):
    r=100000
    foe=None
    for enemy in enemyList:
        if dist(pawn, enemy)<r:
            r=dist(pawn, enemy)
            foe=enemy
    return foe

def Basic_Multi_Melee(pawn, enemyList):
    for m in pawn.Attacks:
        if "multi" in m.tags.keys() and "melee" in m.tags.keys():
            for i in m.tags["multi"]:
                if dist((n:=Closest_Foe(pawn, enemyList)), pawn)<=pawn.Attacks[i].tags["melee"]:
                    yield (1, i, n)
            break