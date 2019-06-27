# Rubik's Cube AI: Feature-Based Reinforcement Learning

### About

The Rubik's cube itself is a generalized implementation of a collection of 3D "cubies", the individual blocks that make up a cube, which allows for simplified operators via rotational matrices.

Reinforcement learning is an AI technique where agents explore a state space, earning rewards for certain behaviors along the way that they try to maximize over time. Q learning is a model-free reinforcement algorithm where the goal of the agent is to determine the optimal policy, or plan, to take them from the starting state to the goal state. Various parameters are used to fine tune exploration vs exploitation of learning, state recall, and sparse rewards among others. Features were used for this particular problem due to the incredible size of the state space a Rubik's cube presents. By incorporating heuristic-like measures for various features of a state, an agent can leverage information it knows about states it's been in before that have similar features. The hard part is in choosing good features that push the agent to the goal.


This was the final project for CSE 415, Introduction to Artificial Intelligence at UW.


### Usage

```shell
python Q_Learn.py [N] [n_transitions] [n_repeats] [level (0 - 3)]

# N: size of the cube. 2 for 2x2, 3 for 3x3, etc
# n_transitions: the number of transitions to run per repeat
# n_repeats: the number of times to redo n transitions. For exploiting learning
# level: 0 - 3, the puzzle level of difficulty where 0 is one turn from a solution and 3 is fully scrambled

# example scrambled 2x2 with solution path and Q values:
python Q_Learn.py 2 1000 5 3

Path:
Initial state:
Front: RRRR
Back:  OOOO
Up:    WYYW
Down:  WYYW
Left:  BGGB
Right: BGGB

Rotate 180'F (207.79536960389967)
Initial state:
Front: RRRR
Back:  OOOO
Up:    YYWW
Down:  YYWW
Left:  GGBB
Right: GGBB

Rotate 180'U (256.07980517585605)
Initial state:
Front: RORO
Back:  OROR
Up:    WWYY
Down:  YYWW
Left:  GGBB
Right: GGBB

Rotate 180'R (314.3972324934149)
Initial state:
Front: RORO
Back:  OROR
Up:    WWWW
Down:  YYYY
Left:  GGBB
Right: BBGG

Rotate 180'U (399.8293013904836)
Initial state:
Front: RRRR
Back:  OOOO
Up:    WWWW
Down:  YYYY
Left:  GGGG
Right: BBBB

Exit (499.9297874737978)
```
