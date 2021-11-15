# Recurso-Disassembler

Disassmbler , Emulator written in python language to disassemble the Recurso compiled bytecode.

1. Disassmbles the bytecode to Recurso instructions
2. Emulates the execution of the Recurso bytecode

This was written completely based on given [Recurso Executable](chall_files/Recurso) in the CTF. <br>
By analyszing the decompiled code of given executable and understanding it -> written this disassmbler, emulator to solve the challenge.
<br>
<br>

## [Recurso](https://github.com/Kasimir123/Recurso)

Recurso is a stack based interpreted functional programming language given in K3RN3LCTF.<br>
The language was created by [Abraxus](https://github.com/Kasimir123)

Recurso Compiler & Instruction set & More about it : https://github.com/Kasimir123/Recurso
<br>
<br>

## CTF Challenges

There are two challanges given in the CTF. based on this Recurso VM

1. Recurso (file : [leFlag.recc](chall_files/leFlag.recc))
2. Rasm (file : [rasm.recc](chall_files/rasm.recc))

Both are files compiled by [Recurso Executable](chall_files/Recurso) which is emulator, compiler.<br>
We can run recc bytecode file with the given Recuso file.

#### Goal is

challenge files (.recc - Recurso compiled) contain the flag checking logic.<br>
By getting functionality of them , Reversing the logic -> getting flag.

### More about the Challanges :

- Write-ups are there in my blog : https://d1r3wolf.blogspot.com/

1. [Recurso]()
2. [Rasm]()
