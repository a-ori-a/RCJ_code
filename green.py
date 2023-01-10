def has_green(img):
    data = img[230]
    # for i in data:
    #     print(i)
    # exit()
    data = [ x for x,y in enumerate(data) if 60 < y[0] < 90 and 150 < y[1] and 20 < y[2]]
    return data
