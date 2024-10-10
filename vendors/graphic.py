def getH(r,g,b):
    r = r/255
    g = g/255
    b = b/255
    maximum = max([r,g,b])
    minimum = min([r,g,b])
    cost = maximum - minimum
    hue = 0
    if maximum == r:
        hue = 60*(((g-b)/cost) % 6)
    elif maximum == g:
        hue = 60*(((b-r)/cost) + 2)
    elif maximum == b:
        hue = 60*(((r-g)/cost) + 4)
    return hue


def getS(r,g,b):
    r = r/255
    g = g/255
    b = b/255
    maximum = max([r,g,b])
    minimum = min([r,g,b])
    value = maximum
    cost = maximum - minimum
    saturation = 0
    if value != 0:
        saturation = cost/value
    return saturation


def getV(r,g,b):
    r = r/255
    g = g/255
    b = b/255
    maximum = max([r,g,b])
    value = maximum
    return value