# Shellcode
A series of **machine code** that hacker can use to control the program. Simply talking, to get shell.  
Two important features of shellcode:  
1. character size limitation  
2. position independent  

assembly code is readable representation of machine code...  

## How to get the assembly output?
1. use gcc with source code  
```
gcc -S test.c
```  

## How to run the assembly code?
1. compile it to the exe file  
```
nasm -felf32 test.s -o test.o
ld test.o -melf_i386 -o test
```  
2. pwntools  
```python
from pwn import *
s = asm(
"""
...
.ascii "test"
.byte 0
""",arch="i386")
```  

## Convert between assembly code and machine code
[Online x86 / x64 Assembler and Disassembler](https://defuse.ca/online-x86-assembler.htm)  
With the tool, you can convert the assembly code to make a shellcode payload, or convert the shellcode to make readable.  

## The easiest way to test your shellcode
```c
#include <stdio.h>

char shellcode[] = "\x..\x..\x.......";

int main(){
	void (*fptr)() = shellcode;
	fptr();
}
// gcc -m32 -z execstack test.c -o test
```  

## Sime tricks to write shellcode
Put the address of the string into register ebx  
1. push and mov  
```
push 0xblah   // now esp points to the 0xblah
mov ebx, esp   // put the pointer address into ebx
```  
2. call function  
```
success:
   pop ebx     // 2. get the top of the stack, which is the address of blah
main:
   call success    // 1. push the next instruction address(return address) onto the stack
   db 'blah',0xa
```
