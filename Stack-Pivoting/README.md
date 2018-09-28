## Stack Pivoting  
Move esp/rsp to a bigger buffer which has been put with our payload.  
  
## Ideas  
The main idea of migrating the stack place is use with gadgets such like ```leave; ret;```  
because `leave` is equal to ```mov rsp, rbp; pop rbp;```  
  
## Draw some pictures  
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
Gadgets A:  `pop rbp; ret;`  
```
      ---------      ---------
     |         |    |         |
      ---------      ---------
     |         |    | rbp val | <buf2 <rbp
      ---------      ---------
     |         |    |  adr C  |
      ---------      ---------
rsp> |  adr B  |    | rax val |
      ---------      ---------
     |         |    |         |
      ---------      ---------

rbp: bf2 address
return to gadget B
```  
Gadgets B: `mov rsp, rbp; pop rbp; ret;`  
```
      ---------      ---------
     |         |    |         |
      ---------      ---------
     |         |    |         | <buf2 <rsp
      ---------      ---------
     |         |    |  adr C  |
      ---------      ---------
     |         |    | rax val |
      ---------      ---------
     |         |    |         |
      ---------      ---------

rbp: rbp val
rsp: bf2 address
return to gadget C
```  
Gadgets C: `pop rax; ret;`  
```
      ---------      ---------
     |         |    |         |
      ---------      ---------
     |         |    |         | <buf2 <rsp
      ---------      ---------
     |         |    |         |
      ---------      ---------
     |         |    |         |
      ---------      ---------
     |         |    |         |
      ---------      ---------
      
rax: rax val
```  
  
## Practice  
[Sean Practice](https://github.com/shinmao/CTF-writeups/blob/master/Advanced%20Binary%20Exploitation(Sean)/src/rop1.c)
