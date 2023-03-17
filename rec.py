def recs(x):
    x = x + 1
    if x > 250:
        print("yay")
        return ""
    else:
        recs(x)
    print(x)

recs(-1)