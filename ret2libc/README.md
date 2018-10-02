# ret2libc
We already can control the return address by buffer overflow, then we can get shell if there is system function in code. However, if we don't know the address of system function or developer doesn't use system function, how do we get shell? We need to use the existing function in library, which is skill of ret2libc.

## Dynamic linking v.s. Static linking
Before starting, I need to emphasize again the difference between two linking method. Default gcc compiling would make dynamic linking for us.  
  
How do we find out an existing elf is dynamic linking or static linking?  
The assembly function code would be replaced with symbol such like `<strcpy@plt>` when you take a look into dynamic linking.  
Therefore, you also cannot use `print` to locate function with symbol when the elf is static linking.  

## Demo
Here comes an example assumed that **aslr is off** and **elf is dynamic linking**:  
  
First you can use print to get the address of function in library.  
![](https://farm2.staticflickr.com/1935/44023365595_41a9945008_b.jpg)  

Second, there is something needed to be taken care of:  
```
payload = padding + system_address + *exit_address + /bin/sh_address
```
Remember to give a address between `system_address` and argument `/bin/sh_address`. When program calls a function, it always pushes a return address onto the stack at first. Therefore, when `system` wants to get its argument, he will cross 4/8 bytes forward to find it. If you replace `exit_address` with invalid address such as `AAAA`, it would cause segmentation fault. 

