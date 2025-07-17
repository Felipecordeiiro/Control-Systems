import sympy as sym
from sympy.abc import A, a, s, t

f = A*sym.exp(-a*t)
# Basta usarmos a função laplace_transform da lib sympy que ela pode computar
# a TF da função, alternativamente podemos usar também o próprio numpy
F = sym.laplace_transform(f, t, s)

print(F)