from sympy import Matrix, lambdify, cos, sin, symbols

f, ox, oy, a, b, g, x, y, z, s, beta = symbols('f ox oy a b g x y z s beta')

K = Matrix([
    [f,     s * f,      ox],
    [0,     beta * f,   oy],
    [0,     0,          1]])

R = Matrix([
    [   cos(a) * cos(b),        cos(a) * sin(b) * sin(g) - sin(a) * cos(g),     cos(a) * sin(b) * cos(g) + sin(a) * sin(g) ],
    [   sin(a) * cos(b),        sin(a) * sin(b) * sin(g) + cos(a) * cos(g),     sin(a) * sin(b) * cos(g) - cos(a) * sin(g) ],
    [   -1 * sin(b),            cos(b) * sin(g),                                cos(b) * cos(g)                            ]])

semiP = Matrix([
    [1, 0,  0,  -1 * x],
    [0, 1,  0,  -1 * y],
    [0, 0,  1,  -1 * z]])

P = K * R * semiP

PM = lambdify((f, ox, oy, a, b, g, x, y, z, s, beta), P, 'numpy')
    


def projmatrix(F, Ox, Oy, Ax, Ay, Az, X, Y, Z, Skewness=0, Beta=1):
    return PM(F, Ox, Oy, Az, Ay, Ax, X, Y, Z, Skewness, Beta)

