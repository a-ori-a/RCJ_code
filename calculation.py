# negative value means left
# and positive value means right

# change this function to have the robot tuned
def turn_strength(top:int, bottom:int):
    center = 320
    next_vector = top - bottom
    position_now = int((bottom - center)/5)
    return max(min(next_vector + position_now,100), -100) # limit -100 ~ 100