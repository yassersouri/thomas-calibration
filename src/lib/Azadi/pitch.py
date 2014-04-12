import math

def add_tuple(a, b):
    return tuple([i1 + i2 for i1, i2 in zip(a,b)])

def sub_tuple(a, b):
    return tuple([i1 - i2 for i1, i2 in zip(a,b)])

def div_tuple(a, k):
    return tuple([i/k for i in a])

def normalize(a):
    norm = norm2(a)
    return div_tuple(a, norm)

def norm2(a):
    squares = [i*i for i in a]
    norm = math.sqrt(sum(squares))
    return norm

def mul_tuple(a, k):
    return tuple([i * k for i in a])

class pitch(object):
    """
    Conventions:

        - each point is in the 3D coordinate system represented by a tuple (x, y, z)
    """

    CENTERAL_CIRCLE_R = 9.15
    GOAL_AREA_HEIGHT = 5.5
    PENALTY_SPOT_DIS = 11
    PENALTY_AREA_HEIGHT = 16.5
    POST_TO_POST = 7.32
    GOAL_LINE_TO_PENALTY_LINE = 11

    def __init__(self, c1, p0c0, p0g0, p0c3):
        self.c0 = (0, 0, 0)
        self.c1 = c1
        self.p0c0 = p0c0
        self.p0g0 = p0g0
        self.p0c3 = p0c3

        pc0_pg0 = sub_tuple(self.p0g0, self.p0c0)
        x_direction = normalize(pc0_pg0)
        y_direction = normalize(sub_tuple(self.c1, self.c0))

        self.c3 = add_tuple(self.p0c0, self.p0c3)
        self.c2 = add_tuple(self.c1, self.c3)
        
        self.hl0 = div_tuple(self.c1, 2)
        self.hl1 = add_tuple(self.hl0, self.c3)

        self.cs0 = div_tuple(add_tuple(self.hl0, self.hl1), 2)

        self.cs1 = add_tuple(self.cs0, mul_tuple(x_direction, -1 * self.CENTERAL_CIRCLE_R))

        self.cs2 = add_tuple(self.cs0, mul_tuple(x_direction, self.CENTERAL_CIRCLE_R))
        
        pp0_pp1 = mul_tuple(x_direction, self.POST_TO_POST)
        pc0_pc3 = sub_tuple(self.p0c3, self.p0c0)
        pg0_pp0 = div_tuple(sub_tuple(pc0_pc3, add_tuple(mul_tuple(pc0_pg0, 2), pp0_pp1)), 2)

        self.p0p0 = add_tuple(pg0_pp0, self.p0g0)
        self.p0p1 = add_tuple(self.p0p0, pp0_pp1)
        self.p0g3 = add_tuple(self.p0p1, pg0_pp0)

        self.p0c1 = add_tuple(self.p0c0, mul_tuple(y_direction, self.PENALTY_AREA_HEIGHT))
        self.p0c2 = add_tuple(self.p0c3, mul_tuple(y_direction, self.PENALTY_AREA_HEIGHT))

        self.p0g1 = add_tuple(self.p0g0, mul_tuple(y_direction, self.GOAL_AREA_HEIGHT))
        self.p0g2 = add_tuple(self.p0g3, mul_tuple(y_direction, self.GOAL_AREA_HEIGHT))

        self.p0ps = add_tuple(div_tuple(add_tuple(self.p0p0, self.p0p1), 2), mul_tuple(y_direction, self.PENALTY_SPOT_DIS))

        self.p1c1 = add_tuple(self.c1, sub_tuple(self.p0c0, self.c0))
        self.p1g1 = add_tuple(self.c1, sub_tuple(self.p0g0, self.c0))
        self.p1p0 = add_tuple(self.c1, sub_tuple(self.p0p0, self.c0))
        self.p1p1 = add_tuple(self.c1, sub_tuple(self.p0p1, self.c0))
        self.p1g2 = add_tuple(self.c1, sub_tuple(self.p0g3, self.c0))
        self.p1c2 = add_tuple(self.c1, sub_tuple(self.p0c3, self.c0))

        self.p1c0 = add_tuple(self.p1c1, mul_tuple(y_direction, -1 * self.PENALTY_AREA_HEIGHT))
        self.p1c3 = add_tuple(self.p1c2, mul_tuple(y_direction, -1 * self.PENALTY_AREA_HEIGHT))

        self.p1g0 = add_tuple(self.p1g1, mul_tuple(y_direction, -1 * self.GOAL_AREA_HEIGHT))
        self.p1g3 = add_tuple(self.p1g2, mul_tuple(y_direction, -1 * self.GOAL_AREA_HEIGHT))

        self.p1ps = add_tuple(div_tuple(add_tuple(self.p1p0, self.p1p1), 2), mul_tuple(y_direction, -1 * self.PENALTY_SPOT_DIS))