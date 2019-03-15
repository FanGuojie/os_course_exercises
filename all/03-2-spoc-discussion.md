# lec6 SPOC思考题


NOTICE
- 有"w3l2"标记的题是助教要提交到学堂在线上的。
- 有"w3l2"和"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的git repo上。
- 有"hard"标记的题有一定难度，鼓励实现。
- 有"easy"标记的题很容易实现，鼓励实现。
- 有"midd"标记的题是一般水平，鼓励实现。

## 与视频相关思考题

### 6.1	非连续内存分配的需求背景
  1. 为什么要设计非连续内存分配机制？
     * 提高分配的灵活性
     * 提高内存的利用效率：方便共享、充分利用内存空间
     * 避免碎片产生
     * 允许一个程序使用非连续的物理空间
     * 运行共享代码与数据
     * 支持动态加载于链接


  1. 非连续内存分配中内存分块大小有哪些可能的选择？大小与大小是否可变?
     * 内存块大，管理方便
     * 内存块小，使用更灵活


 1. 为什么在大块时要设计大小可变，而在小块时要设计成固定大小？小块时的固定大小可以提供多种选择吗？

    在大块时，数量不多，管理方便，这是大小可变可以相对更灵活

    在小块时，数量多，灵活但管理困难，固定大小可以减少管理难度

### 6.2	段式存储管理
 1. 什么是段、段基址和段内偏移？

    段表示访问方式和存储数据等属性相同的一段地址空间


 1. 段式存储管理机制的地址转换流程是什么？为什么在段式存储管理中，各段的存储位置可以不连续？这种做法有什么好处和麻烦？

    段式存储管理中，地址转换是段基址（段号）加段内偏移

    段反映了程序的存储结构，程序不会从一个段的基址去访问另一个段，于是不同的段可以不连续

    好处是可以不连续，方便内存管理

    麻烦是地址转换稍微复杂一些


### 6.3	页式存储管理
 1. 什么是页（page）、帧（frame）、页表（page table）、存储管理单元（MMU）、快表（TLB, Translation Lookaside Buffer）和高速缓存（cache）？

    页：进程逻辑地址空间划分的基本单位

    帧：物理内存划分的基本单位

    页表：*页表*是一种特殊的数据结构，放在系统空间的*页表*区，存放逻辑页与物理页帧的对应关系

    存储管理单元：管理虚拟内存系统 的器件

    快表：从虚拟地址到物理地址的匹配表

    高速缓存：是用于减少处理器访问内存所需平均时间的部件。 在金字塔式存储体系中它位于自顶向下的第二层，仅次于CPU寄存器。 其容量远小于内存，但速度却可以接近处理器的频率。

 1. 页式存储管理机制的地址转换流程是什么？为什么在页式存储管理中，各页的存储位置可以不连续？这种做法有什么好处和麻烦？

    页式存储管理中，地址转换是页号加页内偏移

    CPU使用连续的逻辑地址，存储访问时，逻辑地址先分成逻辑页号和页内偏移，然后通过页表定义的对应关系，把逻辑页面转换成物理页号，最后再把物理页号加页内偏移得到物理地址；于是不同的段可以不连续

    好处是可以不连续，方便内存管理中的存储分配和回收；麻烦是地址转换比较复杂（页表项访问开销和页表存储开销），并且频繁进行（每次存储访问会变成两次或更多）


### 6.4	页表概述
 1. 每个页表项有些什么内容？有哪些标志位？它们起什么作用？

    * 内容
      * 页号
      * 块号（页框号）
      * 标志位
    * 标志位
      * 中断位：用于判断该页是不是在内存中，如果是0,表示该页面不在内存中，会引起一个缺页中断
      * 保护位（存取控制位）：用于指出该页允许什么类型的访问，如果用一位来标识的化：1表示只读，0表示读写
      * 修改位（脏位）：用于页面的换出，如果某个页面被修改过（即为脏），在淘汰该页时，必须将其写回磁盘，反之，可以直接丢弃该页
      * 访问位：不论是读还是写，系统都回设置该页的访问位，它的值用来帮助操作系统中发生缺页中断时选择要淘汰的页，即用于页面置换
      * 高速缓存禁止位（辅存地址位）：对于那些映射到设备寄存器而不是常规内存的页面有用，假设操作系统正在循环等待某个I/O设备对其指令进行响应，保证硬件不断地从设备中读取数据而不是访问一个旧的高速缓存中的副本是非常重要的。即用于页面调入。

    ​	

 1. 页表大小受哪些因素影响？

    页大小、地址空间大小、进程数目


