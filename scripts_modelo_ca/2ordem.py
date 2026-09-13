# 2ordem.py
#
# Modelo medio e modelo CA em espaco de estados para um conversor de 2a ordem.
#
# Como usar:
#   1. Altere os parametros do circuito logo abaixo.
#   2. Rode o script.
#   3. Copie as matrizes ou os .param gerados para o LTspice.
#
# Estados:
#   x1 = iL
#   x2 = vC
#
# Entrada:
#   u = Vin
#
# Forma media:
#   x' = A*x + B*u
#   y  = C*x + E*u
#
# Modelo CA padrao:
#   x_til' = Ap*x_til + Bp*d_til
#   y_til  = Cp*x_til + Ep*d_til

import numpy as np

# ============================================================
# PARAMETROS DO CIRCUITO
# ============================================================

L = 500e-6       # Indutancia [H]
Cap = 100e-6     # Capacitancia [F]
R = 5            # Carga [ohm]
Vin = 48         # Tensao de entrada [V]
D = 0.4          # Razao ciclica nominal

# ============================================================
# 1a ETAPA
# ============================================================
#
# Equacoes diferenciais:
#   dx1/dt = Vin/L
#   dx2/dt = -x2/(R*Cap)

A1 = np.array([
    [0, 0],
    [0, -1/(R*Cap)]
], dtype=float)

B1 = np.array([
    [1/L],
    [0]
], dtype=float)

C1 = np.array([
    [1, 0],
    [0, 1]
], dtype=float)

E1 = np.array([
    [0],
    [0]
], dtype=float)

# ============================================================
# 2a ETAPA
# ============================================================
#
# Equacoes diferenciais:
#   dx1/dt = x2/L
#   dx2/dt = -x1/Cap - x2/(R*Cap)

A2 = np.array([
    [0, 1/L],
    [-1/Cap, -1/(R*Cap)]
], dtype=float)

B2 = np.array([
    [0],
    [0]
], dtype=float)

C2 = np.array([
    [1, 0],
    [0, 1]
], dtype=float)

E2 = np.array([
    [0],
    [0]
], dtype=float)

# ============================================================
# MATRIZES MEDIAS
# ============================================================
#
# A = D*A1 + (1-D)*A2
# B = D*B1 + (1-D)*B2
# C = D*C1 + (1-D)*C2
# E = D*E1 + (1-D)*E2

A = D*A1 + (1-D)*A2
B = D*B1 + (1-D)*B2
C = D*C1 + (1-D)*C2
E = D*E1 + (1-D)*E2

# ============================================================
# VALORES EM REGIME PERMANENTE
# ============================================================
#
# 0 = A*X + B*U
# X = -inv(A)*B*U
#
# Em Python, np.linalg.solve(A, B*U) e melhor numericamente que inv(A)*B*U.

U = np.array([[Vin]], dtype=float)
X = -np.linalg.solve(A, B @ U)
Y = C @ X + E @ U

# ============================================================
# MATRIZES PADRAO DO MODELO CA
# ============================================================
#
# Ap = A
# Bp = (A1-A2)*X + (B1-B2)*U
# Cp = C
# Ep = (C1-C2)*X + (E1-E2)*U

Ap = A
Bp = (A1 - A2) @ X + (B1 - B2) @ U
Cp = C
Ep = (C1 - C2) @ X + (E1 - E2) @ U

# ============================================================
# IMPRESSAO DOS RESULTADOS
# ============================================================

np.set_printoptions(precision=6, suppress=False)

print('PARAMETROS')
print('L   =', L)
print('Cap =', Cap)
print('R   =', R)
print('Vin =', Vin)
print('D   =', D)
print()

print('1a ETAPA')
print('A1 =\n', A1)
print('B1 =\n', B1)
print('C1 =\n', C1)
print('E1 =\n', E1)
print()

print('2a ETAPA')
print('A2 =\n', A2)
print('B2 =\n', B2)
print('C2 =\n', C2)
print('E2 =\n', E2)
print()

print('MATRIZES MEDIAS')
print('A =\n', A)
print('B =\n', B)
print('C =\n', C)
print('E =\n', E)
print()

print('VALORES EM REGIME PERMANENTE')
print('U =\n', U)
print('X =\n', X)
print('Y =\n', Y)
print()

print('MATRIZES PADRAO DO MODELO CA')
print('Ap =\n', Ap)
print('Bp =\n', Bp)
print('Cp =\n', Cp)
print('Ep =\n', Ep)
print()

print('PARAMETROS PARA LTspice')
print(f'.param A11={A[0,0]:.12g}')
print(f'.param A12={A[0,1]:.12g}')
print()
print(f'.param A21={A[1,0]:.12g}')
print(f'.param A22={A[1,1]:.12g}')
print()
print(f'.param B11={B[0,0]:.12g}')
print(f'.param B21={B[1,0]:.12g}')
print()
print(f'.param C11={C[0,0]:.12g}')
print(f'.param C12={C[0,1]:.12g}')
print()
print(f'.param D11={E[0,0]:.12g}')
print()
print(f'.param IC1={X[0,0]:.12g}')
print(f'.param IC2={X[1,0]:.12g}')