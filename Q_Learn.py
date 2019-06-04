"""
Shadrach Wilson
shadew@uw.edu

This code is the implementation of feature-based Q learning
for solving the Rubik's cube. Based off of q learning script from A6,
among other things.
"""

from cube import *
import cube

ACTIONS=None; Q_VALUES=None
is_valid_goal_state=None; Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None

def setup(actions, goal_test, use_exp_fn=False):
    '''This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair.'''
    global ACTIONS, is_valid_goal_state
    global USE_EXPLORATION_FUNCTION, Terminal_state, INITIAL_STATE
    INITIAL_STATE = CREATE_INITIAL_STATE()
    ACTIONS = actions
    Q_VALUES = {}
    is_valid_goal_state = goal_test
    Terminal_state = State(n=N)
    USE_EXPLORATION_FUNCTION = use_exp_fn
    if USE_EXPLORATION_FUNCTION:
        # Change this if you implement an exploration function:
        print("You have not implemented an exploration function")


if __name__ == "__main__":
    setup(actions=OPERATORS, goal_test=GOAL_TEST)