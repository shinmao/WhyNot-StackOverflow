# What's ROP?
When we face the challenge of NX on the stack, we need to change our attack way. For example, use gadget in memory to change the register value, when we finish the change the call system(), we can get the shell, and this is ROP! The gadget of ROP usually ends with **ret**, because ret can pop rip and help us control it!!  
Fowllowing are the condition we need to fullfill before we start ROP:  
1. Overflow to get return address  
2. We can find gadgets, if PIE is open, we also should leak the address of gadgets!  
  
## Learn by Breaking it   
There are various kinds of ROP.  
Remember that all we want to complete is just ```execve('/bin/sh');```  
  
:camel: Put shellcode into the buffer in .bss or on stack, and return to it.  
Challenge: The place you put shellcode in needs to have **execution permission**.  
  
:camel: Return to ```pop rax; ret;```; return to ```pop rdi; ret;``` and give him address of /bin/sh; return to ```syscall;```  
Challenge: You may not find the gadgets on elf and should leak the base first.  
  
:camel: Return to libc( return to the function in libc.  
In libc, our goal is to ```system('/bin/sh');```  
In order to bypass ASLR, these are our steps:  
[.] leak address of --libc-start-main  
[.] Get the base of libc  
[.] Get the address of system and string /bin/sh in libc  
[.] Run, overflow, return to system('/bin/sh')  
**Please take a look at the file ret2libc-good-luck.py(Be careful that the file is x86-based)**  
  
## Shell  
Some concept you need to be aware of:  
1. We need to write shellcode in the executable section  
2. If we cannot exe the whole shellcode, we need to complete system('/bin/sh') or execve('/bin/sh',NULL,NULL).  
3. For the string 'sh', you can start finding from program first because you don't need to care about the ASLR. There must have '/bin/sh' in the libc; however; you may need to leak the libc base first.  
  
## Find real address  
1. Existing functions in binary.  
2. puts, write the GOT. (Be careful that the function need to be resolved!  
**PUTS** until \x00.  
**WRITE** can even control the printed length.  
  
## Advanced 
  
## Practice  
Kinds of ROP | practice link  
------------ | --------------  
Would you like to try simple rop first? | [NTU 2017 ROP](https://github.com/shinmao/CTF-writeups/tree/master/NTU-CTF-2017/simple_rop)

