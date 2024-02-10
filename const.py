ftable = str.maketrans('[,]', 'fjg')
btable = str.maketrans('fjg', '[,]')

def encode(txt):
    return txt.translate(ftable)

def decode(txt):
    return txt.translate(btable)