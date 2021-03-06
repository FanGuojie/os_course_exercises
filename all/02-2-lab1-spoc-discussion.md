# lec4: lab1 SPOC思考题

##**提前准备**
（请在上课前完成）

 - 完成lec4的视频学习和提交对应的在线练习
 - git pull ucore_os_lab, v9_cpu, os_course_spoc_exercises in github repos。这样可以在本机上完成课堂练习。
 - 了解x86的保护模式，段选择子，全局描述符，全局描述符表，中断描述符表等概念，以及如何读写，设置等操作
 - 了解Linux中的ELF执行文件格式
 - 了解外设:串口，并口，时钟，键盘,CGA，已经如何对这些外设进行编程
 - 了解x86架构中的mem地址空间和io地址空间
 - 了解x86的中断处理过程（包括硬件部分和软件部分）
 - 了解GCC的x86/RV内联汇编
 - 了解C语言的可函数变参数编程
 - 了解qemu的启动参数的含义
 - 在piazza上就lec3学习中不理解问题进行提问
 - 学会使用 qemu
 - 在linux系统中，看看 /proc/cpuinfo的内容

## 思考题

### 启动顺序

1. x86段寄存器的字段含义和功能有哪些？

   答：

   1. 代码段寄存器CS：存放当前正在运行程序代码所在段的段基地址，表示当前使用的指令代码可以从该段寄存器指定的存储器段中取得，相应的偏移量则由IP提供
   2. 数据段寄存器DS：指出前程序使用的数据所存放段的最低地址，即存放数据段的段基地址
   3. 堆栈段寄存器SS：指出当前堆栈的底部地址，即存放堆栈段的段基地址
   4. 附加段寄存器ES：指出当前程序使用附加数据段的段基地址，该段是串操作指令中目的串所在的段
   5. 附加段寄存器FS
   6. 附加段寄存器GS

2. x86描述符特权级DPL、当前特权级CPL和请求特权级RPL的含义是什么？在哪些寄存器中存在这些字段？对应的访问条件是什么？

   * CPL是当前进程的权限级别，是当前正值执行的代码所在的段的特权级，存在于CS寄存器的低两位

   * RPL说明的是进程对段访问的请求权限，是对于段选择子而言的，每个段选择子有自己的RPL，它说明的是进程对段访问的请求权限，有点像函数参数。而且RPL对每个段来说不是固定的，两次访问同一 段时的RPL可以不同。RPL可能会削弱CPL的作用例如当前CPL=0的进程要访问一个数据段，它把段选择符中的RPL设为3，这样它对该段仍然只有特权为3的访问权限。

   * DPL存储在段描述符中，规定访问该段的权限级别，每个段的DPL固定。当进程访问一个段时，需要进程特权级检查，一般要求DPL>=max{CPL,RPL}

   * 对数据段和堆栈段访问时的特权级控制：

     ​	要求访问数据段或堆栈段的程序的CPL<=待访问的数据段或堆栈段的DPL，同时选择子的RPL<=待访问的数据段或堆栈段的DPL，即程序访问数据段或堆栈段要遵循一个准则：只有相同或更高特权级的代码才能访问相应的数据段。这里，RPL可能会削弱CPL的作用，访问数据段或堆栈段时，默认用CPU和RPL中的最小特权级去访问数据段，所以max{CPL,RPL}<=DPL,否则访问失败

     

3. 分析可执行文件格式elf的格式（无需回答）

### 4.1 C函数调用的实现

### 4.2 x86中断处理过程

