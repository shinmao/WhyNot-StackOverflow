## Stack Pivoting (stack migration =v=)  
When we can overflow a little bytes, migrate our stack to another place is another choice!  
  
## Ideas  
I also spend so much time on payload of stack pivoting.  
The main idea of change stack place is by gadgets of ```leave; ret;```  
because leave is the construct of ```pop rbp; mov rsp, rbp;```, remember! This is important!
  
## You need to draw some pictures  
```
      ---------      ---------
     |         |    |         |
      ---------      ---------
rsp> |  adr A  |    | rbp val | <buf2
      ---------      ---------
     | bf2 adr |    |  adr C  |
      ---------      ---------
     |  adr B  |    | rax val |
      ---------      ---------
     |         |    |         |
      ---------      ---------
```
In the pictures above, the payload in first buffer is used to leak information just like libc base, and the one in the second buffer can be used to syscall and get shell.  
  
## Practice  
[Sean Practice](https://github.com/shinmao/CTF-writeups/blob/master/Advanced%20Binary%20Exploitation(Sean)/src/rop1.c)
