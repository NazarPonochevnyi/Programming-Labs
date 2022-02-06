import sys
from unicorn import *
from unicorn.x86_const import *
from capstone import *

if len(sys.argv) != 2:
    print(f"USAGE: {sys.argv[0]} [filepath]")
    sys.exit()

cs = Cs(CS_ARCH_X86, CS_MODE_64)


def hook_code(uc, address, size, user_data):
    global cs
    mem = uc.mem_read(address, size)
    for i in cs.disasm(mem, size):
        print("hook 0x{:03x} size {:2d}: {:20s} {} {}".format(
            address, size, i.bytes.hex(), i.mnemonic, i.op_str))
        if i.bytes.hex() == "cd80":
            rax = mu.reg_read(UC_X86_REG_RAX)
            rbx = mu.reg_read(UC_X86_REG_RBX)
            rsi = mu.reg_read(UC_X86_REG_RSI)
            if rax == 11:
                sh_data = [bytes(x) for x in mu.mem_read(
                    rbx, 0x1000).split(b"\0")[:16] if x != b""]
                sh, args = (sh_data[0] + sh_data[1]
                            ).decode("utf8"), sh_data[2].decode("utf8")
                cmd_data = [bytes(x) for x in mu.mem_read(
                    rsi, 0x1000).split(b"\0")[:16] if x != b""]
                cmd = cmd_data[2].decode("utf8")
                print(f"[SYSCALL] sys_execve {sh} {args} {cmd}")
            else:
                print(f"[SYSCALL] rax = 0x{rax}, rbx = 0x{rbx}, rsi = 0x{rsi}")


print(f"\nOpening {sys.argv[1]} file for processing...\n")
with open(sys.argv[1], "rb") as file:
    code = file.read()
address = 0x08048000

mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.mem_map(address, address + 0x2000)
mu.mem_write(address, code)
mu.reg_write(UC_X86_REG_ESP, address + 0x1000)

mu.hook_add(UC_HOOK_CODE, hook_code)

try:
    mu.emu_start(0x08048054, address + len(code))
except:
    pass
print("\nDone")
