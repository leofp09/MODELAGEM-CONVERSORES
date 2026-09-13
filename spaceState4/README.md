# StateSpace4 para LTspice

Esta pasta contem uma versao independente do bloco de espaco de estados baseada no estilo da pasta `spaceState` original.

Arquivos:

- `statespace.sub`: biblioteca local com os subcircuitos numericos `1`, `2`, `3` e `4`.
- `StateSpace4.asy`: simbolo LTspice apontando inicialmente para o modelo `4`.

Foi testado no LTspice 24.0.12 que nomes de subcircuito puramente numericos (`1`, `2`, `3`, `4`) sao aceitos.

## Como escolher a ordem

Depois de inserir o simbolo no esquematico, basta colocar no parametro `SpiceModel`/`Value` do componente o numero da ordem desejada:

```text
1   para 1a ordem
2   para 2a ordem
3   para 3a ordem
4   para 4a ordem
```

O arquivo `StateSpace4.asy` ja vem com:

```text
SYMATTR SpiceModel 4
```

Portanto, para usar como bloco de 4a ordem, basta inserir o simbolo e declarar os parametros `.param` no esquematico. Para usar a mesma biblioteca com modelos de 1a, 2a ou 3a ordem, altere o `SpiceModel`/`Value` da instancia para `1`, `2` ou `3`.

## Modelo de 4a ordem

O modelo implementado para `SpiceModel 4` e:

```text
x' = A*x + B*u
y  = C*x + D*u
```

com:

```text
A = [A11 A12 A13 A14
     A21 A22 A23 A24
     A31 A32 A33 A34
     A41 A42 A43 A44]

B = [B11 B21 B31 B41]^T
C = [C11 C12 C13 C14]
D = [D11]
```

As condicoes iniciais sao:

```text
ic = [IC1 IC2 IC3 IC4]
```

Internamente, o bloco segue a filosofia original: fontes `G`, capacitores de `1 F` como integradores e resistor de saida de `1 ohm`.

## Exemplo para 4a ordem

Cole as diretivas abaixo no esquematico:

```text
.param A11=0
.param A12=-1200
.param A13=0
.param A14=-1200

.param A21=12765.957
.param A22=0
.param A23=-8510.638
.param A24=0

.param A31=0
.param A32=400
.param A33=0
.param A34=-600

.param A41=12765.957
.param A42=0
.param A43=12765.957
.param A44=-4255.319

.param B11=2000
.param B21=0
.param B31=0
.param B41=0

.param C11=0
.param C12=0
.param C13=0
.param C14=1

.param D11=0

.param IC1=0
.param IC2=0
.param IC3=0
.param IC4=0
```

Evite usar `D` como nome de duty-cycle no mesmo circuito. Prefira `Duty`, porque `D11` representa a transmissao direta do modelo em espaco de estados.

## Estados internos

Este simbolo possui apenas entrada e saida, seguindo o estilo original. Os estados podem ser visualizados pelos nos internos da instancia:

```text
V(u1:1) = x1
V(u1:2) = x2
V(u1:3) = x3
V(u1:4) = x4
```

Se o nome da instancia nao for `U1`, substitua `u1` pelo nome correspondente da instancia no LTspice.

## Exemplo minimo de netlist

```text
V1 in 0 PULSE(0 1 0 1u 1u 1m 2m)
XU1 in out 4 A11={A11} A12={A12} A13={A13} A14={A14} B11={B11} A21={A21} A22={A22} A23={A23} A24={A24} B21={B21} A31={A31} A32={A32} A33={A33} A34={A34} B31={B31} A41={A41} A42={A42} A43={A43} A44={A44} B41={B41} C11={C11} C12={C12} C13={C13} C14={C14} D11={D11} ic1={IC1} ic2={IC2} ic3={IC3} ic4={IC4}
.tran 5m
.lib statespace.sub
.end
```