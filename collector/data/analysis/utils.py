def cut_left(s, c):
    return s[s.find(c) + len(c):]

def cut_right(s, c):
    return s[:s.find(c)]