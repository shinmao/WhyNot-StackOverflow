# Format String Attack

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
e.g., `%3$p` points to the fourth parameter because the first parameter is format string itself!

## Use of Format String
```
%[flags][width][.precision][length]specifier
```  
You can find definition of [format string](https://www.cplusplus.com/reference/cstdio/printf/) at here.  
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

// the use of width and length
// the minimum length of string is 5, the result would be "Hello World"
printf("%5s", "Hello World");
// the maximum length of string is 9, the result would be "Hello Wor"
printf("%.9s", "Hello World");
```  
You may get tired with the rules above. Don't worry, I will show how to use it in soon.:+1:  
> When we start to attack, we also need to be careful **null bytes**(`\x00`) would stop the format string, this usually happen in 64-bits program!  
  
### First, tell you a little trick
When we neen to make the payload, the number before c is always a complex problem.  
Therefore, how about make up a function to calculate for us.
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
Besides, we can use gdb-peda to get the index of argument such as the **fmtarg** in the following example.
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/fmtarg.png" width="474" height="280">  

## Help with your Buffer Overflow
Already know that we need to length of string to overwrite the ret address.  
Therefore, We can use %(num)d, %(num)u, or %(num)x to stretch the original one.  

## Write to arbitrary memory  
```C
"12345%3$n"   //write len(12345) to the fourth parameter  
"%123c%3$n"   //write 123 to the fourth parameter because "c" is the count
"%123c%3$hhn" //write one byte
"%30c%3$hhn%70c%4$hhn"   //Be careful, this mean we write 30 into fourth parameter and 100 to the fifth parameter!!
```  
How if we want to write a large address such as `0x66778899`? The case would be more serious in a 64-bits program  
![fmt-write](https://user-images.githubusercontent.com/9136748/157985782-18c104ee-71d8-4212-8e20-9062f3df81b3.png)  
If we convert `0x66887799` to the decimal count and put it in format string (e.g, `%1719109785c...`), it would take a long time to output such large numbef of characters. In this case, we can group them by two bytes (`%hn`) or one bytes (`%hhn`) to make it easier. Just as the screenshot above, it can write `0x6688` into higher two bytes and `0x7799` into lower two bytes. `Notice!` The value written by `$n` is decided by the count of output so far. Therefore, the count until the first `%hn` is 0x6688 (two addresses(8 bytes) + `%.8x` * 4(32 bytes) + `_` * 5(5 bytes) + `@@@@`(4 bytes) + `%.26199x`(26199 bytes))   

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
**Be sure that RELRO not be FULL**. When RELRO is open, pltsymbol will be removed.  
  
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
[The reading I recommend so much](https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/formatstring-umustread.pdf)