1. x86/RV中断处理中硬件压栈内容？用户态中断和内核态中断的硬件压栈有什么不同？

   硬件中断处理过程：

   起始：从CPU收到中断时间后，打断当前程序或任务的执行，根据某种机制跳转到终端服务例程去执行的过程。其具体流程如下：

   * CPU根据得到的中断向量到IDT中找到该向量对应的中断描述符，中断描述符里保存着中断服务例程的段选择子
   * CPU使用IDT查到的中断服务例程的段选择子从GDT中取得相应的段描述符，段描述符里保存着中断服务例程的段基地址和属性信息，此时CPU就得到了中断服务例程的起始地址，并跳转到该地着
   * CPU会根据CPL和中断服务例程的段描述符的DPL信息query是否发生了特权级的转换，这时CPU会从的那个钱的程序的TSS信息里取得该程序的内核低着，即包括内核态的SS和ESP的值，并立即将系统当前使用的栈切换成型的内核栈。这个栈就是即将运行的中断服务程序所使用的栈。紧接着就将当前程序使用的用户态的ss和esp压到新的内和站中保存起来。
   * CPU需要开始保存当前被打断的程序的现场，以便于将来恢复被打断的程序继续执行。这需要利用内和站来保存相关现场信息，即一次雅茹当前被打断程序使用的eflags，cs，eip,errorCode信息
   * Cpu利用中断服务例程的段描述符将其第一条指令的低着加载到cs和eip寄存器中，开始执行中断服务例程。这意味着先前的程序被暂停执行，中断服务程序正是开始工作

   结束：每个中断服务例程在有中断处理工作完成后需要通过iret指令恢复被打断的程序的执行。CPU执行IRET指令的具体过程如下

   * 程序执行这条iret指令时，首先会从内和站里探出先前保存的被打断的程序的现场信息，即eflags,cs,eip重新开始执行
   * 如果存在特权级转换，则还需要从内和站中探出用户态栈的ss和esp这样也意味着栈也被切换回原来使用的用户态的栈了
   * 如果此次处理的是带有错误码的异常，cpu栈回去先前程序的现场时，并不会探出errorCode.这一步需要通过软件完成，即要求相关的中断服务例程栈调用iret妇女会之前添加出栈代码主动探出errorCode

   用户态压栈和内核态压栈决定是否需要特权级改变，并且操作的栈不同。

2. 为什么在用户态的中断响应要使用内核堆栈？

   答：
   保护中断服务例程代码安全

3. x86中trap类型的中断门与interrupt类型的中断门有啥设置上的差别？如果在设置中断门上不做区分，会有什么可能的后果?

   答：

   * 调用Interrupt Gate时，Interrupt会被CPU自动禁止
   * 调用Trap Gate时，CPU不会去禁止或打开中断，而是保留它原来的样子
   * 如果在设置上不做区分，会导致重复触发中断

### 4.3 练习四和五 ucore内核映像加载和函数调用栈分析

1. ucore中，在kdebug.c文件中用到的函数`read_ebp`是内联的，而函数`read_eip`不是内联的。为什么要设计成这样？
   * ebp可以直接获得，若不内敛则会得到错误的ebp值
   * 而由于没有直接获取eip值的指令，我们需要利用call指令将eip鸭掌的特性，通过调用read_eip函数来读出鸭掌上的eip的值。若将read_eip内联，则不会有函数调用存在，无法获得eip的值

### 4.4 练习六 完善中断初始化和处理

1. CPU加电初始化后中断是使能的吗？为什么？

   不是，CPU启动后，BIOS会再POST自检完成后再内存中建立中断向量表和中断服务程序

## 开放思考题

1. 在ucore/rcore中如何修改lab1, 实现在出现除零异常时显示一个字符串的异常服务例程？
2. 在ucore lab1/bin目录下，通过`objcopy -O binary kernel kernel.bin`可以把elf格式的ucore kernel转变成体积更小巧的binary格式的ucore kernel。为此，需要如何修改lab1的bootloader, 能够实现正确加载binary格式的ucore OS？ (hard)
3. GRUB是一个通用的x86 bootloader，被用于加载多种操作系统。如果放弃lab1的bootloader，采用GRUB来加载ucore OS，请问需要如何修改lab1, 能够实现此需求？ (hard)
4. 如果没有中断，操作系统设计会有哪些问题或困难？在这种情况下，能否完成对外设驱动和对进程的切换等操作系统核心功能？

## 课堂实践
### 练习一
在Linux系统的应用程序中写一个函数print_stackframe()，用于获取当前位置的函数调用栈信息。实现如下一种或多种功能：函数入口地址、函数名信息、参数调用参数信息、返回值信息。

### 练习二
在ucore/rcore内核中写一个函数print_stackframe()，用于获取当前位置的函数调用栈信息。实现如下一种或多种功能：函数入口地址、函数名信息、参数调用参数信息、返回值信息。