### 6.5	快表和多级页表
 1. 快表（TLB）与高速缓存（cache）有什么不同？

    TLB在硬件上和cache一样，是处理器内部的一小块高速SRAM内存，用于缓存，与cache不同的是，它专门缓存存放在内存中的页表，容量相对较小，而cache则用于缓存普通内存，容量相对较大。

 1. 为什么快表中查找物理地址的速度非常快？它是如何实现的？为什么它的的容量很小？

    * 速度快：因为它是在多个表项中同步查找有没有对应的线性地址项（全相连），并且在CPU中是一个寄存器
    * 实现：当cpu要访问一个虚拟地址/线性地址时，CPU会首先根据虚拟地址的高20位（20是x86特定的，不同架构有不同的值）在TLB中查找。如果是表中没有相应的表项，称为TLB miss，需要通过访问慢速RAM中的页表计算出相应的物理地址。同时，物理地址被存放在一个TLB表项中，以后对同一线性地址的访问，直接从TLB表项中获取物理地址即可，称为TLB hit。
    * 容量小：因为用电路换时间了（多路并行查找），成本和耗电量比较高。

 1. 什么是多级页表？多级页表中的地址转换流程是什么？多级页表有什么好处和麻烦？

    答：

    ​	多级页表是有多层次的页表。地址转换流程就是不断根据每一级的页号和页表基址查找下一级的页表基址（或者查到页表项）。

    好处是减小了页表占据的空间（因为程序一般不会用完自己的虚拟地址空间，所以大部分次级页表不需要生成）；麻烦是地址转换变得更加复杂和缓慢了。


### 6.6	反置页表
 1. 页寄存器机制的地址转换流程是什么？

    ​	逻辑地址进行hash，然后查相应页寄存器

    ​	用快表缓存页表项后的页寄存器搜索步骤

    - 对逻辑地址进行Hash变换
    - 在快表中查找对应页表项
    - 有冲突时遍历冲突项列表
    - 查找失败时，产生异常

 1. 反置页表机制的地址转换流程是什么？

    ​	逻辑地址和进程号共同进行hash，然后查相应页寄存器

    ​	查找过程：

    - 从逻辑地址中得到页号
    - 根据页号和PID计算出Hash值
    - 在反置页表中查找对应的页表项，核对页号是否一致，从中找出相应的物理帧号；处理hash冲突

 1. 反置页表项有些什么内容？

    PID、逻辑页号、标志位

### 6.7	段页式存储管理
 1. 段页式存储管理机制的地址转换流程是什么？这种做法有什么好处和麻烦？

    * 地址转换流程：

      在段页式系统中，为了便于实现地址变换，须配置一个段表寄存器，其中存放段表始址和段表长TL。

      1) 进行地址变换时，首先利用段号S，将它与段表长TL进行比较。若S<TL，表示未越界

      2) 于是利用段表始址和段号来求出该段所对应的段表项在段表中的位置，从中得到该段的页表始址

      3) 利用逻辑地址中的段内页号P来获得对应页的页表项位置，从中读出该页所在的物理块号b

      4) 再利用块号b和页内地址来构成物理地址。

    * 好处：

      (1) 它提供了大量的虚拟存储空间。

      (2) 能有效地利用主存，为组织多道程序运行提供了方便

    * 麻烦：

      (1) 增加了硬件成本、系统的复杂性和管理上的开消。

      (2) 存在着系统发生抖动的危险。

      (3) 存在着内碎片。

      (4) 还有各种表格要占用主存空间。

    

    

 1. 如何实现基于段式存储管理的内存共享？

    把需要重用的内存映射到不同的段里

 1. 如何实现基于页式存储管理的内存共享？

    不同的页表项指向相同的物理页

## 个人思考题
（1） (w3l2) 请简要分析64bit CPU体系结构下的分页机制是如何实现的

答：**64bit CPU体系结构下的分页机制是**通过以4KB为基本分页单位来采用四级页表管理虚实映射。

