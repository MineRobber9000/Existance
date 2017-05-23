colors = {"red":(255,0,0),"white":(255,255,255),"black":(0,0,0)}

def defineColor(name,r,g,b):
    colors[name]=(r,g,b)

def getColor(name):
    if name not in colors:
        raise Exception("Undefined color "+name)
    return colors[name]
