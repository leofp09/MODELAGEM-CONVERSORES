# Cola de matrizes por conversor ideal em CCM

Esta cola usa a forma padrao:

```text
x' = A*x + B*u
y  = C*x + E*u
```

Para conversores PWM com duas etapas:

```text
Etapa 1: chave ligada    -> A1, B1, C1, E1
Etapa 2: chave desligada -> A2, B2, C2, E2
```

Modelo medio:

```text
A = D*A1 + (1-D)*A2
B = D*B1 + (1-D)*B2
C = D*C1 + (1-D)*C2
E = D*E1 + (1-D)*E2
```

Modelo CA padrao em torno do ponto de operacao:

```text
0 = A*X + B*U
X = -inv(A)*B*U
Y = C*X + E*U

Ap = A
Bp = (A1-A2)*X + (B1-B2)*U
Cp = C
Ep = (C1-C2)*X + (E1-E2)*U
```

No Python, prefira `X = -np.linalg.solve(A, B @ U)` em vez de `-inv(A)*B*U`.

Aviso importante: as matrizes dependem da convencao de sinais. Se voce inverter o sentido de uma corrente ou a polaridade de um capacitor, a linha/coluna correspondente muda de sinal.

---

## 1. Buck

Estados:

```text
x1 = iL
x2 = vC = Vout
u  = Vin
y  = vC
```

### 1a etapa: chave ligada

```text
dx1/dt = (Vin - x2)/L
dx2/dt = x1/C - x2/(R*C)
```

```text
A1 = [ 0    -1/L
       1/C  -1/(R*C) ]

B1 = [ 1/L
       0   ]

C1 = [0  1]
E1 = [0]
```

### 2a etapa: chave desligada

```text
dx1/dt = -x2/L
dx2/dt = x1/C - x2/(R*C)
```

```text
A2 = [ 0    -1/L
       1/C  -1/(R*C) ]

B2 = [ 0
       0 ]

C2 = [0  1]
E2 = [0]
```

### Media

```text
A = [ 0    -1/L
      1/C  -1/(R*C) ]

B = [ D/L
      0   ]

C = [0  1]
E = [0]
```

---

## 2. Boost

Estados:

```text
x1 = iL
x2 = vC = Vout
u  = Vin
y  = vC
```

### 1a etapa: chave ligada

```text
dx1/dt = Vin/L
dx2/dt = -x2/(R*C)
```

```text
A1 = [ 0  0
       0  -1/(R*C) ]

B1 = [ 1/L
       0   ]

C1 = [0  1]
E1 = [0]
```

### 2a etapa: chave desligada

```text
dx1/dt = (Vin - x2)/L
dx2/dt = x1/C - x2/(R*C)
```

```text
A2 = [ 0    -1/L
       1/C  -1/(R*C) ]

B2 = [ 1/L
       0   ]

C2 = [0  1]
E2 = [0]
```

### Media

```text
A = [ 0          -(1-D)/L
      (1-D)/C   -1/(R*C) ]

B = [ 1/L
      0   ]

C = [0  1]
E = [0]
```

---

## 3. Buck-Boost inversor

Estados:

```text
x1 = iL
x2 = vC = Vout
u  = Vin
y  = vC
```

Nesta convencao, `Vout` em regime permanente fica negativo.

### 1a etapa: chave ligada

```text
dx1/dt = Vin/L
dx2/dt = -x2/(R*C)
```

```text
A1 = [ 0  0
       0  -1/(R*C) ]

B1 = [ 1/L
       0   ]

C1 = [0  1]
E1 = [0]
```

### 2a etapa: chave desligada

```text
dx1/dt = x2/L
dx2/dt = -x1/C - x2/(R*C)
```

```text
A2 = [ 0     1/L
      -1/C  -1/(R*C) ]

B2 = [ 0
       0 ]

C2 = [0  1]
E2 = [0]
```

### Media

```text
A = [ 0          (1-D)/L
     -(1-D)/C   -1/(R*C) ]

B = [ D/L
      0   ]

C = [0  1]
E = [0]
```

---

## 4. SEPIC

Estados:

```text
x1 = iL1, positivo de Vin para o no da chave
x2 = vC1 = V(sw) - V(mid)
x3 = iL2, positivo do terra para o no mid
x4 = vC2 = Vout
u  = Vin
y  = vC2
```

### 1a etapa: chave ligada

```text
dx1/dt = Vin/L1
dx2/dt = -x3/C1
dx3/dt = x2/L2
dx4/dt = -x4/(R*C2)
```

```text
A1 = [ 0  0       0       0
       0  0      -1/C1    0
       0  1/L2    0       0
       0  0       0      -1/(R*C2) ]

B1 = [ 1/L1
       0
       0
       0 ]

C1 = [0  0  0  1]
E1 = [0]
```

### 2a etapa: chave desligada

```text
dx1/dt = (Vin - x2 - x4)/L1
dx2/dt = x1/C1
dx3/dt = -x4/L2
dx4/dt = (x1 + x3)/C2 - x4/(R*C2)
```

