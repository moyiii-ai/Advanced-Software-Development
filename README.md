# 高级软件开发 小组Lab：简易Markdown编辑器

## 0. 运行方法



## 1. 设计

Line：储存和编辑文件的基本单元，即一行。不同类型的Line有不同类型的打印格式，因此使用Strategy模式。

LineList：用链表来存储整个文件，通过python的装饰器实现Singleton模式，同时是Composite模式。

Adapter：使用Adapter模式，将Command转化为LineList可以直接处理的形式，并递交LineList进行处理。

Command：一个指令

CommandQueue：使用Command模式，用队列来存储所有Command



## 2. 测试结果



## 3. 讨论

Iterator模式 为什么不用 麻烦+遍历方式不太会改变

## 4. 小组分工

结构设计，撰写文档，代码复核：徐怡然，孙若诗

代码实现：曹丝露，刘高志

编写测试脚本，测试用例：万瑞

文档复核，PPT制作和展示：顾轩



