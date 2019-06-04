"""
Shadrach Wilson
shadew@uw.edu

A set of functions representing various features of
a rubik's cube. Meant to simplify the state space of the cube
by implementing feature-based reenforcement learning.

Each function is of the form: F(s, a), where
s is a state and a is the action. These features are typically binary.
"""


def f0(s, a):
    """Default function always returns 1.
    No idea if I'm supposed to do this but it seems like it.
    """
    return 1

def f1(s, a):
    pass

def f2(s, a):
    pass

def f3(s, a):
    pass

def f4(s, a):
    pass

def f5(s, a):
    pass

def f6(s, a):
    pass


FEATURES = [f0, f1, f2, f3, f4, f5, f6]