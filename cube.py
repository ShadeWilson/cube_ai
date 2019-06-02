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

    def __lt__(self, s2):
        if self.x < s2.x: return True
        elif self.y < s2.y: return True
        elif self.z < s2.z: return True
        else: return False

    def __le__(self, s2):
        if self.x <= s2.x: return True
        elif self.y <= s2.y: return True
        elif self.z <= s2.z: return True
        else: return False

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
        if dir in ["L", "R"]:  # about X
            if clockwise:
                new.y = -self.z
                new.z = self.y
            else:
                new.y = self.z
                new.z = -self.y
            new.UD_color = self.FB_color
            new.FB_color = self.UD_color
        elif dir in ["U", "D"]:  # about Y
            if clockwise:
                new.x = self.z
                new.z = -self.x
            else:
                new.x = -self.z
                new.z = self.x
            new.FB_color = self.LR_color
            new.LR_color = self.FB_color
        elif dir in ["F", "B"]:  # about Z
            if clockwise:
                new.x = self.y
                new.y = -self.x
            else:
                new.x = -self.y
                new.y = self.x
            new.UD_color = self.LR_color
            new.LR_color = self.UD_color
        else:
            raise ValueError("{} is not a valid rotation axis.".format(rotation_axis))

        return new

    def is_outside_cube(self, coordinate_range):
        """ Given a range of Cube coordinates, 
        returns true iff the cubie itself is on the outside of the cube.
        Ie, the cubie would be visible (and thus matters)

        """
        max_coord = max(coordinate_range)
        min_coord = min(coordinate_range)
        edges = [min_coord, max_coord]

        return self.x in edges or self.y in edges or self.z in edges





class Cube:
    def __init__(self, n=2):
        """n is the dimention of the NxN Rubiks cube.
        c is the number of colors, defaulting to 6.

        """
        self.n = n
        self.cube = []
        self.front = []
        self.back = []
        self.up = []
        self.down = []
        self.left = []
        self.right = []
        #self.color_dict = {0: "W", 1: "B", 2: "R", 3: "G", 4: "O", 5: "Y"}

        # max coordinate is the farthest distance from the origin
        # a cubie may be found. Coordinates are 1 unit away from each other,
        # down to the min coordinate (-max coordinate). SYMMETRICAL
        self.max_coord = 0.0
        for i in range(n):
            self.max_coord += i
        self.max_coord = self.max_coord / n

        self.coordinate_range = [-self.max_coord]
        for i in range(n - 1):
            self.coordinate_range.append(-self.max_coord + 1 + i)

        # populate Cube w/ cubies and faces with relevent cubies
        for x in self.coordinate_range:
            for y in self.coordinate_range:
                for z in self.coordinate_range:
                    FB_color, UD_color, LR_color = self._side_color(x, y, z)
                    cubie = Cubie(x, y, z, FB_color, UD_color, LR_color)
                    if cubie.is_outside_cube(self.coordinate_range):
                        self._add_to_face(cubie)
                        self.cube.append(cubie)

    def _side_color(self, x, y, z):
        """Given an x, y, and z coord,
        return a tuple of 
        (FB_color, UD_color, LR_color). 
        One or more may be None if the cubie is not
        visible from that direction."""
        FB_color = None
        UD_color = None
        LR_color = None

        max_coord = max(self.coordinate_range)
        min_coord = min(self.coordinate_range)

        if x == min_coord:
            LR_color = "B"
        elif x == max_coord:
            LR_color = "G"

        if y == min_coord:
            UD_color = "Y"
        elif y == max_coord:
            UD_color = "W"

        if z == min_coord:
            FB_color = "R"
        elif z == max_coord:
            FB_color = "O"

        return (FB_color, UD_color, LR_color) 

    def _add_to_face(self, cubie):
        """Add cubie to the proper faces."""
        max_coord = max(self.coordinate_range)
        min_coord = min(self.coordinate_range)

        if cubie.x == min_coord:
            self.left.append(cubie)
        elif cubie.x == max_coord:
            self.right.append(cubie)

        if cubie.y == min_coord:
            self.down.append(cubie)
        elif cubie.y == max_coord:
            self.up.append(cubie)

        if cubie.z == min_coord:
            self.front.append(cubie)
        elif cubie.z == max_coord:
            self.back.append(cubie)

    def _to_color(self, color_num):
        """Converts the color number (0 - 5)
        to a letter representing the color.
        """
        return self.color_dict[color_num]

    def __eq__(self, s2):
        if self.n != s2.n:
            return False

        # this changes the internal representation but
        # the list order doesn't matter for us
        self.cube.sort()
        s2.cube.sort()

        for i in range(len(self.cube)):
            if self.cube[i] != s2.cube[i]:
                return False
        return True

    def __str__(self):
        res = "Front:\n"

        for c in self.front:
            res += str(c) + "\n"
        res +="Back:\n"
        for c in self.back:
            res += str(c) + "\n"
        res +="Up:\n"
        for c in self.up:
            res += str(c) + "\n"
        res +="Down:\n"
        for c in self.down:
            res += str(c) + "\n"
        res +="Left:\n"
        for c in self.left:
            res += str(c) + "\n"
        res +="Right:\n"
        for c in self.right:
            res += str(c) + "\n"

        return res

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        new = Cube(self.n)

        new.cube = []
        new.front = []
        new.back = []
        new.up = []
        new.down = []
        new.left = []
        new.right = []

        for cubie in self.cube:
            new._add_to_face(cubie)
            new.cube.append(cubie)

        return new

    def can_move(self, dir):
        '''Tests whether it's legal to move a tile that is next
           to the void in the direction given.'''
        return True

    def move(self, dir, clockwise=True):
        if dir == "F":
            for cubie in self.front:
                new = cubie.rotate(dir=dir, clockwise=clockwise)
                print("{} -> {}".format(cubie, new))

""" GLOBAL FUNCTIONS """

def goal_test(s):
    goal = Cube(n=s.n)
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
    """
    c1 = Cube(n=3)
    print("Max coord: {}\nRange: {}".format(c1.max_coord, c1.coordinate_range))
    print(c1)

    c2 = c1.copy()
    print(c1 == c2)
    c2.cube[0] = Cubie(-1, 0, -1, "R", "W", "B")
    print("After change: {}".format(c1 == c2))

    cubie = Cubie(-1, -1, -1, "R", "W", "B")
    print(cubie)

    cubie2 = cubie.rotate(dir="U")
    print(cubie2 == cubie)
    print(cubie2)

    cubie3 = cubie2.rotate(dir="U", clockwise=False)
    print(cubie3 == cubie)
    print(cubie3)
    """
    cube = Cube(n=2)
    print(cube)

    print("***************")
    cube.move(dir="F")

