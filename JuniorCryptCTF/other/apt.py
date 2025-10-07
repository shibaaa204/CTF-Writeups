from pwn import *
p=remote("ctf.mf.grsu.by", 9058)
p.sendline(b'2009')
p.sendline(b'T1566')
p.sendline(b'T1003.001')
p.interactive()
