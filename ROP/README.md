# What's ROP?
When we face the challenge of NX on the stack, we need to change our attack way. For example, use gadget in memory to change the register value, when we finish the change the call system(), we can get the shell, and this is ROP! The gadget of ROP usually ends with **ret**, because we need to use the **ropchain** to append another action.  
Fowllowing are the condition we need to fullfill before we start ROP:  
1. Overflow to get return address  
2. We can find gadgets, if PIE is open, we also should leak the address of gadgets!  
  
## Learn by Breaking it  
1. ret2text  
2. ret2shellcode (The first and the second one are return to the place which has static address such as .bss  
3. ret2syscall  
Get your ROPchain: To **execve("/bin/sh",NULL,NULL)**, we need following gadgets  
e.g.  
ROPgadget --binary ./elf > dump  
cat dump | grep "pop eax ; ret"  
e.g.  (x86)  
ROPgadget --binary ./elf --only 'pop|ret' | grep "eax"  
ROPgadget --binary ./elf --string '/bin/sh'  
ROPgadget --binary ./elf --only 'int'  
Gadgets | Details  
------- | -------
pop eax ; ret | To set eax as 0xb  
pop ebx ; ret | To set ebx as /bin/sh or sh address  
pop ecx ; ret or xor ecx | To set ecx as null  
pop edx ; ret or xor rdx | To set edx as null  
Because we cannot expect finding gadgets in consecutive memory, so we should find gadgtes and return to there.  
payload = 'padding' + p64(pop-eax-ret) + 0xb + p64(pop-edx-ecx-ebx-ret) + 0 + 0 + sh-addr + int0x80-addr  
4. ret2libc  
Return to plt, but we should know the real address of function first.  
payload = "padding" + system-plt + 'p'x4 + p64(sh-addr)  
why we need to **padding 4 bytes** right after we call system?  
Be careful that sh-addr is the argument of system(), the padding is for ret address of system()!  
However, if we don't have the address of /bin/sh, we also can write by ourselves!!  
buf = place in .bss  
payload = 'padding' + gets-plt + pop-ebx + buf + system-plt + 0xdeadbeef + buf  
r.sendline(payload)  
r.sendline('/bin/sh')  
An interesting trick, right?  
I have always use the showing function of program to leak the GOT. However, I face a challenge...  
I will put this kind of fresh new payload in the ret2libc-good-luck.py in the above!!  
In conclusion, I would recommend the last one for most, because we should always leak our real address, only by the already running function the got will be replaced with the real address, therefore I will choose **libc_start_main** to help me success!!  
  
## Shell  
Some concept you need to be aware of:  
1. We need to write shellcode in the executable section  
2.  
  
## Advanced 
  
## Practice  

