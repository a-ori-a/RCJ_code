# how to detect intersection
# fot each (top, center, bottom), judge (left, center, right) and then integrate the answer
# switch by the combined chars

def around(standard, num, thresh=10):
    if abs(num - standard) < thresh:
        return 0
    elif num < standard:
        return -1
    elif num > standard:
        return 1
    else:
        print("Something wrong happened in intersection detection")
        return 0

def intersection(points: list):
    result = ""
    for point in points:
        condition = around(320, point, 100)
        if condition == 0:
            result  += "c"
        elif condition == -1:
            result += "l"
        elif condition == 1:
            result += "r"
    