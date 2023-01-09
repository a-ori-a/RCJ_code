def has_green(img):
    data = img[230]
    data = [ x for x,y in enumerate(data) if 60 < y[0] < 78]
    return data