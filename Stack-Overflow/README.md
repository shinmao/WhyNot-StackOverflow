# What's Stack overflow?  
The data write into the buffer exceeds its size. The overflow can change the value of neighborhood, and hacker can use it to crash the program or even hijack the program.  
There is some limit for us to make an overflow.  
1. We can write into stack.  
2. The size of data hasn't be well controlled.  
  
## Start Overflow  
Basiclly, we would like using overflow to overwrite the return address of the function to the place we can control, and the place should also be executable!  
In this part, we always need to be sure that how much padding can let us overwrite the return address.  
1. Open your source code and laugh!  
2. Open your **IDA**  
3. PWNTOOLS Bruteforce
  
## Dangerous function    
* gets  (read the whole line and ignore \x00
* scanf  
* vscanf  
* sprintf  
* strcpy (copy string until \x00  
* strcat (append string until \x00
* strlen  (count the length of string until \x00
* bcopy
 
