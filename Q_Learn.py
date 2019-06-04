"""
Shadrach Wilson
shadew@uw.edu

This code is the implementation of feature-based Q learning
for solving the Rubik's cube. Based off of q learning script from A6,
among other things.
"""

from cube import *
import cube

from cube_feature_fns import *

ACTIONS=None; Q_VALUES=None
Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None
WEIGHTS = None

# model parameters
ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9
LIVING_REWARD = -0.1

def setup(actions, use_exp_fn=False):
    """ Basic setting up of global vars"""
    global ACTIONS, USE_EXPLORATION_FUNCTION
    global Terminal_state, INITIAL_STATE, Q_VALUES
    global WEIGHTS

    actions.append(Operator("Exit", None, None)) 
    ACTIONS = actions

    USE_EXPLORATION_FUNCTION = use_exp_fn
    Terminal_state = State(n=N)
    INITIAL_STATE = CREATE_INITIAL_STATE()
    Q_VALUES = {}

    # initalize feature weights to 1
    WEIGHTS = {}
    for i in range(len(FEATURES)):
        WEIGHTS[i] = 1
    
    if USE_EXPLORATION_FUNCTION:
        # Change this if you implement an exploration function:
        print("You have not implemented an exploration function")

def q_learning_driver(initial_state, iterations):
    """Drives the q learning process from the initial state."""
    pass


def choose_action(s):
    """Given a state, decides on the next action to take.
    It will try to choose the optimal action based on the policy,
    but depending on the value of episilon, there is a chance a random
    action may be taken instead.

    If s is the goal state, always return the "Exit" action.
    Else, return any action BUT "Exit".

    Return: Operator class that is an action
    """
    if is_valid_goal_state(s):
        return "Exit"
    pass

NGOALS=1 # EDIT THIS LATER MAYBE?
def R(s, a, sp):
    """ REWARD FUNCTION:
    - 100 for completing the cube.
    - other rewards??
    """
    # Handle goal state transitions first...
    if goal_test(s):
        if a=="Exit" and sp == Terminal_state: return 100.0
        else: return 0.0
    elif NGOALS==2 and goal_test2(s):
        if a=="Exit" and sp == Terminal_state: return 10.0
        else: return 0.0
    # Handle all other transitions:
    return LIVING_REWARD

def transition_handler(s, a):
    """Given a state s and an action a,
    handle the body of the looping q learning. 

    - Apply a to s -> sp, get R and a new action, ap
    - Record Q value and difference between sample and old estimate
    - Update weights

    Returns sp and ap to be used as the new state and action for the following iteration
    """
    pass

def update_q_values(s, a, r, sp, ap):
    """Call this function whenever s has transitioned to another
    state to update the q values dictionary, Q_VALUES, which is set up as:
    Q_VALUES: {s -> {a: q value} }

    The q value for a s, a pair can be retrieved as such: Q_VALUES[s][a]
    The ideal action for V(s) can be computed as: max(Q_VALUES[s]).

    Formula: Q(s, a) = (1 - ALPHA) * Q(s, a) + ALPHA[R(s, a, sp) + GAMMA * Q(sp, ap)]

    Returns the difference between the sample and the old Q value estimate.
    """
    global Q_VALUES
    pass

def update_weights(s, a, difference):
    """Update the feature weights. 

    Edits WEIGHTS. Returns None.
    """
    global WEIGHTS
    for i in range(len(WEIGHTS)):
        WEIGHTS[i] += ALPHA * difference * FEATURES[i](s, a)


if __name__ == "__main__":
    setup(actions=OPERATORS, use_exp_fn=False)

    for op in ACTIONS:
        print(op.name)