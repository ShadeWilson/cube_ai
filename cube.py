"""
Shade Wilson

State representation of a NxN Rubik's cube.

CSE 415
5/28/19
"""


class Cube:
    def __init__(self, n=3, c=6):
        """n is the dimention of the NxN Rubiks cube.
        c is the number of colors, defaulting to 6.

        """
        self.n = n
        self.c = c
        self.cube = []
        for side in range(6):
            color = side % c
            self.cube.append([x[:] for x in [[color] * n] * n])
    

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
        buf = " " * (2 + self.n * 3)
        upper = 0
        for r in range(self.n):
            res += buf + "U" + str(self.cube[upper][r])
            res += "\n"
        res += "\n"

        # 2D cube as "t" is long in horizontal direction
        sides = ["L", "F", "R", "B"]
        for r in range(self.n):
            for s in range(len(sides)):
                side = sides[s]
                res += side + str(self.cube[s + 1][r]) + " "
            res += "\n"
        res += "\n"

        # handle DOWN (D)
        down = 5
        for r in range(self.n):
            res += buf + "D" + str(self.cube[down][r])
            res += "\n"


        return res

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        pass

    def can_move(self, dir):
        '''Tests whether it's legal to move a tile that is next
           to the void in the direction given.'''
        raise True

    def move(self, dir):
        pass


if __name__ == "__main__":
    c1 = Cube(n=2, c=6)
    print(c1)