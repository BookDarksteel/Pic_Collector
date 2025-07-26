# Pic_Collector

**v 1.2.0r | Python源代码版 | Github开源版**

Pic_Collector是一个用于管理图片及其信息的应用程序。

Pic_Collector能够管理您的图片以及与图片相关的信息，它提供对图片编号、管理图片信息、简单的搜索等实用功能。能够通过标签管理图片是Pic_Collector的一个值得一提的功能。

此版本Pic_Collector开发完成日期：2025年7月26日  
开发者：BookDarksteel

## 如何开始使用Pic_Collector

只需将Pic_Collector项目的所有文件保存到一个文件夹中，然后运行其中的 *mian.py* 。

## 关于运行环境

Pic_Collector的开发与测试均在Windows 11操作系统下进行，使用的Python解释器版本为3.10。

Pic_Collector使用了如下Python库，这些库都是比较常见的，其中对msvcrt库的使用可能对Pic_Collector的兼容性有较大的影响。

- atexit
- copy
- msvcrt
- os
- random
- shutil
- sys
- time

很抱歉，由于Pic_Collector的开发者知识的匮乏以及测试条件的有限，这里无法给出更多的关于兼容性的信息。

## 关于交互界面

很遗憾地，目前Pic_Collector没有图形化的交互界面，但Pic_Collector的开发者努力开发了比较友好地命令行交互功能。

尽管本 *readme.md* 中包含中文和英文对Pic_Collector的介绍，但目前Pic_Collector的命令行交互功能仅支持主要采用中文的提示信息，您可能需要能够阅读简单的中文才能比较容易地使用Pic_Collector。

## 关于保存图片信息的方式

尽管用数据库管理图片信息是一个非常好的主意，但目前Pic_Collector还是使用了文本文件来保存图片信息，这样做有多方面的原因，包括在仅有基础的文件管理程序和文本编辑器的情况下也能访问或编辑Pic_Collector的图片仓库、Pic_Collector的轻量化、开发人员的技能水平等。

## 关于Pic_Collector拓展功能

自1.2.0r版本开始，Pic_Collector支持通过拓展功能模块扩展功能，Pic_Collector中有关于如何使用拓展功能模块的信息。使用拓展功能模块时请注意拓展功能模块适用的Pic_Collector版本。

目前本项目不提供有实质拓展功能的拓展功能模块，但在 *expansion_function_modules_not_installed* 文件夹中提供了一个示例拓展功能模块，其可以用于测试Pic_Collector的关于拓展功能的部分，以及帮助想要开发Pic_Collector的拓展功能模块却不知道怎样做的人更快地理解如何开发Pic_Collector的拓展功能模块。需要注意的是Pic_Collector并不能直接加载 *expansion_function_modules_not_installed* 文件夹中的拓展功能模块，需要按照Pic_Collector中的相关提示信息将拓展功能模块文件存入指定文件夹后Pic_Collector才能加载拓展功能模块。

## 关于Pic_Collector之粗陋的说明

需要说明的是，Pic_Collector是BookDarksteel基于兴趣爱好，出于学习、练习编程技术为目的，在业余时间开发的应用程序。受限于BookDarksteel开发Pic_Collector时的技术水平以及拥有的资源，Pic_Collector的设计、开发、测试等工作都进行得比较粗糙且不够专业。使用或研究Pic_Collector时请充分考虑其粗陋可能会带来麻烦与风险。

强烈建议在使用Pic_Collector时将其会处理的信息进行备份以防程序错误或操作意外带来的损失。

## 更新日志
- v 1.2.0r  
支持通过拓展功能模块扩展功能；  
提供了示例拓展功能模块；  
修正了导入图片时不输入标签会导致图片信息异常的错误和图片没有标签时导出的图片信息存在异常的错误；  
优化了少许提示信息。
- v 1.1.1r  
调整了部分代码的格式。
- v 1.1.0r  
增加了按标签搜索的功能；  
修正了关于按普通字段和文件名搜索功能的一些错误。
- v 1.0.1r  
修正了程序开始运行时版本号显示错误的错误；  
提供了.gitignore文件；  
修正了readme.md中的一些错误。
- v 1.0.0r  
Pic_Collector的第一个开源版本。

