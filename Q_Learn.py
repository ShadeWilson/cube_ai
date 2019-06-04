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

import random

try:
  import sys
  arg2 = sys.argv[2]
  N_TRANS = int(arg2)
except:
  N_TRANS = 5

ACTIONS=None; Q_VALUES=None
Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None
WEIGHTS = None
EXIT_ACTION = Operator("Exit", None, None)

# model parameters
ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.2
CUSTOM_EPSILON = False
GAMMA = 0.9
LIVING_REWARD = 0.0

def setup(actions, use_exp_fn=False):
    """ Basic setting up of global vars"""
    global ACTIONS, USE_EXPLORATION_FUNCTION
    global Terminal_state, INITIAL_STATE, Q_VALUES
    global WEIGHTS

    ACTIONS = actions
    USE_EXPLORATION_FUNCTION = use_exp_fn
    Terminal_state = State(n=N)
    INITIAL_STATE = CREATE_INITIAL_STATE()
    Q_VALUES = {}

    # initalize feature weights to 1
    WEIGHTS = [1 for i in range(len(FEATURES))]
    
    if USE_EXPLORATION_FUNCTION:
        # Change this if you implement an exploration function:
        print("You have not implemented an exploration function")

def q_learning_driver(initial_state, n_transitions, end_early=False, verbose=False):
    """Drives the q learning process from the initial state.
    Runs n_transitions number of transitions aka agent turns,
    updating Q values each time.

    """
    s = initial_state
    a = choose_action(s, verbose=verbose)
    for i in range(n_transitions):
        if verbose:
            print("******* Iter #{} *******".format(i))

        s, a = transition_handler(s, a, verbose=verbose)

        if s == Terminal_state:
            if end_early:
                print("done early")
            else:
                s = INITIAL_STATE
                a = choose_action(s, verbose=verbose)
        else:
            #if i % 100 == 99: 
            #    print(".", end='')
            pass

    for i in range(len(WEIGHTS)):
        print("w{}: {}".format(i, WEIGHTS[i]))

    print("Path:")
    path = solution_path()


def choose_action(s, verbose=False):
    """Given a state, decides on the next action to take.
    It will try to choose the optimal action based on the policy,
    but depending on the value of episilon, there is a chance a random
    action may be taken instead.

    If s is the goal state, always return the "Exit" action.
    Else, return any action BUT "Exit".

    Return: Operator class that is an action
    """
    if goal_test(s):
        print("Goal state reached. Returning exit action.")
        return EXIT_ACTION
    
    r = random.uniform(0, 1)
    if r <= EPSILON or not s in Q_VALUES: # if we haven't seen the state, choose rand
        rand_a = random.randint(0, len(ACTIONS) - 1)
        a = ACTIONS[rand_a]
        if verbose:
            print("Selecting random action! {}, ep: {}".format(a.name, EPSILON))

    else:
        a, q = get_max_action_value(s)

        if verbose:
            print("Returning action '{}' ({})".format(a.name, Q_VALUES[s][a]))
    return a



NGOALS=1 # EDIT THIS LATER MAYBE?
def R(s, a, sp):
    """ REWARD FUNCTION:
    - 100 for completing the cube.
    - other rewards??
    """
    # Handle goal state transitions first...
    if goal_test(s):
        if a.name == "Exit" and sp == Terminal_state: 
            print("WIN")
            AssertionError("Bruh howd you win")
            return 1000.0
        else: return 0.0
    elif goal_test2(s):
        return 100.0
    # Handle all other transitions:
    return LIVING_REWARD

def transition_handler(s, a, verbose=False):
    """Given a state s and an action a,
    handle the body of the looping q learning. 

    - Apply a to s -> sp, get R and a new action, ap
    - Record Q value and difference between sample and old estimate
    - Update weights

    Returns sp and ap to be used as the new state and action for the following iteration
    """
    sp = a.state_transf(s)
    ap = choose_action(sp, verbose=verbose)

    if verbose:
        print("New state:")
        print(sp)

    difference = update_q_values(s, a, sp)
    update_weights(s, a, difference, verbose=verbose)

    return sp, ap

def compute_q_value(s, a):
    """Compute Q values,
    specific to feature-based Q learning.
    """
    global Q_VALUES
    res = 0.0
    for i in range(len(WEIGHTS)):
        res += WEIGHTS[i] * FEATURES[i](s, a)

    if not s in Q_VALUES:
        Q_VALUES[s] = {}
    
    Q_VALUES[s][a] = res

    return res

def update_q_values(s, a, sp):
    """Call this function whenever s has transitioned to another
    state to update the q values dictionary, Q_VALUES, which is set up as:
    Q_VALUES: {s -> {a: q value} }

    - s: current state
    - a: action taken to get to sp,
    - sp: next state
    - ap next action to take from sp

    The q value for a s, a pair can be retrieved as such: Q_VALUES[s][a]
    The ideal action for V(s) can be computed as: max(Q_VALUES[s]).

    Formula: Q(s, a) = (1 - ALPHA) * Q(s, a) + ALPHA[R(s, a, sp) + GAMMA * Q(sp, ap)]

    Returns the difference between the sample and the old Q value estimate.
    """
    global Q_VALUES

    if not sp in Q_VALUES:
        Q_VALUES[sp] = {}
        Q_VALUES[sp][a] = 0.0

    # need to be cautious:
    # make sure 1) we've seen state s and 2) we've done action on s... 
    if not s in Q_VALUES:
        Q_VALUES[s] = {}
    if not a in Q_VALUES[s]:
        Q_VALUES[s][a] = 0.0

    ap = choose_action(sp)
    Q_sp_a = compute_q_value(sp, ap)

    sample = R(s, a, sp) + GAMMA * Q_sp_a
    Q_s_a = Q_VALUES[s][a]

    Q_VALUES[s][a] = (1 - ALPHA) * Q_s_a + ALPHA * sample

    return sample - Q_s_a

def update_weights(s, a, difference, verbose):
    """Update the feature weights. 

    Edits WEIGHTS. Returns None.
    """
    global WEIGHTS
    for i in range(len(WEIGHTS)):
        WEIGHTS[i] += ALPHA * difference * FEATURES[i](s, a)

        if verbose:
            print("F{}: {}, W{}: {} (diff: {})".format(i, FEATURES[i](s, a), i, WEIGHTS[i], difference))

def get_max_action_value(s):
    """Returns a tuple with the action, q value
    associated with the max q value for the given state.
    """
    actions = Q_VALUES[s]
    max_action = None
    max_q = -10000
    for a in actions:
        q_value = Q_VALUES[s][a]
        if q_value > max_q:
            max_action = a
            max_q = q_value
    return max_action, max_q


def extract_policy(S, A):
    """Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.
    Ties between actions having the same (s, a) value can be broken arbitrarily.
    Reminder: goal states should map to the Exit action, and no other states
    should map to the Exit action.

    what does this even mean here???
    """
    global Policy
    Policy = {}
    
    return Policy

def solution_path():
    s = INITIAL_STATE
    i = 0
    path = []
    while not goal_test(s) and i < 100:
        a, q = get_max_action_value(s)
        print("A: {} ({})".format(a.name, q))
        path.append(a)
        s = a.state_transf(s)
        i += 1

        if s not in Q_VALUES:
            break
    return path


if __name__ == "__main__":
    setup(actions=OPERATORS, use_exp_fn=False)

    #for op in ACTIONS:
    #    print(op.name)
    print(GOAL_STATE)
    q_learning_driver(INITIAL_STATE, n_transitions=N_TRANS, verbose=True)