```text
A2 = [ 0      -1/L1  0      -1/L1
       1/C1    0     0       0
       0       0     0      -1/L2
       1/C2    0     1/C2   -1/(R*C2) ]

B2 = [ 1/L1
       0
       0
       0 ]

C2 = [0  0  0  1]
E2 = [0]
```

### Media

```text
A = [ 0              -(1-D)/L1   0             -(1-D)/L1
      (1-D)/C1       0          -D/C1          0
      0              D/L2        0             -(1-D)/L2
      (1-D)/C2       0           (1-D)/C2      -1/(R*C2) ]

B = [ 1/L1
      0
      0
      0 ]

C = [0  0  0  1]
E = [0]
```

---

## 5. Cuk inversor

Estados:

```text
x1 = iL1
x2 = vC1, tensao no capacitor de transferencia
x3 = iL2
x4 = vC2, modulo da tensao de saida invertida
u  = Vin
y  = vC2
```

Nesta convencao, `x4` representa o modulo positivo da saida. A tensao fisica do conversor Cuk inversor e `-x4`.

### 1a etapa: chave ligada

```text
dx1/dt = Vin/L1
dx2/dt = -x3/C1
dx3/dt = (x2 - x4)/L2
dx4/dt = x3/C2 - x4/(R*C2)
```

```text
A1 = [ 0  0       0       0
       0  0      -1/C1    0
       0  1/L2    0      -1/L2
       0  0       1/C2   -1/(R*C2) ]

B1 = [ 1/L1
       0
       0
       0 ]

C1 = [0  0  0  1]
E1 = [0]
```

### 2a etapa: chave desligada

```text
dx1/dt = (Vin - x2)/L1
dx2/dt = x1/C1
dx3/dt = -x4/L2
dx4/dt = x3/C2 - x4/(R*C2)
```

```text
A2 = [ 0      -1/L1  0      0
       1/C1    0     0      0
       0       0     0     -1/L2
       0       0     1/C2  -1/(R*C2) ]

B2 = [ 1/L1
       0
       0
       0 ]

C2 = [0  0  0  1]
E2 = [0]
```

### Media

```text
A = [ 0              -(1-D)/L1  0       0
      (1-D)/C1       0         -D/C1    0
      0              D/L2       0      -1/L2
      0              0          1/C2   -1/(R*C2) ]

B = [ 1/L1
      0
      0
      0 ]

C = [0  0  0  1]
E = [0]
```

---

## 6. Zeta

Estados:

```text
x1 = iL1
x2 = vC1, tensao no capacitor de transferencia
x3 = iL2
x4 = vC2 = Vout
u  = Vin
y  = vC2
```

Com esta convencao, `x2` pode aparecer negativo no ponto de operacao, dependendo da polaridade escolhida para o capacitor de transferencia.

### 1a etapa: chave ligada

```text
dx1/dt = Vin/L1
dx2/dt = x3/C1
dx3/dt = (Vin - x2 - x4)/L2
dx4/dt = x3/C2 - x4/(R*C2)
```

```text
A1 = [ 0  0       0       0
       0  0       1/C1    0
       0 -1/L2    0      -1/L2
       0  0       1/C2   -1/(R*C2) ]

B1 = [ 1/L1
       0
       1/L2
       0 ]

C1 = [0  0  0  1]
E1 = [0]
```

### 2a etapa: chave desligada

```text
dx1/dt = x2/L1
dx2/dt = -x1/C1
dx3/dt = -x4/L2
dx4/dt = x3/C2 - x4/(R*C2)
```

```text
A2 = [ 0       1/L1   0      0
      -1/C1    0      0      0
       0       0      0     -1/L2
       0       0      1/C2  -1/(R*C2) ]

B2 = [ 0
       0
       0
       0 ]

C2 = [0  0  0  1]
E2 = [0]
```

### Media

```text
A = [ 0              (1-D)/L1   0       0
     -(1-D)/C1       0          D/C1    0
      0             -D/L2       0      -1/L2
      0              0          1/C2   -1/(R*C2) ]

B = [ D/L1
      0
      D/L2
      0 ]

C = [0  0  0  1]
E = [0]
```

---

## Resumo rapido para colar em Python

O trecho abaixo e igual para todos os conversores; troque apenas `A1`, `B1`, `C1`, `E1`, `A2`, `B2`, `C2`, `E2`.

```python
A = D*A1 + (1-D)*A2
B = D*B1 + (1-D)*B2
C = D*C1 + (1-D)*C2
E = D*E1 + (1-D)*E2

U = np.array([[Vin]], dtype=float)
X = -np.linalg.solve(A, B @ U)
Y = C @ X + E @ U

Ap = A
Bp = (A1 - A2) @ X + (B1 - B2) @ U
Cp = C
Ep = (C1 - C2) @ X + (E1 - E2) @ U
```
