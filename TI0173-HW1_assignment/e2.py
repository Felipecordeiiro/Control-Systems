import sympy as sym
from sympy.abc import s, t

# Basta usarmos a função laplace_transform da lib sympy que ela pode computar
# a TF da função, alternativamente podemos usar também o próprio numpy
Fs = 1/(s+3)**2
ft = sym.inverse_laplace_transform(Fs, t, s)

print(ft)