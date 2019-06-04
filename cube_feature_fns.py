"""
Shadrach Wilson
shadew@uw.edu

A set of functions representing various features of
a rubik's cube. Meant to simplify the state space of the cube
by implementing feature-based reenforcement learning.

Each function is of the form: F(s, a), where
s is a state and a is the action. These features are typically binary.
"""
from cube import *

def f0(s, a):
    """Default function always returns 1.
    No idea if I'm supposed to do this but it seems like it.
    """
    return 1

def f1(s, a):
    """Count number of reds on FRONT"""
    res = 0
    for c in s.front:
        if c.FB_color == "R":
            res += 1
    return res

def f2(s, a):
    """Count number of whites on UP"""
    res = 0
    for c in s.up:
        if c.UD_color == "W":
            res += 1
    return res

def f3(s, a):
    """Count number of yellows on down"""
    res = 0
    for c in s.down:
        if c.UD_color == "Y":
            res += 1
    return res

def f4(s, a):
    """Count number of oranges on BACK"""
    res = 0
    for c in s.back:
        if c.FB_color == "O":
            res += 1
    return res

def f5(s, a):
    """Count number of greens on LEFT"""
    res = 0
    for c in s.left:
        if c.LR_color == "G":
            res += 1
    return res

def f6(s, a):
    """Count number of blues on RIGHT"""
    res = 0
    for c in s.right:
        if c.LR_color == "B":
            res += 1
    return res

# Following 6 functions return answ for if action is taken for first 6
def f7(s, a):
    if a.name == "Exit":
        return s.n * s.n
    sp = a.state_transf(s)
    return f1(sp, a)

def f8(s, a):
    if a.name == "Exit":
        return s.n * s.n
    sp = a.state_transf(s)
    return f2(sp, a)

def f9(s, a):
    if a.name == "Exit":
        return s.n * s.n
    sp = a.state_transf(s)
    return f3(sp, a)

def f10(s, a):
    if a.name == "Exit":
        return s.n * s.n
    sp = a.state_transf(s)
    return f4(sp, a)

def f11(s, a):
    if a.name == "Exit":
        return s.n * s.n
    sp = a.state_transf(s)
    return f5(sp, a)

def f12(s, a):
    if a.name == "Exit":
        return s.n * s.n
    sp = a.state_transf(s)
    return f6(sp, a)

def f13(s, a):
    """Next action leads to goal state"""
    if a.name == "Exit":
        return 1
    sp = a.state_transf(s)
    if goal_test(sp):
        return 1
    else:
        return 0

def f14(s, a):
    """First layer solved. Considering red as base"""
    # red must be solved
    if f1(s, a) != s.n * s.n:
        return 0
    # check cubes on FRONT's plane are in right place
    min_coord = min(s.coordinate_range)
    for cubie in s.back:
        if cubie.z == min_coord and cubie.FB_color != "O":
            return 0
    for cubie in s.up:
        if cubie.z == min_coord and cubie.UD_color != "W":
            return 0
    for cubie in s.down:
        if cubie.z == min_coord and cubie.UD_color != "Y":
            return 0
    for cubie in s.left:
        if cubie.z == min_coord and cubie.LR_color != "G":
            return 0
    for cubie in s.right:
        if cubie.z == min_coord and cubie.LR_color != "B":
            return 0
    return 1



FEATURES = [
    f0, f1, f2, f3, f4, f5, f6,
    f7, f8, f9, f10, f11, f12, f13, f14
]