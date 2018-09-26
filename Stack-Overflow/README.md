# What's Stack-based overflow?  
The data write into the buffer exceeds its size. The overflow can change the value of neighborhood, and hacker can use it to crash the program or even hijack the program.  
There is some limit for us to make an overflow.  
1. We can write into stack.  
2. The size of data hasn't be well controlled.  
  
## Start Overflow  
Basiclly, we would like using overflow to overwrite the return address of the function to the place we can control, and the place should also be executable!  
In this part, we always need to be sure that how much padding can let us overwrite the return address.  
1. Open your source code and laugh!  
2. Open your **IDA**  
We can always find some code in IDA just like following . 
Assume x86
```C
int vul()
{
    char s;  // [sp+4h][bp-14h]  
    gets(&s);  
    return puts(&s);  
}
``` 
s is where our input will be put, and with IDA label, we can see that its distance between with bp is 0x14, therefore we can guess the structure of stack now!  
```C
         +---------------+  
         |   ret addr    |  
         +---------------+  
         |   saved ebp   |  
   ebp-> +---------------+  
         |               |
         |               |
         |               |
         |               |
ebp-0x14>+---------------+
```  
Finally, our payload might be `"A"x0x14 + "A"x0x4 + ret_to_evil_addr`  
3. PWNTOOLS Bruteforce . 
This is the most common method I use, I will try to make segmentation fault and use the command of **crashoff** in GDB, then I can get the distance between ret address and input buffer!
  
## Dangerous function   
Function | Details
------------ | -------------
scanf | scanf("%s",buf) **%s** won't check the boundary, you need to use "%(num)%s"
gets |  No boundary check, most dangerous!!  
read |  leakable  
fread|  Same as read 
strcpy | strcpy(buf1,buf2),overflow 
strcat | strcat(buf1,buf2),overflow   
strlen | strlen(buf) you can use \x00 to bypass the check!