每个页表项占据64位，因此每个作为页表的物理页面可以存放512个页表项，从而最末级页表所映射出来的物理内存大小为512*4KB=2MB，依次类推，在上一级页面（PMD）中，每一个PMD表项可映射2MB的物理内存。当采用2MS作为分页的基本单位时，内核中则设置了三级页表。在三级页表中，最末以及页表为PM表，同样的，每一个PMD表项指出了一个2MB的大页面，也即虚拟地址的低21位作为大页面的页内偏移，二高位则作为大页面的页面编号（pfn)。为了能让MMU正确地进行虚实地址转换，必须告知MMU哪个页表项映射的是4KB的物理页面，哪个页表项映射的是2MB的大页面，这是通过页表项标志位_PAGE_PSE来区分的，这一般是通过内联函数pte_mkhuge()设置的。同时由于是四级页表，页可以1G页面的转换。

64位的寻址空间能够寻址16EB的内存大小，对于目前的硬件来说太大了。在X64体系结构下，只实现了48位虚拟地址，高12位作为符号位扩展。兼容模式下，使用32位。



## 小组思考题
（1）(spoc) 某系统使用请求分页存储管理，若页在内存中，满足一个内存请求需要150ns (10^-9s)。若缺页率是10%，为使有效访问时间达到0.5us(10^-6s),求不在内存的页面的平均访问时间。请给出计算步骤。

0.5*10^-6=0.9 * 0.15 * 10^-6+0.1 * x=>x=0.365us

（2）(spoc) 有一台假想的计算机，页大小（page size）为32 Bytes，支持32KB的虚拟地址空间（virtual address space）,有4KB的物理内存空间（physical memory），采用二级页表，一个页目录项（page directory entry ，PDE）大小为1 Byte,一个页表项（page-table entries
PTEs）大小为1 Byte，1个页目录表大小为32 Bytes，1个页表大小为32 Bytes。页目录基址寄存器（page directory base register，PDBR）保存了页目录表的物理地址（按页对齐）。

PTE格式（8 bit） :
```
  VALID | PFN6 ... PFN0
```
PDE格式（8 bit） :
```
  VALID | PT6 ... PT0
```
其
```
VALID==1表示，表示映射存在；VALID==0表示，表示映射不存在。
PFN6..0:页帧号
PT6..0:页表的物理基址>>5
```
在[物理内存模拟数据文件](./03-2-spoc-testdata.md)中，给出了4KB物理内存空间的值，请回答下列虚地址是否有合法对应的物理内存，请给出对应的pde index, pde contents, pte index, pte contents。
```
1) Virtual Address 6c74
   Virtual Address 6b22
2) Virtual Address 03df
   Virtual Address 69dc
3) Virtual Address 317a
   Virtual Address 4546
4) Virtual Address 2c03
   Virtual Address 7fd7
5) Virtual Address 390e
   Virtual Address 748b
```

比如答案可以如下表示： (注意：下面的结果是错的，你需要关注的是如何表示)
```
Virtual Address  6c74:
  --> pde index:0x1b  pde contents:(valid 1, pfn 0x20)
    --> pte index:0x3  pte contents:(valid 1, pfn 0x61)
     --> Translates to Physical Address 0xc34 --> Value: 0x6
Virtual Address 6b22:
  --> pde index:0x1a  pde contents:(valid 1, pfn 0x52)
    --> pte index:0x19  pte contents:(valid 1, pfn 0x47)
     --> Translates to Physical Address 0x8e2 --> Value: 0x1a
Virtual Address  03df:
  --> pde index:0x0  pde contents:(valid 1, pfn 0x5a)
    --> pte index:0x1e  pte contents:(valid 1, pfn 0x5)
     --> Translates to Physical Address 0xbf --> Value: 0xf
Virtual Address 69dc:
  --> pde index:0x1a  pde contents:(valid 1, pfn 0x52)
    --> pte index:0xe  pte contents:(valid 0, pfn 0x7f)
      	--> Fault (page directory entry not valid)
Virtual Address  317a:
  --> pde index:0xc  pde contents:(valid 1, pfn 0x18)
    --> pte index:0xb  pte contents:(valid 1, pfn 0x35)
     --> Translates to Physical Address 0x6ba --> Value: 0x1e
Virtual Address 4546:
  --> pde index:0x11  pde contents:(valid 1, pfn 0x21)
    --> pte index:0xa  pte contents:(valid 0, pfn 0x7f)
      	--> Fault (page directory entry not valid)
Virtual Address  2c03:
  --> pde index:0xb  pde contents:(valid 1, pfn 0x44)
    --> pte index:0x0  pte contents:(valid 1, pfn 0x57)
     --> Translates to Physical Address 0xae3 --> Value: 0x16
Virtual Address 7fd7:
  --> pde index:0x1f  pde contents:(valid 1, pfn 0x12)
    --> pte index:0x1e  pte contents:(valid 0, pfn 0x7f)
      	--> Fault (page directory entry not valid)
Virtual Address  390e:
  --> pde index:0xe  pde contents:(valid 0, pfn 0x7f)
      --> Fault (page directory entry not valid)
Virtual Address 748b:
  --> pde index:0x1d  pde contents:(valid 1, pfn 0x0)
    --> pte index:0x4  pte contents:(valid 0, pfn 0x7f)
      	--> Fault (page directory entry not valid)

```

