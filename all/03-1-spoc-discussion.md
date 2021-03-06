# lec5: SPOC思考题

##**提前准备**
（请在上课前完成）

- 完成lec５的视频学习和提交对应的在线练习
- git pull ucore_os_lab, v9_cpu, os_course_spoc_exercises in github repos。这样可以在本机上完成课堂练习。
- 理解连续内存动态分配算法的实现（主要自学和网上查找）

NOTICE
- 有"hard"标记的题有一定难度，鼓励实现。
- 有"easy"标记的题很容易实现，鼓励实现。
- 有"midd"标记的题是一般水平，鼓励实现。


## 思考题
---

## “连续内存分配”与视频相关的课堂练习

### 5.1 计算机体系结构和内存层次

1.操作系统中存储管理的目标是什么？

* 抽象
* 保护
* 共享
* 虚拟化


### 5.2 地址空间和地址生成
1.描述编译、汇编、链接和加载的过程是什么？

* 编译：将程序源代码转换为汇编代码

  ​	编译是指编译器读取字符流的圆程序，对其进行词法于语法的分析，将高级语言指令转换为功能等效的汇编代码

  编译主要分为两个过程：预处理过程、编译过程

  * 预处理过程：

    预处理过程将.c文件转换为.i文件，当编译器为gcc时，使用的命令是gcc -E。预处理过程，主要是以下几部分

    * 宏定义指令
    * 条件编译指令
    * 头文件包含指令
    * 特殊符号

  * 编译过程

    编译是把预处理完的文件进行一系列的词法分析，语法分析，语义分析及优化后生成相应的汇编代码

* 汇编：将汇编代码转为二进制的机器码

  ​	汇编器是将汇编代码转变成机器可以执行的命令，每一个汇编语句几乎都对应一条机器指令。汇编相对于编译过程比较简单，根据汇编指令和机器指令的对照表一一翻译即可

  汇编生成的目标文件中，存放的 是源程序等效的机器语言代码。生成的目标文件由段组成，通常至少有两个段：

  * 代码段：该段中包含的是程序指令。该段一般可读可执行，但一般不可写
  * 数据段：主要存放程序中用到的各种全局变量或静态数据，一般数据段都是可读，可写，可执行的

* 链接：将多个二进制的机器码结合成一个可执行环境

  ​	链接的主要工作是把各个模块之间相互引用的部分处理好，使各个模块之间可以正确衔接。

  链接的作用，一方面在于是的分离编译称为可能；另一方面在于动态绑定实现，即定义、四号线、使用分离

* 加载：将程序从外存中加载到内存中

  ​	加载器将可执行文件从外村加载到内存中，并执行。加载过程如下：

  加载器受限创建内存影响。Linux进程运行时的内存映象如下：

  根据上面的内存映象，加载器跳转到程序入口点，执行启动代码。

  在执行玩初始化话任务，即init之后，启动代码滴哦啊用atexit例程，该例程注册了一系列调用exit函数时必须的你吃了个。随后，启动代码调用应用程序的main例程，执行用户程序代码。当用户程序代码返回后，启动代码调用_exit例程，将控制权交还给操作系统。

2.动态链接如何使用？尝试在Linux平台上使用LD_DEBUG查看一个C语言Hello world的启动流程。  (optional)



### 5.3 连续内存分配
1.什么是内碎片、外碎片？

* 内碎片：分配给任务的内存大小比任务所要求的大小所多出来的内存。
* 外碎片：只分配给任务的内存之间无法利用的内存

2.最先匹配会越用越慢吗？请说明理由（可来源于猜想或具体的实验）？

​	会。最先匹配总是有限找低地址空间的内存，在低地址空间容易使用的地址都分配出去之后，往往需要查找到高地址才能分配，因而会越来越慢

3.最差匹配的外碎片会比最优适配算法少吗？请说明理由（可来源于猜想或具体的实验）？

​	会。因为最差匹配总是先找最大的内存快进行分割，这样剩下来的内存还比较大，往往还可以装下其他程序，因而会减少外碎片的产生。

4.理解0:最优匹配，1:最差匹配，2:最先匹配，3:buddy systemm算法中分区释放后的合并处理过程？ (optional)

​	查看边上是否有空闲块，如果有，则合并空闲块，然后将空闲快管理数据插入链表中。


### 5.4 碎片整理
1.对换和紧凑都是碎片整理技术，它们的主要区别是什么？为什么在早期的操作系统中采用对换技术？  

​	答：

​	紧凑是在内存中搬动进程占用的内存位置，以合并出更大的内存空闲块。

​	对换是把内存中的进程搬到外存中，以空出更多的内存空闲块。

​	早期由于内存容量小，计算机结构没有这么复杂，用对换处理简单。	

2.一个处于等待状态的进程被对换到外存（对换等待状态）后，等待事件出现了。操作系统需要如何响应？

​	将进程从硬盘中读取到内存中，在这个过程中，操作系统将该进程标为等待状态并且调度其他进程。

### 5.5 伙伴系统
1.伙伴系统的空闲块如何组织？

​	按照内存的大小有一系列链表组织，类似于哈希表，将相同大小的内存区域首地址连接起来

2.伙伴系统的内存分配流程？伙伴系统的内存回收流程？

* 内存分配流程

  当向内核请求分配[2^（i-1),2^i]数码的页块时，按照2^i页块请求处理。如果对应的块链表中没有空闲页块，则在更大的页块链表中查找。当分配的页块中有多余的页时，伙伴系统根据多余的页框大小插入到对应的空闲页块链表中

  

* 内存回收流程

  当释放多页的块时，内核受限计算出该内存快的伙伴地址。内核将满足一下条件的三个块称为伙伴

  １.两个块具有相同的大小，记作ｂ

  ２.它们的物理地址是连续的

  ３.第一块的第一个页的物理地址是２×（２＾ｂ）的倍数。

  如果找到了该内存快的伙伴

## 课堂实践

观察最先匹配、最佳匹配和最差匹配这几种动态分区分配算法的工作过程，并选择一个例子进行分析分析整个工作过程中的分配和释放操作对维护数据结构的影响和原因。

  * [算法演示脚本的使用说明](https://github.com/chyyuu/os_tutorial_lab/blob/master/ostep/ostep3-malloc.md)
  * [算法演示脚本](https://github.com/chyyuu/os_tutorial_lab/blob/master/ostep/ostep3-malloc.py)

例如：
```
python ./ostep3-malloc.py -S 100 -b 1000 -H 4 -a 4 -l ADDRSORT -p BEST -n 5 -c
python ./ostep3-malloc.py -S 100 -b 1000 -H 4 -a 4 -l ADDRSORT -p FIRST -n 5 -c
python ./ostep3-malloc.py -S 100 -b 1000 -H 4 -a 4 -l ADDRSORT -p WORST -n 5 -c
```

### 扩展思考题 (optional)

1. 请参考xv6（umalloc.c），ucore lab2代码，选择四种（0:最优匹配，1:最差匹配，2:最先匹配，3:buddy systemm）分配算法中的一种或多种，在Linux应用程序/库层面，用C、C++或python来实现malloc/free，给出你的设计思路，并给出可以在Linux上运行的malloc/free实现和测试用例。


2. 阅读[slab分配算法](http://en.wikipedia.org/wiki/Slab_allocation)，尝试在应用程序中实现slab分配算法，给出设计方案和测试用例。
