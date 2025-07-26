# 示例拓展功能模块
# Pic_Collector拓展功能模块
# efm_interactive_interface.py

from constants import *


EFM_NAME = "示例拓展功能模块"

def interactive_interface(warehouse_keeper):
    print("---\n" + EFM_NAME + "\n---")
    with open(
        EXPANSION_FUNCTION_MODULE_FOLDER_PATH
        + "/"
        + EFM_NAME
        + "/introduction_info.txt",
        "r",
        encoding="utf-8",
    ) as f:
        f.readline()
        f.readline()
        f.readline()
        version = f.readline()[:-1].split("：")[1]
        f.readline()
        f.readline()
        applicable_Pic_Collector_versions_str = f.readline()[:-1]
        f.readline()
        simple_introduction_info = f.readline()[:-1]
        f.readline()
        detailed_introduction_info = ""
        while True:
            info_line = f.readline()[:-1]
            if info_line == "":
                break
            else:
                detailed_introduction_info += info_line + "\n"
        detailed_introduction_info = detailed_introduction_info[:-1]
        developer = f.readline()[:-1].split("：")[1]
        version_completion_date = f.readline()[:-1].split("：")[1]
    print("本拓展功能模块版本：" + version)
    print("欢迎使用")
    print()
    while True:
        print("---示例拓展功能模块菜单---")
        print("A.查看本拓展模块信息")
        print("B.退出本拓展模块")
        user_input = input("请输入：")
        print()

        if user_input == "":
            print("您没有输入任何内容，请您重新输入。")

        elif user_input[0] == "A" or user_input[0] == "a":
            print("--本拓展模块信息--")
            print("名称：" + EFM_NAME)
            print("版本号：" + version)
            print("适用的Pic_Collector版本：" + applicable_Pic_Collector_versions_str)
            print()
            print("简单介绍：")
            print(simple_introduction_info)
            print()
            print("详细介绍：")
            print(detailed_introduction_info)
            print()
            print("开发者：" + developer)
            print("此版本拓展功能模块开发完成时间：" + version_completion_date)
            print()
            while True:
                print("A.返回示例拓展功能模块菜单")
                user_input = input("请输入：")
                print()
                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")
                elif user_input[0] == "A" or user_input[0] == "a":
                    break
                else:
                    print("本程序未能理解您的输入，请您重新输入。")

        elif user_input[0] == "B" or user_input[0] == "b":
            break

        else:
            print("本程序未能理解您的输入，请您重新输入。")
