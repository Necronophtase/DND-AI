#do all includes, likely:
from lib import *
import AgentTypes
import AI_Types
import time

#initialize global things:
for i in range(4):
    blueTeam.append(AgentTypes.Bandit([i, 2, 0], AI_Types.Shoot_and_Close(), Team=True))
    redTeam.append(AgentTypes.Bandit([i, -2, 0], AI_Types.Shoot_and_Close(), Team=False))
# - Generate initiative list
LLL=[]
for person in redTeam+blueTeam:
    LLL.append((person, person.Initiative()))
LLL.sort(key=lambda x: x[1])
[initList.append(x[0]) for x in LLL]
print(initList)
#fight until one side dies
while len(redTeam)>0 and len(blueTeam)>0:
    for turn in range(len(initList))[::-1]:
        initList[turn].take_turn()