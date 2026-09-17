# 4ordem.py
#
# Modelo medio e modelo CA em espaco de estados para um conversor de 4a ordem.
#
# Este arquivo esta escrito no estilo de script simples:
#   1. Altere os parametros do circuito na secao PARAMETROS.
#   2. Confira as equacoes da 1a e 2a etapa.
#   3. Rode o script.
#   4. Copie as matrizes ou os .param gerados para o LTspice.
#
# Exemplo implementado: SEPIC ideal em CCM.
#
# Estados adotados:
#   x1 = iL1
#   x2 = vC1
#   x3 = iL2
#   x4 = vC2 = Vout
#
# Entrada:
#   u = Vin
#
# Saida:
#   y = vC2 = Vout
#
# Forma media:
#   x' = A*x + B*u
#   y  = C*x + E*u
#
# Modelo CA padrao:
#   x_til' = Ap*x_til + Bp*d_til
#   y_til  = Cp*x_til + Ep*d_til
#
# Observacao:
#   Para outro conversor de 4a ordem, mantenha a parte de matrizes medias,
#   regime permanente e modelo CA. Troque apenas as equacoes/matrizes A1, B1,
#   C1, E1, A2, B2, C2 e E2.

import numpy as np

# ============================================================
# PARAMETROS DO CIRCUITO
# ============================================================

L1 = 150e-6      # Indutancia L1 [H]
L2 = 150e-6        # Indutancia L2 [H]
C1 = 22e-6       # Capacitancia C1 [F]
C2 = 100e-6       # Capacitancia C2 [F]
R = 5            # Carga [ohm]
Vin = 12        # Tensao de entrada [V]
D = 0.294          # Razao ciclica nominal

# ============================================================
# 1a ETAPA: CHAVE LIGADA
# ============================================================
#
# Para o SEPIC ideal em CCM, com a convencao acima:
#
#   dx1/dt = Vin/L1
#   dx2/dt = -x3/C1
#   dx3/dt = x2/L2
#   dx4/dt = -x4/(R*C2)

A1 = np.array([
    [0, 0, 0, 0],           #somente L1
    [0, 0, -1/C1, 0],       #somente C1
    [0, 1/L2, 0, -1/L2],    #somente L2
    [0, 0, 1/C2, -1/(R*C2)] #somente C2 normalmente = vo
], dtype=float)

B1 = np.array([
    [1/L1],  
    [0],
    [1/L2],
    [0]
], dtype=float)

C1_mat = np.array([
    [0, 0, 0, 1]
], dtype=float)

E1 = np.array([
    [0]
], dtype=float)

# ============================================================
# 2a ETAPA: CHAVE DESLIGADA
# ============================================================
#
# Para o SEPIC ideal em CCM, com a convencao acima:
#
#   dx1/dt = (Vin - x2 - x4)/L1
#   dx2/dt = x1/C1
#   dx3/dt = -x4/L2
#   dx4/dt = (x1 + x3)/C2 - x4/(R*C2)

A2 = np.array([
    [0, -1/L1, 0, 0],
    [1/C1, 0, 0, 0],
    [0, 0, 0, -1/L2],
    [0, 0, 1/C2, -1/(R*C2)]
], dtype=float)

B2 = np.array([
    [0],
    [0],
    [0],
    [0]
], dtype=float)

C2_mat = np.array([
    [0, 0, 0, 1]
], dtype=float)

E2 = np.array([
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
#
# Aqui usamos C1_mat e C2_mat para nao confundir com o capacitor C1.

A = D*A1 + (1-D)*A2
B = D*B1 + (1-D)*B2
C = D*C1_mat + (1-D)*C2_mat
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
Ep = (C1_mat - C2_mat) @ X + (E1 - E2) @ U

# ============================================================
# IMPRESSAO DOS RESULTADOS
# ============================================================

np.set_printoptions(precision=6, suppress=False)

print('PARAMETROS')
print('L1  =', L1)
print('L2  =', L2)
print('C1  =', C1)
print('C2  =', C2)
print('R   =', R)
print('Vin =', Vin)
print('D   =', D)
print()

print('1a ETAPA')
print('A1 =\n', A1)
print('B1 =\n', B1)
print('C1 =\n', C1_mat)
print('E1 =\n', E1)
print()

print('2a ETAPA')
print('A2 =\n', A2)
print('B2 =\n', B2)
print('C2 =\n', C2_mat)
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
print(f'.param A13={A[0,2]:.12g}')
print(f'.param A14={A[0,3]:.12g}')
print()
print(f'.param A21={A[1,0]:.12g}')
print(f'.param A22={A[1,1]:.12g}')
print(f'.param A23={A[1,2]:.12g}')
print(f'.param A24={A[1,3]:.12g}')
print()
print(f'.param A31={A[2,0]:.12g}')
print(f'.param A32={A[2,1]:.12g}')
print(f'.param A33={A[2,2]:.12g}')
print(f'.param A34={A[2,3]:.12g}')
print()
print(f'.param A41={A[3,0]:.12g}')
print(f'.param A42={A[3,1]:.12g}')
print(f'.param A43={A[3,2]:.12g}')
print(f'.param A44={A[3,3]:.12g}')
print()
print(f'.param B11={B[0,0]:.12g}')
print(f'.param B21={B[1,0]:.12g}')
print(f'.param B31={B[2,0]:.12g}')
print(f'.param B41={B[3,0]:.12g}')
print()
print(f'.param C11={C[0,0]:.12g}')
print(f'.param C12={C[0,1]:.12g}')
print(f'.param C13={C[0,2]:.12g}')
print(f'.param C14={C[0,3]:.12g}')
print()
print(f'.param D11={E[0,0]:.12g}')
print()
print(f'.param IC1={X[0,0]:.12g}')
print(f'.param IC2={X[1,0]:.12g}')
print(f'.param IC3={X[2,0]:.12g}')
print(f'.param IC4={X[3,0]:.12g}')