[链接](https://piazza.com/class/i5j09fnsl7k5x0?cid=664)有上面链接的参考答案。请比较你的结果与参考答案是否一致。如果不一致，请说明原因。



（3）请基于你对原理课二级页表的理解，并参考Lab2建页表的过程，设计一个应用程序（可基于python、ruby、C、C++、LISP、JavaScript等）可模拟实现(2)题中描述的抽象OS，可正确完成二级页表转换。

[链接](https://piazza.com/class/i5j09fnsl7k5x0?cid=664)有上面链接的参考答案。请比较你的结果与参考答案是否一致。如果不一致，提交你的实现，并说明区别。

```python
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

```

（4）假设你有一台支持[反置页表](http://en.wikipedia.org/wiki/Page_table#Inverted_page_table)的机器，请问你如何设计操作系统支持这种类型计算机？请给出设计方案。

答：

​	在利用反置页表进行地址变换时，是用进程标志符和页号去检索反置页表；若检索完整个页表都未找到与之匹配的页表项，表明此页此时尚未调入内存，对于具有请求调页功能的存储器系统应产生请求调页中断，若无此功能则表示地址出错；如果检索到与之匹配的表项，则该表项的序号i便是该页所在的物理块号，将该块号与页内地址一起构成物理地址。
​	虽然反置页表可以有效地减少页表占用的内存，然而该表中却只包含已经调入内存的页面，并未包含那些未调入内存的各个进程的页面，因而必须为每个进程建立一个外部页表(External Page Table)，该页表与传统页表一样，当所访问的页面在内存时并不访问这些页表，只是当不在主存时才使用这些页表。该页表中包含了页面在外存的物理位置，通过该页表可将所需要的页面调入内存。
​	由于在反置页表中是为每一个物理块设置一个页表项的，通常页表项的数目很大，从几千项到几万项，要利用进程标识符和页号去检索这样大的线性表是相当费时的。于是又利用一种Hash表来检索。

 (5)[X86的页面结构](http://os.cs.tsinghua.edu.cn/oscourse/OS2019spring/lecture06)
---

## 扩展思考题

阅读64bit IBM Powerpc CPU架构是如何实现[反置页表](http://en.wikipedia.org/wiki/Page_table#Inverted_page_table)，给出分析报告。


## interactive　understand VM

[Virtual Memory with 256 Bytes of RAM](http://blog.robertelder.org/virtual-memory-with-256-bytes-of-ram/)：这是一个只有256字节内存的一个极小计算机系统。按作者的[特征描述](https://github.com/RobertElderSoftware/recc#what-can-this-project-do)，它具备如下的功能。

 - CPU的实现代码不多于500行；
 - 支持14条指令、进程切换、虚拟存储和中断；
 - 用C实现了一个小的操作系统微内核可以在这个CPU上正常运行；
 - 实现了一个ANSI C89编译器，可生成在该CPU上运行代码；
 - 该编译器支持链接功能；
 - 用C89, Python, Java, Javascript这4种语言实现了该CPU的模拟器；
 - 支持交叉编译；
 - 所有这些只依赖标准C库。

针对op-cpu的特征描述，请同学们通过代码阅读和执行对自己有兴趣的部分进行分析，给出你的分析结果和评价。
