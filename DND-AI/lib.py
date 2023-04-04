import random
from enum import Enum, IntEnum
import math

def d(n, count=1):
    return sum([random.randint(1,n) for i in range(count)])
def dist(a, b):
    Atiles= tileSize(a.Size)
    Btiles= tileSize(b.Size)
    dist=[0, 0]
    # if statement for when they aren't already overlapped. if it gets skipped, then it was 0 anyway!
    if (a.pos[0] > b.pos[0]+Btiles) or (a.pos[0]+Atiles < b.pos[0]): 
       dist[0] = max(a.pos[0] - b.pos[0]+Btiles, -a.pos[0]+Atiles + b.pos[0])
    if (a.pos[1] > b.pos[1]+Btiles) or (a.pos[1]+Atiles < b.pos[1]): 
       dist[1] = max(a.pos[1] - b.pos[1]+Btiles, -a.pos[1]+Atiles + b.pos[1])
    return dist[0]+dist[1]
    #return dist_points(a.pos, b.pos)
def dist_points(a, b):
    return math.floor(math.sqrt(sum([(a[i]-b[i])**2 for i in range(len(a))])))
def dis():
    return min([d(20), d(20)])
def adv():
    return max([d(20), d(20)])
def add(a, b):
    return [a[i]+b[i] for i in range(min(len(a), len(b)))]
def tileSize(big):
    return max(int(big)-1, 1)

class Event:
    def __init__(self):
        self.__eventhandlers = []
 
    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self
 
    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self
 
    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)

AoO_Trigger = Event()
redTeam=[]
blueTeam=[]
initList=[]
SimSpeed = 0.1
class dmg(Enum):
    BLUD_MUND=0
    BLUD_MAG=1
    SLASH_MUND=2
    SLASH_MAG=3
    PIERCE_MUND=4
    PIERCE_MAG=5
    FIRE=6
    COLD=7
    POISON=8
    ACID=9
    THUNDER=10
    LIGHTNING=11
    RADIANT=12
    NECROTIC=13
    PSYCHIC=14
    FORCE=15

class size(IntEnum):
    Tiny=0
    Small=1
    Medium=2
    Large=3
    Huge=4
    Gargantuan=5