# What's ROP?
When we face the challenge of NX, we need to change our attacking way. Use gadget existing in memory to build up your shellcode again, and this is ROP! The gadget of ROP usually ends with **ret**, because ret can pop rip and help us control it!!  
Fowllowing are the condition we need to fullfill before we start ROP:  
1. Overwrite return address  
2. We can find gadgets, if PIE is open, we also should leak the address of gadgets!    
  
## How to find gadgets?
`pop rax; ret` would be better than `mov rax, <val>` because the there would no the piece of value you want in binary.

## ROP (find in `/file/rop`)
```c
...
int main(){

    init();

    puts( "Say hello to stack :D" );

    char buf[0x30];
    gets( buf );

    return 0;
}
```
This is a sample helping to figure out how ROP works. Check the makefile in folder, we can see that pie, canary are disabled. Also we should be able to find a lot of gadgets because it is static-linked.  
This code would open a buffer of 48 bytes to receive our input. We cannot use shellcode to launch attack because NX is enabled. How do I hijack the control flow to pop a shell?  
First step is to overwrite the return address of main function and go to gadget one:  
```
------------  <---- rsp
|          |
|          |  <-- 0x30 bytes
|          |
------------
| saved rbp|  <-- 0x8 bytes
------------
| ret addr |
------------
```
Therefore, we would use `0x38` bytes of junk data to overflow and overwrite return address then. Here, we know we can hijack the control flow. But what should our control flow be like? To pop up a shell, our ideal goal is to call `execve('/bin/sh', 0, 0)`. Take a look at [syscall table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/), `sys_execve` needs rax to be 59, rdi to be address of `/bin/sh`, then both rsi and rdx to be 0.  
To find the gadgets, here comes a popular tools: [ROPgadget](https://github.com/JonathanSalwan/ROPgadget).  
I would not describe the whole process of finding gadgets, it costs a long time. I would directly introduce the control flow hijacked by my rop chain:  
```
-----------
pop rdi; ret;   <-- ret addr of main function (gadget 1)
-----------
    bss
-----------
pop rsi; ret;   <-- ret addr of gadget 1 (gadget 2)
-----------
 "/bin/sh\0"
-----------
mov qword ptr [rdi], rsi; ret;  <-- ret addr of gadget 2 (gadget 3)
-----------
pop rdx; pop rsi; ret;   <-- ret addr of gadget 3 (gadget 4)
-----------
     0
     0
-----------
pop rax; ret;    <-- ret addr of gadget 4 (gadget 5)
-----------
     59
-----------
  syscall     <-- ret addr of gadget 5 (gadget 6)
```
Here we use six gadgets to make the syscall of execve. Let me explain gadgets one by one.  
1. Gadget 1 is to put the address of string(`/bin/sh`) into rdi. We can find a writeable place in virtual memory (It's possible to ruin program), here I choose bss section. When `ret` is executed, stuff pointed by rsp would be poped into rip. Therefore, rip would point to gadget 1 and execute it. At the same time, rsp points to bss. When gadget 1 try to pop rdi, the bss would be put into rdi. In final step, stack would pop again with `ret` executed, so rip point to gadget 2.  
2. Gadget 2 is to put string(`/bin/sh`) into rsi because we plan to put it into the bss in further step. Same, pop rsi then string would be put into rsi. In final step, rip point to gadget 3.  
3. Gadget 3 is to put value of rsi which is `/bin/sh` into the address referred by rdi, which is bss. In final step, rip point to gadget 4.  
4. Gadget 4 is to give 0 to both rdx and rsi. In final step, rip point to gadget 5.  
5. Gadget 5 is to give 59 to rax, then rip point to gadget 6.  
6. Gadget 6, final gadget, make syscall.  
Exploit: (`/file/rop/exp.py` run with python2)
  
## Practice  
Kinds of ROP | practice link  
------------ | --------------  
Would you like to try simple rop first? | [NTU 2017 ROP](https://github.com/shinmao/CTF-writeups/tree/master/NTU-CTF-2017/simple_rop)