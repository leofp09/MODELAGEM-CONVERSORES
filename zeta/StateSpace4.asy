Version 4
SymbolType CELL
LINE Normal -60 -4 -64 -4
LINE Normal -56 0 -60 -4
LINE Normal -60 4 -56 0
LINE Normal -64 4 -60 4
RECTANGLE Normal 48 32 -64 -32
TEXT -8 -14 Center 2 x'=Ax+Bu
TEXT -7 14 Center 2 y=Cx+Du
WINDOW 38 -64 -39 Left 2
SYMATTR SpiceModel 4
SYMATTR Prefix x
SYMATTR ModelFile statespace.sub
SYMATTR Description 4th order SISO state-space model.
SYMATTR Value A11={A11} A12={A12} A13={A13} A14={A14} B11={B11}
SYMATTR Value2 A21={A21} A22={A22} A23={A23} A24={A24} B21={B21}
SYMATTR SpiceLine A31={A31} A32={A32} A33={A33} A34={A34} B31={B31} A41={A41} A42={A42} A43={A43} A44={A44} B41={B41}
SYMATTR SpiceLine2 C11={C11} C12={C12} C13={C13} C14={C14} D11={D11} ic1={IC1} ic2={IC2} ic3={IC3} ic4={IC4}
PIN -64 0 NONE 8
PINATTR PinName in
PINATTR SpiceOrder 1
PIN 48 0 NONE 8
PINATTR PinName out
PINATTR SpiceOrder 2