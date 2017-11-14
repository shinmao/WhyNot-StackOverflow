# What's ROP?
When we face the challenge of NX on the stack, we need to change our attack way. For example, use gadget in memory to change the register value, when we finish the change the call system(), we can get the shell, and this is ROP! The gadget of ROP usually ends with **ret**, because ret can pop rip and help us control it!!  
Fowllowing are the condition we need to fullfill before we start ROP:  
1. Overflow to get return address  
2. We can find gadgets, if PIE is open, we also should leak the address of gadgets!  
  
## Learn by Breaking it   
:boom: **ret2syscall**  
To start with ROP, I love a picture of stack to figure out with.  
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/picture/ROP.png" width="373" height="385">  
With this picture, we could realize how to make up our own payload!  
:star2: **ret2plt**  
  
## Shell  
Some concept you need to be aware of:  
1. We need to write shellcode in the executable section  
2.  
  
## Advanced 
  
## Practice  
Kinds of ROP | practice link  
------------ | --------------  
Would you like to try simple rop first? | ![NTU 2017 ROP](https://github.com/shinmao/CTF-writeups/tree/master/NTU-CTF-2017/simple_rop)

