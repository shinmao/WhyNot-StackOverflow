# Format String Attack
First, take a look at the **printf** example.
```
printf("%p",a);   //such %p is called "Format String"
//However, many people just use like the following >
printf("a");     //or printf(buf);
```  
Now, you should know that is very **dangerous**. When the author forget to use the format string and hacker can control the   
