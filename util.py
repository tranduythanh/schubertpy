def padding_right(lam, value, count):
    return lam + [value]*count


def yd(partition):
    print('Young diagram for partition: ' + str(partition))
    for row in partition:
        print(('[]') * row)