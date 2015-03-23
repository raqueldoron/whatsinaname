import random


def generateGeneticList(namesList):
    names = []
    for i in range(50):
        name_to_add = random.choice(namesList)
        if name_to_add in names:
            i-=1
            pass
        names.append(name_to_add)
        
    return names

