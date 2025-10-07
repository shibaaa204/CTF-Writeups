def to_signed_16bit(x):
    """Ép giá trị 16-bit không dấu thành có dấu (giống (short) trong C)"""
    return x if x < 0x8000 else x - 0x10000

def main():
    for ticket in range(0xFFFFFFFF + 1):
        local_10 = ticket
        local_c = local_10
        uVar1 = local_c

        # Câu này tương đương local_c._0_2_ = (short)local_10;
        low_16 = to_signed_16bit(local_10 & 0xFFFF)

        # Câu này là local_c._2_2_ = (short)(local_10 >> 0x10)
        high_16 = to_signed_16bit((local_10 >> 16) & 0xFFFF)

        if low_16 == -0x217 and high_16 == -0x4120:
            print(f"[+] Found winning ticket: {ticket} (0x{ticket:08X})")
            break

main()
