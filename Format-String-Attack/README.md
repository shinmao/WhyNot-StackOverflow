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

## Write to arbitrary memory  

## Advanced trick