---

# Pic_Collector

**v 1.2.0r | Python source code edition | Github open source edition**

Pic_Collector is an application for managing pictures and their information.

Pic_Collector is able to manage your pictures and the information related to them, it provides useful functions such as numbering pictures, managing picture information, simple searching and so on. The ability to manage images by tags is a noteworthy feature of Pic_Collector.

Development completion date for this version of Pic_Collector: July 26, 2025  
Developer: BookDarksteel

## How to get started with Pic_Collector

Simply save all the files of the Pic_Collector project to a folder and run *mian.py* from it.

## About the running environment

Pic_Collector was developed and tested under the Windows 11 operating system, using Python interpreter version 3.10.

Pic_Collector uses the following Python libraries, which are relatively common. The use of the msvcrt library may have a large impact on the compatibility of Pic_Collector.

- atexit
- copy
- msvcrt
- os
- random
- shutil
- sys
- time

Apologies that due to the lack of knowledge of the developers of Pic_Collector and the limited testing conditions, it is unable to give more information about compatibility here.

## About the interactive interface

Unfortunately, Pic_Collector does not currently have a graphical interaction interface. However, the developers of Pic_Collector have worked hard to develop a relatively user-friendly command line interaction.

Although this *readme.md* contains an introduction to Pic_Collector in both Chinese and English, Pic_Collector's command line interaction currently only supports prompts that are primarily in Chinese, and you may need to be able to read simple Chinese in order to use Pic_Collector easily.

## About the way to save the information of the pictures

Although managing information about pictures with a database is a very good idea, Pic_Collector currently uses text files to store information about pictures. There are multiple reasons for this, including the availability of access to or editing of Pic_Collector's pictures repository even with only a basic file manager and text editor, Pic_Collector's lightweighting, the skill level of the developer, and so on.

## About Pic_Collector's expansion functions

Since version 1.2.0, Pic_Collector supports expansion functions via expansion function modules. Pic_Collector has information on how to use expansion function modules. Please note the version of Pic_Collector to which the expansion function module applies when using the expansion function modules.

Currently, this project does not provide expansion function modules with substantial expansion functions. However, a sample expansion function module is provided in the *expansion_function_modules_not_installed* folder. It can be used to test Pic_Collector's parts about expansion functions, as well as to help people who want to develop Pic_Collector's expansion function modules but don't know how to do so to understand how to develop Pic_Collector's expansion function modules more quickly. Note that Pic_Collector does not directly load expansion function modules in the *expansion_function_modules_not_installed* folder. You need to follow the relevant hint messages in Pic_Collector to save the expansion function module files into the specified folder before Pic_Collector can load the expansion function module.

## Pic_Collector is rough

It should be pointed out that Pic_Collector is an application developed by BookDarksteel in his spare time for the purpose of learning and practicing programming skills based on his hobby. The design, development and testing of Pic_Collector are rough and unprofessional due to BookDarksteel's technical level and resources available at the time of developing Pic_Collector. When using or study Pic_Collector, please take into consideration that the roughness of Pic_Collector may bring troubles and risks.

It is strongly recommended to make a backup of the information that Pic_Collector will process when using it in order to prevent losses caused by program errors or operational accidents.

## Update log
- v 1.2.0r  
Expanded functions through expansion function modules are supported;  
Sample expansion function module is provided;  
Fixed the bug that importing pictures without inputting tags resulted in abnormal picture information, and the bug that there was an abnormality in the exported picture information when the picture had no tags;  
Optimized a few hint messages.
- v 1.1.1r  
Adjusted the formatting of some codes.
- v 1.1.0r  
Added the function of searching by tags;  
Fixed some bugs about the function of searching by common fields and filenames.
- v 1.0.1r  
Fixed a bug where the version number was displayed incorrectly when the program started running;  
The .gitignore file is provided;  
Fixed some bugs in readme.md.
- v 1.0.0r  
The first open source version of Pic_Collector.

---
