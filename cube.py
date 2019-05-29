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

    def rotate(self, dir, clockwise=True):
        """Most complicated method here. Based in the linear
        algebra of 3D rotational matrices. I am forcing rotations
        to 90 degrees, which simplifies the matrices a lot, allowing
        me to "collapse" them and instead of performing matrix algebra,
        I can simply swap x, y, and/or z value as needed.
        
        - dir: direction, in cube lingo. Accepted directions are
        B, F, L, R, U, and D. Each stand for rotating a particular face
        90 degrees. This translates to rotation along a particular axis 
        depending on the direction. Ex: F (front) represents a rotation of
        the XY plane about the Z axis. NOTE: this assumes that the user knows
        what they are doing when rotating and does not rotate a cube on the back face
        when the front is rotated...

        - clockwise: True for a clockwise rotation, False for a counterclockwise rotation

        Returns a new cubie rotated from this.
        """
        new = self.copy()
        if dir in ["B", "F"]:  # about Z
            if clockwise:
                new.y = -self.z
                new.z = self.y
            else:
                new.y = self.z
                new.z = -self.y
            new.UD_color = self.LR_color
            new.LR_color = self.UD_color
        elif dir in ["L", "R"]:  # about X
            if clockwise:
                new.x = self.z
                new.z = -self.x
            else:
                new.x = -self.z
                new.z = self.x
            new.FB_color = self.UD_color
            new.UD_color = self.FB_color
        elif dir in ["U", "D"]:  # about Y
            if clockwise:
                new.x = self.y
                new.y = -self.x
            else:
                new.x = -self.y
                new.y = self.x
            new.FB_color = self.LR_color
            new.LR_color = self.FB_color
        else:
            raise ValueError("{} is not a valid rotation axis.".format(rotation_axis))

        return new




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

    cubie = Cubie(-1, -1, -1, "R", "W", "B")
    print(cubie)

    cubie2 = cubie.rotate(dir="U")
    print(cubie2 == cubie)
    print(cubie2)

    cubie3 = cubie2.rotate(dir="U", clockwise=False)
    print(cubie3 == cubie)
    print(cubie3)