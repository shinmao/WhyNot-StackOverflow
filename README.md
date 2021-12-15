# WhyNot-StackOverflow
Some tips of Buffer attack on Stack.  
  
## Guide  
1. [Shellcode](https://github.com/shinmao/WhyNot-StackOverflow/tree/master/Shellcode)  
2. [Stack based Overflow](https://github.com/shinmao/WhyNot-StackOverflow/tree/master/Stack-Overflow) 
3. [Return to library](https://github.com/shinmao/WhyNot-StackOverflow/tree/master/ret2libc)  
4. [ROP](https://github.com/shinmao/WhyNot-StackOverflow/tree/master/ROP)  
5. [stack pivoting](https://github.com/shinmao/WhyNot-StackOverflow/tree/master/Stack-Pivoting)  
6. [Format String attack](https://github.com/shinmao/WhyNot-StackOverflow/tree/master/Format-String-Attack)   

(Sorry for putting format string in stackoverflow, but I just link stack based kind so......just enjoy  
  
## Type (There is also vulnerability if you not know how big the type actually is)  
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/picture/type.png" width="411" height="275">

## Pass arguments to function
In x86, program uses stack to pass the function arguments.  
In x64, program will use `rdi, rsi, rdx, rcx, r8, r9` to pass arguments, then use stack if more.  
  
## Want some asm?  
operation | what means?
------------ | -------------
mov eax, DWORD PTR [esp+4] | eax = 0x80484d0(value in address of esp+4)
lea eax, DWORD PTR [esp+4] | eax = esp+4(the address itself)
add/sub dest, src | add/sub dest with src and store the result into dest
cmp eax, 1 | sub eax, 1 -> just check whether eax is 1 and store result in eflags
AND | only 1 AND 1 can be 1 .........
OR | only 0 OR 0 can be 0.......
XOR eax, eax | used to clean the register -> eax = 0 
test eax, eax | AND eax, eax -> just check whether eax is 0 and store result in eflags
push eax | push value of eax to the top of stack (also become pointed by esp)
pop eax | delete the top of the stack and put its value into eax 
jmp 0x8048436 | conditionally or unconditionally jump to address 0x8048436
ret | pop the top of the stack (address) into eip  
nop | 0x90  
syscall | 0x80  
call | push ret addr then jmp  
ret | pop ret addr
  
## GDB  
Are you confused about why your GDB cannot attach with the error of 'permission denied'?  
```
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```

## x64 vs x86  
if x86, arguments of function will be on **stack**!  
if x64, first six arguments of function will be on RDI, RSI, RDX, RCX, R8, R9, stored in stack only if more!  

## program header
Peogram header shows how the program map into the virtual memory.  
```
readelf -l ./elf
```
A segment contains multiple sections.  

## How dynamic-linking different from static-linking  
In static-linking, program starts the `main` part right after the `_start`. However, in dynamic-linking program,  
```
_start -> __libc_start_main -> .init -> main -> .fini -> exit
```  

## `execve` v.s. `int 0x80` v.s. `syscall` v.s. `system`
Shellcode for `execve` in x86
```asm
eax = 0x0b
ebx -> "/bin/sh"
ecx = 0x0
edx = 0x0

execve("/bin/sh", 0, 0)
```
In x86, use assembly instruction `int 0x80` to make syscall.  
Shellcode for `execve` in x86_64
```asm
rax = 0x3b
rdi -> "/bin/sh"
rsi = 0x0
rdx = 0x0

execve("/bin/sh", 0, 0)
```
In x86_64, use assembly instruction `syscall` to make syscall.  

What is the difference between system and execve?  
system is glibc function, using shell to call program: `fork` + `exec` + `waitpid`; while execve will directly overwrite the process who called him. This means that if I use execve to call shell, I will **never be able to back to my original process**.  
Shellcode for `system` has two ways:
```c
system("/bin/sh")
system("sh")
```
Don't need rax/eax values, but following the calling convention for stack on x86 and register on x86_64.