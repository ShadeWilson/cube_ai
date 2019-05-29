"""
Shade Wilson

State representation of a NxN Rubik's cube.

CSE 415
5/28/19
"""


class Cubie:
    """ Represents a single cubie (ie block) in a Rubik's cube.

    Contains coordinates as well as face colors and their orientations.
    The coordinate system is defined as the FRONT of the cube (RED) making up the 
    XY plane with the X axis to the left and right and the Y axis up and down. 
    The Z axis spans behind the front of the cube.

    3-D coordinates stored as (x, y, z)

    - FB_color: front/back color, the color of the XY plane. Could be facing
        front or back, hence the name
    - UD_color: upper/down color, the color of the XZ plane (top/bottom)
    - LR_color: left/right color, the color of the YZ plane
    """
    def __init__(self, x, y, z, FB_color, UD_color, LR_color):
        self.x = x
        self.y = y
        self.z = z
        self.FB_color = FB_color
        self.UD_color = UD_color
        self.LR_color = LR_color

    def __eq__(self, s2):
        return self.x == s2.x and self.y == s2.y and self.z == s2.z and \
            self.FB_color == s2.FB_color and self.UD_color == s2.UD_color and self.LR_color == s2.LR_color

    def __str__(self):
        return "{}, {}, {} [{} {} {}]".format(
            self.FB_color, self.UD_color, self.LR_color,
            self.x, self.y, self.z)

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        new_cubie = Cubie(x=self.x, y=self.y, z=self.z,
            FB_color=self.FB_color, UD_color=self.UD_color, LR_color=self.LR_color)
        
        return new_cubie



class Cube:
    def __init__(self, n=3, c=6):
        """n is the dimention of the NxN Rubiks cube.
        c is the number of colors, defaulting to 6.

        """
        self.n = n
        self.c = c
        self.cube = []
        self.color_dict = {0: "W", 1: "B", 2: "R", 3: "G", 4: "O", 5: "Y"}

        for side in range(6):
            color = side % c
            self.cube.append([x[:] for x in [[self._to_color(color)] * n] * n])

    def _to_color(self, color_num):
        """Converts the color number (0 - 5)
        to a letter representing the color.
        """
        return self.color_dict[color_num]

    def __eq__(self, s2):
        if self.n != s2.n:
            return False
        elif self.c != s2.c:
            return False
        else:
            for side in range(6):
                for i in range(self.n):
                    for j in range(self.n): 
                        if self.cube[side][i][j] != s2.cube[side][i][j]:
                            return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        res = ""

        # build out UPPER (U)
        buf = " " * (5 + self.n)
        upper = 0
        for r in range(self.n):
            res += buf + "U ["
            for cubie in self.cube[upper][r]:
                res += cubie
            res += "]\n"
        res += "\n"

        # 2D cube as "t" is long in horizontal direction
        sides = ["L", "F", "R", "B"]
        for r in range(self.n):
            for s in range(len(sides)):
                side = sides[s]
                res += side + " ["
                for cubie in self.cube[s + 1][r]:
                    res += cubie
                res += "] "
            res += "\n"
        res += "\n"

        # handle DOWN (D)
        down = 5
        for r in range(self.n):
            res += buf + "D ["
            for cubie in self.cube[down][r]:
                res += cubie
            res += "]\n"


        return res

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        new_cube = Cube(n=self.n, c=self.c)
        for side in range(6):
            for i in range(self.n):
                for j in range(self.n): 
                    new_cube.cube[side][i][j] = self.cube[side][i][j]
        
        return new_cube

    def can_move(self, dir):
        '''Tests whether it's legal to move a tile that is next
           to the void in the direction given.'''
        raise True

    def move(self, dir):
        """ It is very unfortunate i have to do it like this

        # rotate front clock-wise
        if dir == "U":
            a = self.cube[1][0]
            self.cube[1][0] = self.cube[2][0]

            b = self.cube[4][0]
            self.cube[4][0] = a

            a = self.cube[3][0]
            self.cube[3][0] = b

            row = self.cube[1][0]
            #self.cube[1][0] = self.cube[2][0]
            """

""" GLOBAL FUNCTIONS """

def goal_test(s):
    goal = Cube(n=s.n, c=s.n)
    return s == goal

def goal_message(s):
    return "You've solved the Rubik's cube!"

""" OPERATORS """

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

directions = ['N','E','W','S']
OPERATORS = [Operator("Move a tile "+str(dir)+" into the void",
                      lambda s,dir1=dir: s.can_move(dir1),
                      lambda s,dir1=dir: s.move(dir1) )
             for dir in directions]


#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>


if __name__ == "__main__":
    c1 = Cube(n=2, c=6)
    print(c1)

    cubie = Cubie(0, 0, 0, "1", "2", "3")
    print(cubie)

    cubie2 = cubie.copy()
    print(cubie2 == cubie)

    cubie2.x = 5
    print(cubie2 == cubie)