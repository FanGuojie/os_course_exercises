import sys


def virtual2physical(vaddr, pdbr, mem):
    pde_index = vaddr >> 10
    pde = mem[pdbr + pde_index]
    valid_bit = pde >> 7
    pde &= 0b01111111
    print("  --> pde index:%s  pde contents:(valid %d, pfn %s)" %
          (hex(pde_index), valid_bit, hex(pde)))
    if not valid_bit:
        print("      --> Fault (page directory entry not valid)")
        return None
    pt = pde << 5
    pte_index = (vaddr >> 5) & 0b11111
    pte = mem[pt + pte_index]
    valid_bit = pte >>7
    pte &= 0b01111111

    print("    --> pte index:%s  pte contents:(valid %d, pfn %s)" %
          (hex(pte_index), valid_bit, hex(pte)))
    if not valid_bit:
        print("      	--> Fault (page directory entry not valid)")
        return None
    # print(bin(pfn))
    return (pte << 5) + (vaddr & 0b11111)


def loadData(file):
    mem = []
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            bs = (line.split(':')[1]).split(' ')[1:-1]
            # print(bs)
            for byte in bs:
                mem.append(int(byte, 16))

    return mem


if __name__ == '__main__':
    memory = loadData('memory.txt')
    while(True):
        # vaddr = input("输入虚拟地址(输入c表示没有新的数据)：")
        vaddr=input()
        if(vaddr == "c"):
            exit()
        print('Virtual Address %s:' % vaddr)
        vaddr = int(vaddr, 16)
        pdbr = 0x220
        paddr = virtual2physical(vaddr, pdbr, memory)
        if paddr:
            print("     --> Translates to Physical Address %s --> Value: %s" %
                  (hex(paddr), hex(memory[paddr])))
