import datetime
import arrow

def get(inter):
    print(arrow.now().shift(months=-inter-1).format("YYYY-MM-DD"))

get(1)