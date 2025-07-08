# Pic_Collector
# mian.py

import atexit
import msvcrt
import os
import random
import shutil
import sys
import time

from constants import *
from InteractiveInterface import *
from PicWarehouseKeeper import PicWarehouseKeeper


build_file_lock = False

@atexit.register
def exit_pic_collector():
    if build_file_lock:
        os.remove(PROGRAM_SINGLE_INSTANCE_LOCK_FILE_PATH)

def copy_pics(pic_ids):
    """
    复制图片功能交互函数
    提供检测、创建、整理复制目标文件夹的功能并调用warehouse_keeper的图片复制操作。
    参数：要被复制的图片的编号列表。
    无返回值。
    """
    while True:
        copy_target_folder_path = DEFULT_RESULTS_FOLDER_PATH
        print(
            "请输入您希望复制到的文件夹的路径，或输入“D”或“d”以复制到默认结果复制文件夹（"
            + DEFULT_RESULTS_FOLDER_PATH
            + "）。"
        )
        user_input = input("请输入：")
        print()
        reenter_path = False
        if user_input != "D" and user_input != "d":
            if not (os.path.exists(user_input) and (not os.path.isfile(user_input))):

                while True:
                    print("您输入的文件夹不存在，是否要按照您输入的路径新建文件夹？")
                    print("Y.是")
                    print("N.否")
                    sec_user_input = input("请输入：")
                    print()
                    if user_input == "":
                        print("您没有输入任何内容，请您重新输入。")
                    elif sec_user_input[0] == "Y" or sec_user_input[0] == "y":
                        os.makedirs(user_input)
                        print(
                            STYLE_LOWLIGHT
                            + "已创建文件夹 "
                            + sec_user_input
                            + STYLE_DEFULT
                        )
                        break
                    elif sec_user_input[0] == "N" or sec_user_input[0] == "n":
                        reenter_path = True
                        break
                    else:
                        print("本程序未能理解您的输入，请您重新输入。")

            if reenter_path:
                continue
            else:
                copy_target_folder_path = user_input
                break
        else:
            if not (
                os.path.exists(copy_target_folder_path)
                and (not os.path.isfile(copy_target_folder_path))
            ):

                while True:
                    print("尚未创建默认复制目标文件夹，是否要创建默认复制目标文件夹？")
                    print("默认目标文件夹：" + DEFULT_RESULTS_FOLDER_PATH)
                    print("Y.是")
                    print("N.否")
                    sec_user_input = input("请输入：")
                    print()
                    if user_input == "":
                        print("您没有输入任何内容，请您重新输入。")
                    elif sec_user_input[0] == "Y" or sec_user_input[0] == "y":
                        os.makedirs(DEFULT_RESULTS_FOLDER_PATH)
                        print(
                            STYLE_LOWLIGHT
                            + "已创建文件夹 "
                            + DEFULT_RESULTS_FOLDER_PATH
                            + STYLE_DEFULT
                        )
                        break
                    elif sec_user_input[0] == "N" or sec_user_input[0] == "n":
                        reenter_path = True
                        break
                    else:
                        print("本程序未能理解您的输入，请您重新输入。")

            if reenter_path:
                continue
            else:
                break

    if len(os.listdir(copy_target_folder_path)) != 0:

        while True:
            print("复制目标文件夹中有其他文件，是否删除其他文件？")
            print(
                COLOR_YELLOW
                + "注意：为避免需要保留的数据丢失，请谨慎操作！"
                + STYLE_DEFULT
            )
            print("Y.是")
            print("N.否")
            user_input = input("请输入：")
            print()
            if user_input == "":
                print("您没有输入任何内容，请您重新输入。")
            elif user_input[0] == "Y" or user_input[0] == "y":
                shutil.rmtree(copy_target_folder_path)
                os.mkdir(copy_target_folder_path)
                print(
                    STYLE_LOWLIGHT
                    + "已清空文件夹 "
                    + copy_target_folder_path
                    + STYLE_DEFULT
                )
                break
            elif user_input[0] == "N" or user_input[0] == "n":
                break
            else:
                print("本程序未能理解您的输入，请您重新输入。")

    warehouse_keeper.copy_pics(pic_ids, copy_target_folder_path)

def focus_pic(pic_id):
    """
    关注单张图片模式交互函数
    在关注单张图片模式下，可以方便地查看指定的单张图片及其信息，并对该指定的单张图片进行修改信息、导出、删除等操作。
    参数pic_id：指定的单张图片。
    返回值：返回值包括两项，
        前一项描述退出单张图片模式后要进行的操作的字符串，值可能为“返回主菜单”和“关注另一张图片”；
        后一项仅在返回值的前一项值为“关注另一张图片”时有意义，描述要关注的另一张图片的编号。
    """
    pic_info = warehouse_keeper.get_pic_info(pic_id)
    show_pic_info(pic_info)
    while True:
        print(
            "请按照以下信息选择您希望进行的操作，或者输入图片索引以查看其他图片的详细信息或对其他图片进行操作。"
        )
        print("A.打开该图片（以操作系统默认方式）")
        print("B.复制该图片到...")
        print("C.修改图片信息")
        print("D.删除图片")
        print("E.返回主菜单")
        user_input = input("请输入：")
        print()
        if user_input == "":
            print("您没有输入任何内容，请您重新输入。")
        elif user_input[0] == "A" or user_input[0] == "a":
            os.startfile(PIC_FOLDER_PATH + "\\" + pic_info[1]["文件名"])
            print(STYLE_LOWLIGHT + "成功以操作系统默认方式打开图片" + STYLE_DEFULT)
        elif user_input[0] == "B" or user_input[0] == "b":
            copy_pics([pic_id])
        elif user_input[0] == "C" or user_input[0] == "c":

            while True:
                print("请输入您希望进行的图片信息修改操作")
                print("A.修改单个字段信息")
                print("B.增加标签")
                print("C.删除标签")
                print("D.重新输入图片信息")
                print("E.返回上一级")
                user_input = input("请输入：")
                print()

                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")

                elif user_input[0] == "A" or user_input[0] == "a":
                    print(
                        "请输入您要修改的字段名称，您将重新输入该字段的信息以取代旧信息，"
                    )
                    print("支持修改图片的普通字段信息、备注字段信息和标签信息。")
                    user_input = input("请输入：")
                    print()
                    user_defined_ordinary_fields = (
                        warehouse_keeper.get_user_defined_ordinary_fields()
                    )
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    if user_input in user_defined_ordinary_fields:
                        modify_info_field = user_input
                        print(
                            "-您将要修改编号为"
                            + str(pic_id)
                            + "的图片的 "
                            + modify_info_field
                            + " 字段-"
                        )
                        print("该信息当前为：" + pic_info[1][modify_info_field])
                        pic_info[1][modify_info_field] = input("将该信息改为：")
                        print()
                        warehouse_keeper.modify_pic_info(pic_id, pic_info[1])
                        pic_info = warehouse_keeper.get_pic_info(pic_id)
                        show_pic_info(pic_info)
                        break
                    elif user_input == "标签":
                        print("-您将要修改编号为" + str(pic_id) + "的图片的 标签 字段-")
                        tags_str = ""
                        for tag in pic_info[1]["标签"]:
                            tags_str += tag + INLINE_INFO_SEPARATOR
                        print("该图片的标签信息当前为：" + tags_str[:-1])
                        print(
                            "请重新输入该图片的标签信息，标签之间使用“"
                            + INLINE_INFO_SEPARATOR
                            + "”分隔。"
                        )
                        print("您需要输入修改后该图片的所有标签字段。")
                        user_input = input("请输入：")
                        print()
                        raw_new_pic_tags = user_input.split(INLINE_INFO_SEPARATOR)
                        num_raw_new_pic_tags = len(raw_new_pic_tags)
                        new_pic_tags = sorted(
                            set(raw_new_pic_tags), key=raw_new_pic_tags.index
                        )
                        if len(new_pic_tags) != num_raw_new_pic_tags:
                            print(
                                COLOR_YELLOW
                                + "【提示】您输入的标签存在重复，重复的标签将仅保留一个。"
                                + STYLE_DEFULT
                            )
                        if "" in new_pic_tags:
                            new_pic_tags.remove("")
                        pic_info[1]["标签"] = new_pic_tags
                        warehouse_keeper.modify_pic_info(pic_id, pic_info[1])
                        pic_info = warehouse_keeper.get_pic_info(pic_id)
                        show_pic_info(pic_info)
                        break
                    elif user_input in user_defined_comment_fields:
                        modify_info_field = user_input
                        print(
                            "-您将要修改编号为"
                            + str(pic_id)
                            + "的图片的 "
                            + modify_info_field
                            + " 字段-"
                        )
                        print("该信息当前为：")
                        print(pic_info[1][modify_info_field])
                        while True:
                            num_comment_line = 0
                            user_input = input(
                                "请输入该图片的新" + modify_info_field + "信息行数："
                            )
                            if user_input.isdigit():
                                num_comment_line = int(user_input)
                                if num_comment_line >= 0:
                                    break
                                else:
                                    print(
                                        "图片的"
                                        + field
                                        + "信息行数应大于等于零，请您重新输入。"
                                    )
                            else:
                                print("本程序未能理解您的输入，请您重新输入。")
                        comment = ""
                        for line_i in range(num_comment_line):
                            user_input = input(
                                "请输入第"
                                + str(line_i + 1)
                                + "行该图片的"
                                + field
                                + "信息："
                            )
                            comment += user_input + "\n"
                        print()
                        pic_info[1][modify_info_field] = comment[:-1]
                        warehouse_keeper.modify_pic_info(pic_id, pic_info[1])
                        pic_info = warehouse_keeper.get_pic_info(pic_id)
                        show_pic_info(pic_info)
                        break
                    else:
                        print("您输入的字段不存在。")

                elif user_input[0] == "B" or user_input[0] == "b":
                    print("-为编号为" + str(pic_id) + "的图片的增加标签-")
                    tags_str = ""
                    for tag in pic_info[1]["标签"]:
                        tags_str += tag + INLINE_INFO_SEPARATOR
                    print("该图片的标签信息当前为：" + tags_str[:-1])
                    print(
                        "输入多个标签时标签之间使用“"
                        + INLINE_INFO_SEPARATOR
                        + "”分隔。"
                    )
                    user_input = input("请输入您希望增加的标签：")
                    print()
                    raw_new_pic_tags = (tags_str + user_input).split(
                        INLINE_INFO_SEPARATOR
                    )
                    num_raw_new_pic_tags = len(raw_new_pic_tags)
                    new_pic_tags = sorted(
                        set(raw_new_pic_tags), key=raw_new_pic_tags.index
                    )
                    if len(new_pic_tags) != num_raw_new_pic_tags:
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的标签存在重复或与已有的标签重复，重复的标签将仅保留一个。"
                            + STYLE_DEFULT
                        )
                    if "" in new_pic_tags:
                        new_pic_tags.remove("")
                    pic_info[1]["标签"] = new_pic_tags
                    warehouse_keeper.modify_pic_info(pic_id, pic_info[1])
                    pic_info = warehouse_keeper.get_pic_info(pic_id)
                    show_pic_info(pic_info)
                    break

                elif user_input[0] == "C" or user_input[0] == "c":
                    print("-为编号为" + str(pic_id) + "的图片的删除标签-")
                    tags_str = ""
                    for tag in pic_info[1]["标签"]:
                        tags_str += tag + INLINE_INFO_SEPARATOR
                    print("该图片的标签信息当前为：" + tags_str[:-1])
                    print(
                        "输入多个标签时标签之间使用“"
                        + INLINE_INFO_SEPARATOR
                        + "”分隔。"
                    )
                    user_input = input("请输入您希望删除的标签：")
                    print()
                    raw_del_pic_tags = user_input.split(INLINE_INFO_SEPARATOR)
                    del_pic_tags = sorted(
                        set(raw_del_pic_tags), key=raw_del_pic_tags.index
                    )
                    if "" in del_pic_tags:
                        del_pic_tags.remove("")
                    for del_tag in del_pic_tags:
                        if del_tag in pic_info[1]["标签"]:
                            pic_info[1]["标签"].remove(del_tag)
                        else:
                            print(
                                COLOR_YELLOW
                                + "【提示】该图片原来并没有您希望删除的 "
                                + del_tag
                                + " 标签"
                                + STYLE_DEFULT
                            )
                    warehouse_keeper.modify_pic_info(pic_id, pic_info[1])
                    pic_info = warehouse_keeper.get_pic_info(pic_id)
                    show_pic_info(pic_info)
                    break

                elif user_input[0] == "D" or user_input[0] == "d":
                    print("-重新输入图片编号为" + str(pic_id) + "的图片的信息-")
                    user_defined_ordinary_fields = (
                        warehouse_keeper.get_user_defined_ordinary_fields()
                    )
                    for field in user_defined_ordinary_fields:
                        user_input = input("请输入该图片的" + field + "：")
                        pic_info[1][field] = user_input
                    print(
                        "请输入该图片的标签，标签之间使用“"
                        + INLINE_INFO_SEPARATOR
                        + "”分隔。"
                    )
                    user_input = input("请输入：")
                    raw_new_pic_tags = user_input.split(INLINE_INFO_SEPARATOR)
                    num_raw_new_pic_tags = len(raw_new_pic_tags)
                    new_pic_tags = sorted(
                        set(raw_new_pic_tags), key=raw_new_pic_tags.index
                    )
                    if len(new_pic_tags) != num_raw_new_pic_tags:
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的标签存在重复，重复的标签将仅保留一个。"
                            + STYLE_DEFULT
                        )
                    if "" in new_pic_tags:
                        new_pic_tags.remove("")
                    pic_info[1]["标签"] = new_pic_tags
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    for field in user_defined_comment_fields:
                        while True:
                            num_comment_line = 0
                            user_input = input("请输入该图片的" + field + "信息行数：")
                            if user_input.isdigit():
                                num_comment_line = int(user_input)
                                if num_comment_line >= 0:
                                    break
                                else:
                                    print(
                                        "图片的"
                                        + field
                                        + "信息行数应大于等于零，请您重新输入。"
                                    )
                            else:
                                print("本程序未能理解您的输入，请您重新输入。")
                        comment = ""
                        for line_i in range(num_comment_line):
                            user_input = input(
                                "请输入第"
                                + str(line_i + 1)
                                + "行该图片的"
                                + field
                                + "信息："
                            )
                            comment += user_input + "\n"
                        pic_info[1][field] = comment[:-1]
                    print()
                    warehouse_keeper.modify_pic_info(pic_id, pic_info[1])
                    pic_info = warehouse_keeper.get_pic_info(pic_id)
                    show_pic_info(pic_info)
                    break

                elif user_input[0] == "E" or user_input[0] == "e":
                    show_pic_info(pic_info)
                    break

                else:
                    print("本程序未能理解您的输入，请您重新输入。")

        elif user_input[0] == "D" or user_input[0] == "d":

            print("-删除图片编号为" + str(pic_id) + "的图片-")
            while True:
                print(
                    "您确定要删除编号为"
                    + str(pic_id)
                    + "的图片吗？删除后将无法找回图片及其信息。"
                )
                print("Y.是")
                print("N.否")
                user_input = input("请输入：")
                print()
                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")
                elif user_input[0] == "Y" or user_input[0] == "y":
                    warehouse_keeper.delete_pic(pic_id)
                    return "返回主菜单", -1  # 返回
                elif user_input[0] == "N" or user_input[0] == "n":
                    break
                else:
                    print("本程序未能理解您的输入，请您重新输入。")

        elif user_input[0] == "E" or user_input[0] == "e":
            return "返回主菜单", -1
        elif user_input.isdigit():
            return "关注另一张图片", int(user_input)
        else:
            print("本程序未能理解您的输入，请您重新输入。")

def print_about_info():
    """
    输出关于信息
    无返回值。
    """
    print("Pic_Collector")
    print("v 1.1.1r")
    print("Pic_Collector是一个用于管理图片及其信息的应用程序。")
    print()
    print("此版本Pic_Collector开发完成日期：2025年7月8日")
    print("开发者：BookDarksteel")


def print_import_pic_info_norm():
    """
    输出导入图片信息文本文件书写规范
    无返回值。
    """
    print("-导入图片信息文本文件书写规范-")
    print("导入图片信息文本文件应为采用utf-8编码的txt文件。")
    print("文件内容应从第1行开始编写描述第1张图片的文本段，在内容开头不要留有空行。")
    print("对于描述每张图片的文本段：")
    print(
        "\t第1行为图片的标识符，可以任意编写但不允许为空，由于文件导入图片仓库后会分配编号，所以这个标识符不会被记录；"
    )
    print(
        "\t第2行描述图片的文件名，应先编写“文件名：”，后接图片的文件名，注意这里的文件名应为从导入的图片所在的文件夹开始的相对路径，且需要包含后缀名；"
    )
    print(
        "\t之后数行描述图片的普通字段信息，每行应先编写普通字段名称，后接“：”,再后接图片的该字段信息，普通字段信息的出现顺序任意，若某些普通字段信息没有被描述，则导入后该图片的该普通字段信息记录为空字符串；"
    )
    print(
        "\t之后的一行描述图片的标签信息，应先编写“标签：”，后接该图片的标签，标签之间用“"
        + INLINE_INFO_SEPARATOR
        + "”分隔；"
    )
    print("\t之后数行描述图片的备注字段信息，对于每个备注字段信息的描述：")
    print("\t\t首先编写备注字段名称，后接“：”，再后接备注字段的备注信息的行数，")
    print(
        "\t\t然后在改行的下一行开始编写备注字段的备注信息，遇到备注信息中的换行自动换行，但注意备注信息的总行数不允许超过该备注字段信息的描述的第1行标明的备注信息行数。"
    )
    print(
        "\t\t若备注信息为空，则在备注字段信息的描述的第1行标明备注信息行数为0即可，之后的下一行继续输入后续信息即可。"
    )
    print(
        "\t备注字段信息的出现顺序任意，若某些普通字段信息没有被描述，则导入后该图片的该普通字段信息记录为空字符串。"
    )
    print(
        "\t注意虽然在指定的区域内描述普通字段信息的行和描述备注字段信息的行出现顺序任意，但描述普通字段信息的行只允许出现在描述文件名信息的行和描述标签信息的行之间，描述备注字段信息的行只允许出现描述标签信息的行之后,"
    )
    print("\t而且描述每张图片的文本段内不允许出现无意义的空行。")
    print("每个描述一张图片的文本段之间用一个空行分隔。")
    print("---")

def print_update_log():
    print("-更新日志-")
    print("v1.1.1r")
    print("\t调整部分代码格式。")
    print("v1.1.0r")
    print("\t增加了按标签搜索的功能；")
    print("\t修正了关于按普通字段和文件名搜索功能的一些错误。")
    print("v1.0.1r")
    print("\t修正了程序开始运行时版本号显示错误的错误；")
    print("\t提供了.gitignore文件；")
    print("\t修正了readme.md中的一些错误。")
    print("v1.0.0r")
    print("\tPic_Collector的第一个开源版本。")
    print("---")

def show_pic_info(pic_info):
    """
    显示给定的图片信息。
    参数pic_info：给定的图片信息，类型为列表，其中第0项为图片编号，第1项为图片信息字典。
    无返回值。
    """
    print("--编号为" + str(pic_info[0]) + "的图片信息--")
    user_defined_ordinary_fields = warehouse_keeper.get_user_defined_ordinary_fields()
    user_defined_comment_fields = warehouse_keeper.get_user_defined_comment_fields()
    for (
        field
    ) in (
        user_defined_ordinary_fields
    ):  # 这里之所以不直接遍历pic_info[1].keys()是因为这里显示图片信息要按固定的顺序显示。
        print(field + "：" + pic_info[1][field])
    tags_str = ""
    for tag in pic_info[1]["标签"]:
        tags_str += tag + INLINE_INFO_SEPARATOR
    print("标签：" + tags_str[:-1])
    for field in user_defined_comment_fields:
        print(field + "：")
        print(pic_info[1][field])
    print("---")

def show_search_results(results):
    """
    展示给定搜索结果。
    参数results：搜索结果信息，类型为列表，其中每一项对应一个搜索结果且也是一个列表，其中第0项为搜索结果图片的编号，第1项为搜索结果图片的信息字典，第3项目为搜索结果图片的匹配信息。
    无返回值。
    """
    print("---搜索结果---")
    if len(results) == 0:
        print("没有搜索到符合条件的图片")
    else:
        print("搜索到" + str(len(results)) + "幅图片")
        user_defined_ordinary_fields_print_omit = False
        user_defined_ordinary_fields = (
            warehouse_keeper.get_user_defined_ordinary_fields()
        )
        num_user_defined_ordinary_field = len(user_defined_ordinary_fields)
        if num_user_defined_ordinary_field > 3:
            user_defined_ordinary_fields_print_omit = True

        print("编号\t", end="")
        if num_user_defined_ordinary_field > 0:
            print(user_defined_ordinary_fields[0] + "\t", end="")
        if num_user_defined_ordinary_field > 1:
            print(user_defined_ordinary_fields[1] + "\t", end="")
        if num_user_defined_ordinary_field > 2:
            print(user_defined_ordinary_fields[2] + "\t", end="")
        if user_defined_ordinary_fields_print_omit:
            print("...\t", end="")
        print("匹配信息")

        results_print_omit = False
        print_result_count = 0
        for result in results:
            if print_result_count >= 30:
                results_print_omit = True
                print("...")
            print(str(result[0]) + ".\t", end="")
            if num_user_defined_ordinary_field > 0:
                print(result[1][user_defined_ordinary_fields[0]] + "\t", end="")
            if num_user_defined_ordinary_field > 1:
                print(result[1][user_defined_ordinary_fields[1]] + "\t", end="")
            if num_user_defined_ordinary_field > 2:
                print(result[1][user_defined_ordinary_fields[2]] + "\t", end="")
            if user_defined_ordinary_fields_print_omit:
                print("...\t", end="")
            matching_info = result[2]
            print(matching_info[0], end="")
            if len(matching_info) > 1:
                print(INLINE_INFO_SEPARATOR + matching_info[1], end="")
            if len(matching_info) > 2:
                print(INLINE_INFO_SEPARATOR + matching_info[2], end="")
            if len(matching_info) > 3:
                print("...", end="")
            print()
            print_result_count += 1

        if results_print_omit:
            print(
                "由于搜索到的结果太多，将不显示其余搜索结果的详细信息，下面给出所有搜索到的图片的编号："
            )
            print(results[0][0], end="")
            for result in results[1:]:
                print(INLINE_INFO_SEPARATOR + result[0])
    print("---")


if __name__ == "__main__":
    print("-----\nPic_Collector\n-----")
    print("v 1.1.1r")
    print("欢迎使用")
    print("按任意键继续")
    msvcrt.getch()
    print("")

    # 检查在当前工作文件夹下是否有正在运行的其他Pic_Collector实例
    if os.path.exists(PROGRAM_SINGLE_INSTANCE_LOCK_FILE_PATH):
        print(
            COLOR_RED
            + "【错误】当前在该工作文件夹下已经存在一个正在运行的Pic_Collector"
            + STYLE_DEFULT
        )
        print(
            "工作文件夹相同的Pic_Collector只允许有一个正在运行的实例，请使用正在运行的实例或结束正在运行的实例后再启动新Pic_Collector实例。"
        )
        print("按任意键退出")
        msvcrt.getch()
        sys.exit(1)
    else:
        build_file_lock = True
        with open(
            PROGRAM_SINGLE_INSTANCE_LOCK_FILE_PATH, "w", encoding="utf-8"
        ) as lock_file:
            lock_file.write(str(os.getpid()))

    print("=====")
    if not os.path.exists(PIC_WAREHOUSE_INFO_FILE_PATH):

        print("Pic_Collector没有找到已建立的图片仓库，现在建立一个新的图片仓库吧！")
        while True:
            print("现在开始建立一个新的图片仓库？")
            print("Y.好的，现在开始。")
            print("Q.退出程序")

            user_input = input("请输入：")
            print()

            if user_input == "":
                print("您没有输入任何内容，请您重新输入。")
            elif user_input[0] == "Y" or user_input[0] == "y":
                break
            elif user_input[0] == "Q" or user_input[0] == "q":
                sys.exit(0)
            else:
                print("本程序未能理解您的输入，请您重新输入。")

        while not os.path.exists(PIC_WAREHOUSE_INFO_FILE_PATH):
            print("-----")
            while True:
                print("请输入新建的图片仓库的名称：")
                user_input = input()
                print()
                if user_input == "":
                    print("图片仓库名称不能为空。")
                else:
                    break
            pic_warehouse_name = user_input

            print("-----")
            print(
                "请输入图片信息普通字段名称，每个字段名称之间用“"
                + INLINE_INFO_SEPARATOR
                + "”分隔。"
            )
            print("图片信息普通字段是可以存储单行信息的字段。")
            print(
                "注意：Pic_Collector默认为图片仓库中的图片提供标签功能，所以您不需要在此声明标签字段和标签。备注字段将在稍后进行设置。"
            )
            user_input = input("请输入：")
            print()
            raw_user_defined_ordinary_fields = user_input.split(INLINE_INFO_SEPARATOR)
            num_raw_user_defined_ordinary_field = len(raw_user_defined_ordinary_fields)
            user_defined_ordinary_fields = sorted(
                set(raw_user_defined_ordinary_fields),
                key=raw_user_defined_ordinary_fields.index,
            )
            if len(user_defined_ordinary_fields) != num_raw_user_defined_ordinary_field:
                print(
                    COLOR_YELLOW
                    + "【提示】您输入的图片信息普通字段名称存在重复，重复的图片信息普通字段名称将仅保留一个。"
                    + STYLE_DEFULT
                )
            if "" in user_defined_ordinary_fields:
                user_defined_ordinary_fields.remove("")
            if "文件名" in user_defined_ordinary_fields:
                print(
                    COLOR_YELLOW
                    + "【提示】“文件名”是Pic_Collector的保留字段名。Pic_Collector默认为图片仓库中的图片提供文件名字段。"
                    + STYLE_DEFULT
                )
                user_defined_ordinary_fields.remove("文件名")
            if "标签" in user_defined_ordinary_fields:
                print(
                    COLOR_YELLOW
                    + "【提示】“标签”是Pic_Collector的保留字段名。Pic_Collector默认为图片仓库中的图片提供标签功能。"
                    + STYLE_DEFULT
                )
                user_defined_ordinary_fields.remove("标签")
            if "备注" in user_defined_ordinary_fields:
                print(
                    COLOR_YELLOW
                    + "【提示】“备注”是Pic_Collector的保留字段名。Pic_Collector默认为图片仓库中的图片提供备注字段。"
                    + STYLE_DEFULT
                )
                user_defined_ordinary_fields.remove("备注")

            print("-----")
            print(
                "请输入图片信息备注字段名称，每个字段名称之间用“"
                + INLINE_INFO_SEPARATOR
                + "”分隔。"
            )
            print(
                "图片信息备注字段是可以存储多行信息的字段，Pic_Collector会在图片信息备注字段名称后自动添加“备注”二字"
            )
            print(
                "注意：如果您不输入任何图片信息备注字段名称，Pic_Collector将会自动创建一个默认的备注字段。Pic_Collector默认为图片仓库中的图片提供标签功能，所以您不需要在此声明标签字段和标签。"
            )
            user_input = input("请输入：")
            print()
            raw_user_defined_comment_fields = user_input.split(INLINE_INFO_SEPARATOR)
            num_raw_user_defined_comment_field = len(raw_user_defined_comment_fields)
            user_defined_comment_fields = sorted(
                set(raw_user_defined_comment_fields),
                key=raw_user_defined_comment_fields.index,
            )
            if len(user_defined_comment_fields) != num_raw_user_defined_comment_field:
                print(
                    COLOR_YELLOW
                    + "【提示】您输入的图片信息备注字段名称存在重复，重复的图片信息备注字段名称将仅保留一个。"
                    + STYLE_DEFULT
                )
            if "" in user_defined_comment_fields:
                user_defined_comment_fields.remove("")
            conflicting_fields = []
            for field_i in range(len(user_defined_comment_fields)):
                user_defined_comment_fields[field_i] = (
                    user_defined_comment_fields[field_i] + "备注"
                )
                if user_defined_comment_fields[field_i] in user_defined_ordinary_fields:
                    print(
                        COLOR_YELLOW
                        + "【提示】"
                        + user_defined_comment_fields[field_i]
                        + "已经被声明为图片信息普通字段名称，不能再被声明为图片信息备注字段名称。"
                        + STYLE_DEFULT
                    )
                    conflicting_fields.append(user_defined_comment_fields[field_i])
            for field in conflicting_fields:
                user_defined_comment_fields.remove(field)
            if len(user_defined_comment_fields) == 0:
                user_defined_comment_fields.append("备注")

            print("-----")
            while True:
                print("新建的图片仓库信息：")
                print("仓库名：" + pic_warehouse_name)
                print("图片信息普通字段（不是标签）：")
                for field in user_defined_ordinary_fields:
                    print("\t" + field)
                print("图片信息备注字段：")
                for field in user_defined_comment_fields:
                    print("\t" + field)
                print("\n---")
                print("确定要按这些信息新建图片仓库？")
                print("Y.确定")
                print("N.不，重新设置新建的图片仓库信息。")
                print("Q.退出程序")

                user_input = input("请输入：")
                print()

                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")
                elif user_input[0] == "Y" or user_input[0] == "y":
                    print(STYLE_LOWLIGHT + "开始创建图片仓库..." + STYLE_DEFULT)
                    with open(PIC_WAREHOUSE_INFO_FILE_PATH, "w", encoding="utf-8") as f:
                        f.write(PIC_WAREHOUSE_INFO_FILE_HEAD)
                        f.write("\n\n")
                        f.write(pic_warehouse_name + "\n")
                        user_defined_ordinary_fields_str = ""
                        for field in user_defined_ordinary_fields:
                            user_defined_ordinary_fields_str += (
                                field + INLINE_INFO_SEPARATOR
                            )
                        f.write(user_defined_ordinary_fields_str[:-1])
                        f.write("\n")
                        user_defined_comment_fields_str = ""
                        for field in user_defined_comment_fields:
                            user_defined_comment_fields_str += (
                                field + INLINE_INFO_SEPARATOR
                            )
                        f.write(user_defined_comment_fields_str[:-1])
                        f.write("\n\n")
                        f.write("导入图片时填补空缺编号：F\n")
                        f.write("导入图片时显示细节：T\n")
                        f.write("自动整理图片编号：T\n")
                    with open(PIC_INFO_FILE_PATH, "w", encoding="utf-8") as f:
                        f.write(PIC_INFO_FILE_HEAD)
                        f.write("\n\n")
                    os.makedirs(PIC_FOLDER_PATH)
                    print(STYLE_LOWLIGHT + "图片仓库创建成功" + STYLE_DEFULT)
                    break
                elif user_input[0] == "N" or user_input[0] == "n":
                    break
                elif user_input[0] == "Q" or user_input[0] == "q":
                    sys.exit(0)
                else:
                    print("本程序未能理解您的输入，请您重新输入。")

    warehouse_keeper = PicWarehouseKeeper()
    print("成功加载图片仓库 " + warehouse_keeper.get_warehouse_name())

    current_ii = InteractiveInterface.main_menu
    interface_switching = True

    while True:
        if interface_switching:
            print("=====")
        else:
            interface_switching = True

        if current_ii == InteractiveInterface.main_menu:
            print("---主菜单---")
            print("A.快速搜索")
            print("B.高级搜索")
            print("C.导入图片")
            print("D.查看图片/修改图片信息")
            print("E.修改仓库信息")
            print("S.设置")
            print("T.关于Pic_Collector")
            print("Q.退出")

            user_input = input("请输入：")
            print()

            if user_input == "":
                print("您没有输入任何内容，请您重新输入。")
            elif user_input[0] == "A" or user_input[0] == "a":
                current_ii = InteractiveInterface.fast_search
            elif user_input[0] == "B" or user_input[0] == "b":
                current_ii = InteractiveInterface.advanced_search
            elif user_input[0] == "C" or user_input[0] == "c":
                current_ii = InteractiveInterface.import_pictures
            elif user_input[0] == "D" or user_input[0] == "d":
                current_ii = InteractiveInterface.view_picture_modify_picture_info
            elif user_input[0] == "E" or user_input[0] == "e":
                current_ii = InteractiveInterface.modify_warehouse_info
            elif user_input[0] == "S" or user_input[0] == "s":
                current_ii = InteractiveInterface.settings
            elif user_input[0] == "T" or user_input[0] == "t":
                current_ii = InteractiveInterface.about
            elif user_input[0] == "Q" or user_input[0] == "q":
                sys.exit(0)
            else:
                print("本程序未能理解您的输入，请您重新输入。")
                interface_switching = False

        elif current_ii == InteractiveInterface.fast_search:
            print("---快速搜索---")
            print(
                "快速搜索将根据您输入的单个搜索词进行搜索，\n当搜索词是图片的编号或固定信息字段值或标签时，该图片会被搜索到。"
            )
            print("不支持模糊搜索，但搜索时不区分英文字母的大小写。")
            print("输入“B”或“b”并确认可后退到上级菜单")

            user_input = input("请输入搜索词：")
            print()
            search_term = user_input

            if user_input == "B" or user_input == "b":
                while True:
                    print(
                        "您输入了“"
                        + user_input
                        + "”，请问您是希望搜索“"
                        + user_input
                        + "”还是希望返回到上级菜单？"
                    )
                    print("A.搜索“" + user_input + "”")
                    print("B.返回到上级菜单")
                    user_input = input("请输入：")
                    print()
                    if user_input == "":
                        print("您没有输入任何内容，请您重新输入。")
                    elif user_input[0] == "A" or user_input[0] == "a":
                        break
                    elif user_input[0] == "B" or user_input[0] == "b":
                        current_ii = InteractiveInterface.main_menu
                        break
            if current_ii != InteractiveInterface.fast_search:
                continue

            search_results = warehouse_keeper.fast_search(search_term)
            result_ids = [result[0] for result in search_results]
            show_search_results(search_results)

            while True:
                print(
                    "输入图片索引以查看图片的详细信息，或者按照以下信息选择您希望进行的操作。"
                )
                print("A.复制这些图片到...")
                print("B.返回到主菜单")
                user_input = input("请输入：")
                print()
                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")
                elif user_input[0] == "A" or user_input[0] == "a":
                    copy_pics(result_ids)
                elif user_input[0] == "B" or user_input[0] == "b":
                    break
                else:
                    if user_input.isdigit():
                        concerned_pic_id = int(user_input)
                        return_main_menu = False
                        while True:
                            if warehouse_keeper.check_pic_exist(concerned_pic_id):
                                if concerned_pic_id not in result_ids:
                                    print(
                                        COLOR_YELLOW
                                        + "注意：图片仓库中存在编号"
                                        + str(concerned_pic_id)
                                        + "对应的图片，但该图片不在刚才搜索获得的结果中。"
                                        + STYLE_DEFULT
                                    )
                                next_op, next_id = focus_pic(concerned_pic_id)
                                if next_op == "返回主菜单":
                                    return_main_menu = True
                                else:
                                    concerned_pic_id = next_id
                            else:
                                print("图片仓库中没有您输入的图片编号对应的图片。")
                                break
                            if return_main_menu:
                                break
                            else:
                                continue
                        if return_main_menu:
                            break
                    else:
                        print("本程序未能理解您的输入，请您重新输入。")
            current_ii = InteractiveInterface.main_menu

        elif current_ii == InteractiveInterface.advanced_search:
            print("---高级搜索---")
            print("A.按普通字段和文件名搜索")
            print("B.按标签搜索（和）")
            print("C.按标签搜索（或）")
            print("D.返回主菜单")
            user_input = input("请输入：")
            print()

            if user_input == "":
                print("您没有输入任何内容，请您重新输入。")

            elif user_input[0] == "A" or user_input[0] == "a":
                print("-按普通字段和文件名搜索-")
                print(
                    "您需要针对图片库的每个图片信息普通字段和文件名依次输入搜索词，\n然后在图片库中搜索满足您输入的所有要求的图片。"
                )
                print(
                    "如果您希望对某个字段不做限制，请在需要输入该字段的搜索词时不输入任何内容并直接按下“Enter”键"
                )
                print("不支持模糊搜索，但搜索时不区分英文字母的大小写。")
                common_field_file_name_search_terms_dict = {}
                user_defined_ordinary_fields = (
                    warehouse_keeper.get_user_defined_ordinary_fields()
                )
                field_search_term = input("文件名：")
                if field_search_term != "":
                    common_field_file_name_search_terms_dict["文件名"] = (
                        field_search_term
                    )
                for field in user_defined_ordinary_fields:
                    field_search_term = input(field + "：")
                    if field_search_term != "":
                        common_field_file_name_search_terms_dict[field] = (
                            field_search_term
                        )

                search_results = warehouse_keeper.common_field_file_name_search(
                    common_field_file_name_search_terms_dict
                )
                result_ids = [result[0] for result in search_results]
                show_search_results(search_results)

                while True:
                    print(
                        "输入图片索引以查看图片的详细信息，或者按照以下信息选择您希望进行的操作。"
                    )
                    print("A.复制这些图片到...")
                    print("B.返回到主菜单")
                    user_input = input("请输入：")
                    print()
                    if user_input == "":
                        print("您没有输入任何内容，请您重新输入。")
                    elif user_input[0] == "A" or user_input[0] == "a":
                        copy_pics(result_ids)
                    elif user_input[0] == "B" or user_input[0] == "b":
                        break
                    else:
                        if user_input.isdigit():
                            concerned_pic_id = int(user_input)
                            return_main_menu = False
                            while True:
                                if warehouse_keeper.check_pic_exist(concerned_pic_id):
                                    if concerned_pic_id not in result_ids:
                                        print(
                                            COLOR_YELLOW
                                            + "注意：图片仓库中存在编号"
                                            + str(concerned_pic_id)
                                            + "对应的图片，但该图片不在刚才搜索获得的结果中。"
                                            + STYLE_DEFULT
                                        )
                                    next_op, next_id = focus_pic(concerned_pic_id)
                                    if next_op == "返回主菜单":
                                        return_main_menu = True
                                    else:
                                        concerned_pic_id = next_id
                                else:
                                    print("图片仓库中没有您输入的图片编号对应的图片。")
                                    break
                                if return_main_menu:
                                    break
                                else:
                                    continue
                            if return_main_menu:
                                break
                        else:
                            print("本程序未能理解您的输入，请您重新输入。")
                current_ii = InteractiveInterface.main_menu

            elif user_input[0] == "B" or user_input[0] == "b":
                print("-按标签搜索（和）-")
                print(
                    "您需要输入一组您希望搜索的标签，此功能会搜索同时拥有您输入的所有标签的图片。"
                )
                print("不支持模糊搜索，但搜索时不区分英文字母的大小写。")
                print("输入多个标签时标签之间使用“" + INLINE_INFO_SEPARATOR + "”分隔。")
                user_input = input("请输入您希望搜索的标签集：")
                print()
                if user_input == "":
                    print("您没有输入任何内容，无法进行按标签搜索。")
                else:
                    raw_search_pic_tags = (user_input).split(INLINE_INFO_SEPARATOR)
                    num_raw_search_pic_tags = len(raw_search_pic_tags)
                    search_pic_tags = sorted(
                        set(raw_search_pic_tags), key=raw_search_pic_tags.index
                    )
                    if len(search_pic_tags) != num_raw_search_pic_tags:
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的标签存在重复或与已有的标签重复。"
                            + STYLE_DEFULT
                        )
                    if "" in search_pic_tags:
                        search_pic_tags.remove("")

                    search_results = warehouse_keeper.tag_search(True, search_pic_tags)
                    result_ids = [result[0] for result in search_results]
                    show_search_results(search_results)

                    while True:
                        print(
                            "输入图片索引以查看图片的详细信息，或者按照以下信息选择您希望进行的操作。"
                        )
                        print("A.复制这些图片到...")
                        print("B.返回到主菜单")
                        user_input = input("请输入：")
                        print()
                        if user_input == "":
                            print("您没有输入任何内容，请您重新输入。")
                        elif user_input[0] == "A" or user_input[0] == "a":
                            copy_pics(result_ids)
                        elif user_input[0] == "B" or user_input[0] == "b":
                            break
                        else:
                            if user_input.isdigit():
                                concerned_pic_id = int(user_input)
                                return_main_menu = False
                                while True:
                                    if warehouse_keeper.check_pic_exist(
                                        concerned_pic_id
                                    ):
                                        if concerned_pic_id not in result_ids:
                                            print(
                                                COLOR_YELLOW
                                                + "注意：图片仓库中存在编号"
                                                + str(concerned_pic_id)
                                                + "对应的图片，但该图片不在刚才搜索获得的结果中。"
                                                + STYLE_DEFULT
                                            )
                                        next_op, next_id = focus_pic(concerned_pic_id)
                                        if next_op == "返回主菜单":
                                            return_main_menu = True
                                        else:
                                            concerned_pic_id = next_id
                                    else:
                                        print(
                                            "图片仓库中没有您输入的图片编号对应的图片。"
                                        )
                                        break
                                    if return_main_menu:
                                        break
                                    else:
                                        continue
                                if return_main_menu:
                                    break
                            else:
                                print("本程序未能理解您的输入，请您重新输入。")
                    current_ii = InteractiveInterface.main_menu

            elif user_input[0] == "C" or user_input[0] == "c":
                print("-按标签搜索（或）-")
                print(
                    "您需要输入一组您希望搜索的标签，此功能会搜索拥有您输入的标签中任意至少一个标签的图片。"
                )
                print("不支持模糊搜索，但搜索时不区分英文字母的大小写。")
                print("输入多个标签时标签之间使用“" + INLINE_INFO_SEPARATOR + "”分隔。")
                user_input = input("请输入您希望搜索的标签集：")
                print()
                if user_input == "":
                    print("您没有输入任何内容，无法进行按标签搜索。")
                else:
                    raw_search_pic_tags = (user_input).split(INLINE_INFO_SEPARATOR)
                    num_raw_search_pic_tags = len(raw_search_pic_tags)
                    search_pic_tags = sorted(
                        set(raw_search_pic_tags), key=raw_search_pic_tags.index
                    )
                    if len(search_pic_tags) != num_raw_search_pic_tags:
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的标签存在重复或与已有的标签重复。"
                            + STYLE_DEFULT
                        )
                    if "" in search_pic_tags:
                        search_pic_tags.remove("")

                    search_results = warehouse_keeper.tag_search(False, search_pic_tags)
                    result_ids = [result[0] for result in search_results]
                    show_search_results(search_results)

                    while True:
                        print(
                            "输入图片索引以查看图片的详细信息，或者按照以下信息选择您希望进行的操作。"
                        )
                        print("A.复制这些图片到...")
                        print("B.返回到主菜单")
                        user_input = input("请输入：")
                        print()
                        if user_input == "":
                            print("您没有输入任何内容，请您重新输入。")
                        elif user_input[0] == "A" or user_input[0] == "a":
                            copy_pics(result_ids)
                        elif user_input[0] == "B" or user_input[0] == "b":
                            break
                        else:
                            if user_input.isdigit():
                                concerned_pic_id = int(user_input)
                                return_main_menu = False
                                while True:
                                    if warehouse_keeper.check_pic_exist(
                                        concerned_pic_id
                                    ):
                                        if concerned_pic_id not in result_ids:
                                            print(
                                                COLOR_YELLOW
                                                + "注意：图片仓库中存在编号"
                                                + str(concerned_pic_id)
                                                + "对应的图片，但该图片不在刚才搜索获得的结果中。"
                                                + STYLE_DEFULT
                                            )
                                        next_op, next_id = focus_pic(concerned_pic_id)
                                        if next_op == "返回主菜单":
                                            return_main_menu = True
                                        else:
                                            concerned_pic_id = next_id
                                    else:
                                        print(
                                            "图片仓库中没有您输入的图片编号对应的图片。"
                                        )
                                        break
                                    if return_main_menu:
                                        break
                                    else:
                                        continue
                                if return_main_menu:
                                    break
                            else:
                                print("本程序未能理解您的输入，请您重新输入。")
                    current_ii = InteractiveInterface.main_menu

            elif user_input[0] == "D" or user_input[0] == "d":
                current_ii = InteractiveInterface.main_menu

            else:
                print("本程序未能理解您的输入，请您重新输入。")
                interface_switching = False

        elif current_ii == InteractiveInterface.import_pictures:
            print("---导入图片---")
            print("导入单张图片需要您输入要导入图片的路径，并输入该图片的信息。")
            print(
                "导入多张图片需要您将要导入的图片集合存入一个文件夹并输入该文件夹的路径，\n准备按照规范书写的保存有导入的图片的信息的文本文件并输入该文本文件的路径。"
            )
            print(
                "若想要了解关于导入多张图片的图片信息文本文件书写规范和注意事项的更多信息请选择“C”选项。"
            )
            print(
                "导入图片会将您选择的图片复制入Pic_Collector的图片仓库，不会删除原图片。"
            )
            print("A.导入单张图片")
            print("B.导入多张图片")
            print("C.查看导入多张图片的图片信息文本文件书写规范")
            print("D.返回主菜单")
            user_input = input("请输入：")
            print()

            if user_input == "":
                print("您没有输入任何内容，请您重新输入。")

            elif user_input[0] == "A" or user_input[0] == "a":
                print("---导入单张图片---")
                print("导入单张图片需要您输入要导入图片的路径，并输入该图片的信息。")
                print(
                    "注意：您需要输入包含图片文件后缀名的路径；请使用“/”作为文件路径分隔符。"
                )

                user_input = input("请输入要导入的图片的路径：")
                print()
                if os.path.exists(user_input) and os.path.isfile(user_input):
                    import_pic_path = user_input

                    import_pic_info = {}
                    user_defined_ordinary_fields = (
                        warehouse_keeper.get_user_defined_ordinary_fields()
                    )
                    for field in user_defined_ordinary_fields:
                        user_input = input("请输入该图片的" + field + "：")
                        import_pic_info[field] = user_input
                    print(
                        "请输入该图片的标签，标签之间使用“"
                        + INLINE_INFO_SEPARATOR
                        + "”分隔。"
                    )
                    user_input = input("请输入：")
                    raw_import_pic_tags = user_input.split(INLINE_INFO_SEPARATOR)
                    num_raw_import_pic_tags = len(raw_import_pic_tags)
                    import_pic_tags = sorted(
                        set(raw_import_pic_tags), key=raw_import_pic_tags.index
                    )
                    if len(import_pic_tags) != num_raw_import_pic_tags:
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的标签存在重复，重复的标签将仅保留一个。"
                            + STYLE_DEFULT
                        )
                    if "" in import_pic_tags:
                        import_pic_tags.remove("")
                    import_pic_info["标签"] = import_pic_tags
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    for field in user_defined_comment_fields:
                        while True:
                            num_comment_line = 0
                            user_input = input("请输入该图片的" + field + "信息行数：")
                            if user_input.isdigit():
                                num_comment_line = int(user_input)
                                if num_comment_line >= 0:
                                    break
                                else:
                                    print(
                                        "图片的"
                                        + field
                                        + "信息行数应大于等于零，请您重新输入。"
                                    )
                            else:
                                print("本程序未能理解您的输入，请您重新输入。")
                        comment = ""
                        for line_i in range(num_comment_line):
                            user_input = input(
                                "请输入第"
                                + str(line_i + 1)
                                + "行该图片的"
                                + field
                                + "信息："
                            )
                            comment += user_input + "\n"
                        import_pic_info[field] = comment[:-1]
                    print()

                    print("---确认导入图片---")
                    print("要导入的图片的路径：" + import_pic_path)
                    for field in import_pic_info.keys():
                        if field == "标签":
                            tags_str = ""
                            for tag in import_pic_info["标签"]:
                                tags_str += tag + INLINE_INFO_SEPARATOR
                            print("标签：" + tags_str[:-1])
                        elif field in user_defined_comment_fields:
                            print(field + "：")
                            print(import_pic_info[field])
                        else:
                            print(field + "：" + import_pic_info[field])
                    print("---")
                    while True:
                        print("A.确认导入")
                        print("B.放弃导入")
                        user_input = input("请输入：")
                        print()
                        if user_input == "":
                            print("您没有输入任何内容，请您重新输入。")
                        elif user_input[0] == "A" or user_input[0] == "a":
                            warehouse_keeper.import_pics(
                                [import_pic_path], [import_pic_info]
                            )
                            break
                        elif user_input[0] == "B" or user_input[0] == "b":
                            break
                        else:
                            print("本程序未能理解您的输入，请您重新输入。")

                else:
                    print("未找到您指定的图片。")
                    interface_switching = False
                    print()

            elif user_input[0] == "B" or user_input[0] == "b":
                print("---导入多张图片---")
                print(
                    "导入多张图片需要您将要导入的图片集合存入一个文件夹并输入该文件夹的路径，\n准备按照规范书写的保存有导入的图片的信息的文本文件并输入该文本文件的路径。"
                )
                print("注意：输入路径时请使用“/”作为文件路径分隔符。")
                user_input = input("请输入要导入的图片所在的文件夹路径：")
                print()
                if os.path.exists(user_input) and os.path.isdir(user_input):
                    import_pics_folder_path = user_input
                    user_input = input("请输入要导入的图片对应的图片信息文件路径：")
                    print()
                    if (
                        user_input[-4:] == ".txt"
                        and os.path.exists(user_input)
                        and os.path.isfile(user_input)
                    ):
                        import_pics_info_file_path = user_input
                        print(
                            STYLE_LOWLIGHT
                            + "开始读取并检查导入图片的信息..."
                            + STYLE_DEFULT
                        )
                        exception_explanation_info = "触发Python提供的异常。"
                        exception_line_number = 0
                        try:
                            import_pics_path = []
                            import_pics_info = []
                            with open(
                                import_pics_info_file_path, "r", encoding="utf-8"
                            ) as f:
                                while True:
                                    raw_id_str = f.readline()[:-1]
                                    exception_line_number += 1
                                    if raw_id_str == "":
                                        break
                                    import_pic_info = {}

                                    pic_info_line_info = f.readline()[:-1].split("：")
                                    exception_line_number += 1
                                    if (
                                        pic_info_line_info[0] != "文件名"
                                        or len(pic_info_line_info) < 2
                                    ):
                                        exception_explanation_info = (
                                            "有图片的文件名信息没有被读取到。"
                                        )
                                        raise Exception()
                                    import_pic_info["文件名"] = pic_info_line_info[1]
                                    import_pic_path = (
                                        import_pics_folder_path
                                        + "/"
                                        + import_pic_info["文件名"]
                                    )
                                    if not (
                                        os.path.exists(import_pic_path)
                                        and os.path.isfile(import_pic_path)
                                    ):
                                        exception_explanation_info = (
                                            "指定的图片信息包含无法找到的图片的信息。"
                                        )
                                        raise Exception()

                                    user_defined_ordinary_fields = (
                                        warehouse_keeper.get_user_defined_ordinary_fields()
                                    )
                                    while True:
                                        pic_info_line_info = f.readline()[:-1].split(
                                            "："
                                        )
                                        exception_line_number += 1
                                        field_name = pic_info_line_info[0]
                                        if field_name == "标签":
                                            break
                                        if (
                                            field_name
                                            not in user_defined_ordinary_fields
                                        ):
                                            exception_explanation_info = "指定的图片信息包含图片仓库图片信息中没有声明的普通字段。"
                                            raise Exception()
                                        if len(pic_info_line_info) < 2:
                                            import_pic_info[field_name] = ""
                                        else:
                                            import_pic_info[field_name] = (
                                                pic_info_line_info[1]
                                            )
                                    for field in user_defined_ordinary_fields:
                                        if field not in import_pic_info.keys():
                                            import_pic_info[field] = ""

                                    raw_import_pic_tags = pic_info_line_info[1].split(
                                        INLINE_INFO_SEPARATOR
                                    )
                                    num_raw_import_pic_tags = len(raw_import_pic_tags)
                                    import_pic_tags = sorted(
                                        set(raw_import_pic_tags),
                                        key=raw_import_pic_tags.index,
                                    )
                                    if len(import_pic_tags) != num_raw_import_pic_tags:
                                        print(
                                            COLOR_YELLOW
                                            + "【提示】指定的图片信息中代号为 "
                                            + raw_id_str
                                            + " 的图片存在标签重复，重复的标签将仅保留一个。"
                                            + STYLE_DEFULT
                                        )
                                    if "" in import_pic_tags:
                                        import_pic_tags.remove("")
                                    import_pic_info["标签"] = import_pic_tags

                                    user_defined_comment_fields = (
                                        warehouse_keeper.get_user_defined_comment_fields()
                                    )
                                    while True:
                                        pic_info_line = f.readline()[:-1]
                                        exception_line_number += 1
                                        if pic_info_line == "":
                                            break
                                        pic_info_line_info = pic_info_line.split("：")
                                        field_name = pic_info_line_info[0]
                                        if (
                                            field_name
                                            not in user_defined_comment_fields
                                        ):
                                            exception_explanation_info = "指定的图片信息包含图片仓库图片信息中没有声明的备注字段。"
                                            raise Exception()
                                        if len(pic_info_line_info) < 2:
                                            import_pic_info[field_name] = ""
                                        else:
                                            num_comment_line = int(
                                                pic_info_line_info[1]
                                            )
                                            comment = ""
                                            for _ in range(num_comment_line):
                                                comment += f.readline()
                                                exception_line_number += 1
                                            import_pic_info[field_name] = comment[:-1]
                                    for field in user_defined_comment_fields:
                                        if field not in import_pic_info.keys():
                                            import_pic_info[field] = ""

                                    import_pics_path.append(import_pic_path)
                                    import_pics_info.append(import_pic_info)
                        except Exception:
                            print(
                                STYLE_LOWLIGHT
                                + "导入图片的信息未能成功读取并通过检查"
                                + STYLE_DEFULT
                            )
                            print(
                                COLOR_YELLOW
                                + "【提示】您输指定的图片信息文件内容存在错误或不符合规范。"
                                + STYLE_DEFULT
                            )
                            print(
                                COLOR_YELLOW
                                + "关于导入图片的信息未能成功读取并通过检查的解释："
                                + exception_explanation_info
                                + STYLE_DEFULT
                            )
                            print(
                                COLOR_YELLOW
                                + "触发导入图片的信息未能成功读取并通过检查的行号："
                                + str(exception_line_number)
                                + STYLE_DEFULT
                            )
                            interface_switching = False
                            print()
                        else:
                            print(
                                STYLE_LOWLIGHT
                                + "导入图片的信息已经成功读取并通过检查"
                                + STYLE_DEFULT
                            )
                            warehouse_keeper.import_pics(
                                import_pics_path, import_pics_info
                            )
                            current_ii = InteractiveInterface.main_menu
                    else:
                        print("未找到您指定的图片信息文件。")
                        interface_switching = False
                        print()
                else:
                    print("未找到您指定的文件夹。")
                    interface_switching = False
                    print()

            elif user_input[0] == "C" or user_input[0] == "c":
                print_import_pic_info_norm()
                print()
                interface_switching = False

            elif user_input[0] == "D" or user_input[0] == "d":
                current_ii = InteractiveInterface.main_menu

            else:
                print("本程序未能理解您的输入，请您重新输入。")
                interface_switching = False

        elif current_ii == InteractiveInterface.view_picture_modify_picture_info:
            print("---查看图片/修改图片信息---")
            print("图片仓库名称：" + warehouse_keeper.get_warehouse_name())
            num_pic = warehouse_keeper.get_num_pic()
            if num_pic > 0:
                print("图片仓库中的图片数量：" + str(num_pic))
                print(
                    "图片仓库中最大的图片编号："
                    + str(warehouse_keeper.get_biggest_pic_id())
                )
            else:
                print("图片仓库中当前没有图片")
                print(
                    "您可以返回主菜单后选择“导入图片”，并根据指引向图片仓库中导入图片。"
                )

            while True:
                print(
                    "输入图片索引以查看/修改图片的详细信息，或者按照以下信息选择您希望进行的操作。"
                )
                print("A.随机查看/修改一张图片的详细信息")
                print("B.导出图片仓库中的所有图片")
                print("C.导出图片仓库中的图片信息")
                print("D.删除图片仓库中的所有图片")
                print("E.返回主菜单")
                user_input = input("请输入：")
                print()

                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")

                elif user_input.isdigit():
                    concerned_pic_id = int(user_input)
                    return_main_menu = False
                    while True:
                        if warehouse_keeper.check_pic_exist(concerned_pic_id):
                            next_op, next_id = focus_pic(concerned_pic_id)
                            if next_op == "返回主菜单":
                                return_main_menu = True
                            else:
                                concerned_pic_id = next_id
                        else:
                            print("图片仓库中没有您输入的图片编号对应的图片。")
                            break
                        if return_main_menu:
                            break
                        else:
                            continue
                    if return_main_menu:
                        current_ii = InteractiveInterface.main_menu
                        break

                elif user_input[0] == "A" or user_input[0] == "a":
                    num_pic = warehouse_keeper.get_num_pic()
                    if num_pic > 0:
                        concerned_pic_id = random.randint(1, num_pic)
                        return_main_menu = False
                        while True:
                            next_op, next_id = focus_pic(concerned_pic_id)
                            if next_op == "返回主菜单":
                                return_main_menu = True
                            else:
                                concerned_pic_id = next_id
                            if return_main_menu:
                                break
                            else:
                                continue
                        if return_main_menu:
                            current_ii = InteractiveInterface.main_menu
                            break
                    else:
                        print("因为图片仓库中当前没有图片，所以无法执行该操作")
                        print(
                            "您可以返回主菜单后选择“导入图片”，并根据指引向图片仓库中导入图片。"
                        )

                elif user_input[0] == "B" or user_input[0] == "b":
                    all_id = warehouse_keeper.get_all_ids()
                    copy_pics(all_id)

                elif user_input[0] == "C" or user_input[0] == "c":
                    while True:
                        print("请输入您希望导出到的文件夹的路径。")
                        user_input = input("请输入：")
                        print()
                        reenter_path = False
                        if not (
                            os.path.exists(user_input)
                            and (not os.path.isfile(user_input))
                        ):

                            while True:
                                print(
                                    "您输入的文件夹不存在，是否要按照您输入的路径新建文件夹？"
                                )
                                print("Y.是")
                                print("N.否")
                                sec_user_input = input("请输入：")
                                print()
                                if user_input == "":
                                    print("您没有输入任何内容，请您重新输入。")
                                elif (
                                    sec_user_input[0] == "Y" or sec_user_input[0] == "y"
                                ):
                                    os.makedirs(user_input)
                                    print(
                                        STYLE_LOWLIGHT
                                        + "已创建文件夹 "
                                        + sec_user_input
                                        + STYLE_DEFULT
                                    )
                                    break
                                elif (
                                    sec_user_input[0] == "N" or sec_user_input[0] == "n"
                                ):
                                    reenter_path = True
                                    break
                                else:
                                    print("本程序未能理解您的输入，请您重新输入。")
                        if reenter_path:
                            continue
                        else:
                            copy_target_folder_path = user_input
                            break

                    copy_target_txt_path = (
                        copy_target_folder_path
                        + "/"
                        + warehouse_keeper.get_warehouse_name()
                        + "_图片信息导出_"
                        + time.strftime("%Y%m%d", time.localtime())
                        + ".txt"
                    )
                    print("图片仓库中的图片信息将被导出到" + copy_target_txt_path)
                    if os.path.exists(copy_target_txt_path):
                        while True:
                            print(
                                "已经存在"
                                + copy_target_txt_path
                                + "，如果您不希望覆盖保存，请转移或重命名当前已有的"
                                + copy_target_txt_path
                                + "。"
                            )
                            print(
                                "A.希望覆盖保存，或已经转移或重命名可能被覆盖的文件。"
                            )
                            print("B.停止导出图片信息")
                            sec_user_input = input("请输入：")
                            print()
                            if user_input == "":
                                print("您没有输入任何内容，请您重新输入。")
                            elif sec_user_input[0] == "A" or sec_user_input[0] == "a":
                                warehouse_keeper.export_pics_info(copy_target_txt_path)
                                break
                            elif sec_user_input[0] == "B" or sec_user_input[0] == "b":
                                break
                            else:
                                print("本程序未能理解您的输入，请您重新输入。")
                    else:
                        warehouse_keeper.export_pics_info(copy_target_txt_path)

                elif user_input[0] == "D" or user_input[0] == "d":
                    print(
                        "您确定要删除图片仓库中的所有图片吗？删除后将无法找回图片及其信息。"
                    )
                    print(
                        "若您确定要删除图片仓库中的所有图片，请输入“确定删除所有图片”，输入其他任意内容则返回上一级菜单。"
                    )
                    user_input = input("请输入：")
                    print()
                    if user_input == "确定删除所有图片":
                        warehouse_keeper.delete_all_pics()
                    else:
                        print("未执行删除操作，将返回上一级菜单。")

                elif user_input[0] == "E" or user_input[0] == "e":
                    current_ii = InteractiveInterface.main_menu
                    break

                else:
                    print("本程序未能理解您的输入，请您重新输入。")

        elif current_ii == InteractiveInterface.modify_warehouse_info:
            print("---修改仓库信息---")
            print("图片仓库名称：" + warehouse_keeper.get_warehouse_name())
            num_pic = warehouse_keeper.get_num_pic()
            if num_pic > 0:
                print("图片仓库中的图片数量：" + str(num_pic))
                print(
                    "图片仓库中最大的图片编号："
                    + str(warehouse_keeper.get_biggest_pic_id())
                )
            else:
                print("图片仓库中当前没有图片")
                print(
                    "您可以返回主菜单后选择“导入图片”，并根据指引向图片仓库中导入图片。"
                )
            user_defined_ordinary_fields = (
                warehouse_keeper.get_user_defined_ordinary_fields()
            )
            num_user_defined_ordinary_fields = len(user_defined_ordinary_fields)
            if num_user_defined_ordinary_fields > 0:
                print(
                    "仓库中的用户定义普通字段数量："
                    + str(num_user_defined_ordinary_fields)
                )
                print("仓库中的用户定义普通字段：")
                user_defined_ordinary_fields_str = ""
                for field in user_defined_ordinary_fields:
                    user_defined_ordinary_fields_str += field + INLINE_INFO_SEPARATOR
                print(user_defined_ordinary_fields_str[:-1])
            else:
                print("仓库中没有用户定义普通字段")
            user_defined_comment_fields = (
                warehouse_keeper.get_user_defined_comment_fields()
            )
            num_user_defined_comment_fields = len(user_defined_comment_fields)
            print("仓库中的备注字段数量：" + str(num_user_defined_comment_fields))
            print("仓库中的备注字段：")
            user_defined_comment_fields_str = ""
            for field in user_defined_comment_fields:
                user_defined_comment_fields_str += field + INLINE_INFO_SEPARATOR
            print(user_defined_comment_fields_str[:-1])

            while True:
                print("---")
                print("A.修改仓库名称")
                print("B.添加普通字段")
                print("C.删除普通字段")
                print("D.添加备注字段")
                print("E.删除备注字段")
                print("F.返回主菜单")
                user_input = input("请输入：")
                print()

                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")

                elif user_input[0] == "A" or user_input[0] == "a":
                    print("-修改仓库名称-")
                    print("当前的仓库名称：" + warehouse_keeper.get_warehouse_name())
                    user_input = input("将仓库名称改为：")
                    print()
                    if user_input == "":
                        print(
                            COLOR_YELLOW
                            + "修改失败，仓库名称不允许为空。"
                            + STYLE_DEFULT
                        )
                    else:
                        warehouse_keeper.modify_pic_warehouse_name(user_input)
                    print("当前的仓库名称：" + warehouse_keeper.get_warehouse_name())

                elif user_input[0] == "B" or user_input[0] == "b":
                    print("-添加普通字段-")
                    user_defined_ordinary_fields = (
                        warehouse_keeper.get_user_defined_ordinary_fields()
                    )
                    num_user_defined_ordinary_fields = len(user_defined_ordinary_fields)
                    print(
                        "当前仓库中的用户定义普通字段数量："
                        + str(num_user_defined_ordinary_fields)
                    )
                    print("当前仓库中的用户定义普通字段：")
                    user_defined_ordinary_fields_str = ""
                    for field in user_defined_ordinary_fields:
                        user_defined_ordinary_fields_str += (
                            field + INLINE_INFO_SEPARATOR
                        )
                    print(user_defined_ordinary_fields_str[:-1])
                    print("图片信息普通字段是可以存储单行信息的字段。")
                    print("对于图片仓库中已有的图片的新普通字段的值，将置为空字符串。")
                    print("输入多个字段时使用“" + INLINE_INFO_SEPARATOR + "”分隔。")
                    user_input = input("请输入您希望增加的普通字段：")
                    print()
                    raw_new_user_defined_ordinary_fields = user_input.split(
                        INLINE_INFO_SEPARATOR
                    )
                    num_raw_new_user_defined_ordinary_field = len(
                        raw_new_user_defined_ordinary_fields
                    )
                    new_user_defined_ordinary_fields = sorted(
                        set(raw_new_user_defined_ordinary_fields),
                        key=raw_new_user_defined_ordinary_fields.index,
                    )
                    if (
                        len(new_user_defined_ordinary_fields)
                        != num_raw_new_user_defined_ordinary_field
                    ):
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的想要增加的图片信息普通字段名称存在重复，重复的图片信息普通字段名称将仅保留一个。"
                            + STYLE_DEFULT
                        )
                    if "" in new_user_defined_ordinary_fields:
                        new_user_defined_ordinary_fields.remove("")
                    if "文件名" in new_user_defined_ordinary_fields:
                        print(
                            COLOR_YELLOW
                            + "【提示】“文件名”是Pic_Collector的保留字段名。Pic_Collector默认为图片仓库中的图片提供文件名字段。"
                            + STYLE_DEFULT
                        )
                        new_user_defined_ordinary_fields.remove("文件名")
                    if "标签" in new_user_defined_ordinary_fields:
                        print(
                            COLOR_YELLOW
                            + "【提示】“标签”是Pic_Collector的保留字段名。Pic_Collector默认为图片仓库中的图片提供标签功能。"
                            + STYLE_DEFULT
                        )
                        new_user_defined_ordinary_fields.remove("标签")
                    if "备注" in new_user_defined_ordinary_fields:
                        print(
                            COLOR_YELLOW
                            + "【提示】“备注”是Pic_Collector的保留字段名。Pic_Collector默认为图片仓库中的图片提供备注字段。"
                            + STYLE_DEFULT
                        )
                        new_user_defined_ordinary_fields.remove("备注")
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    conflicting_fields = []
                    for field in new_user_defined_ordinary_fields:
                        if field in user_defined_comment_fields:
                            print(
                                COLOR_YELLOW
                                + "【提示】图片仓库中已存在名称为“"
                                + field
                                + "”普通字段。"
                                + STYLE_DEFULT
                            )
                            conflicting_fields.append(field)
                        else:
                            if field in user_defined_comment_fields:
                                print(
                                    COLOR_YELLOW
                                    + "【提示】图片仓库中已存在名称为“"
                                    + field
                                    + "”的备注字段。"
                                    + STYLE_DEFULT
                                )
                                conflicting_fields.append(field)
                    for field in conflicting_fields:
                        new_user_defined_ordinary_fields.remove(field)
                    if len(new_user_defined_ordinary_fields) > 0:
                        warehouse_keeper.add_user_defined_ordinary_fields(
                            new_user_defined_ordinary_fields
                        )
                    else:
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的希望增加的普通字段均无法添加。"
                            + STYLE_DEFULT
                        )
                    user_defined_ordinary_fields = (
                        warehouse_keeper.get_user_defined_ordinary_fields()
                    )
                    num_user_defined_ordinary_fields = len(user_defined_ordinary_fields)
                    print(
                        "当前仓库中的用户定义普通字段数量："
                        + str(num_user_defined_ordinary_fields)
                    )
                    print("当前仓库中的用户定义普通字段：")
                    user_defined_ordinary_fields_str = ""
                    for field in user_defined_ordinary_fields:
                        user_defined_ordinary_fields_str += (
                            field + INLINE_INFO_SEPARATOR
                        )
                    print(user_defined_ordinary_fields_str[:-1])

                elif user_input[0] == "C" or user_input[0] == "c":
                    print("-删除普通字段-")
                    user_defined_ordinary_fields = (
                        warehouse_keeper.get_user_defined_ordinary_fields()
                    )
                    num_user_defined_ordinary_fields = len(user_defined_ordinary_fields)
                    print(
                        "当前仓库中的用户定义普通字段数量："
                        + str(num_user_defined_ordinary_fields)
                    )
                    print("当前仓库中的用户定义普通字段：")
                    user_defined_ordinary_fields_str = ""
                    for field in user_defined_ordinary_fields:
                        user_defined_ordinary_fields_str += (
                            field + INLINE_INFO_SEPARATOR
                        )
                    print(user_defined_ordinary_fields_str[:-1])
                    print(
                        COLOR_YELLOW
                        + "注意：删除字段会删除图片仓库中已有的图片的被删除字段的信息。"
                        + STYLE_DEFULT
                    )
                    print(
                        "若您现在改变主意不想删除任何字段了，您可以随意输入一个当前图片仓库中并不存在的用户定义普通字段名称，Pic_Collector会提示后返回上一级菜单。"
                    )
                    print("输入多个字段时使用“" + INLINE_INFO_SEPARATOR + "”分隔。")
                    user_input = input("请输入您希望删除的普通字段：")
                    print()
                    raw_del_user_defined_ordinary_fields = user_input.split(
                        INLINE_INFO_SEPARATOR
                    )
                    num_raw_del_user_defined_ordinary_field = len(
                        raw_del_user_defined_ordinary_fields
                    )
                    del_user_defined_ordinary_fields = sorted(
                        set(raw_del_user_defined_ordinary_fields),
                        key=raw_del_user_defined_ordinary_fields.index,
                    )
                    if (
                        len(del_user_defined_ordinary_fields)
                        != num_raw_del_user_defined_ordinary_field
                    ):
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的想要删除的图片信息普通字段名称存在重复。"
                            + STYLE_DEFULT
                        )
                    if "" in del_user_defined_ordinary_fields:
                        del_user_defined_ordinary_fields.remove("")
                    existing_fields_in_del_user_defined_ordinary_fields = []
                    for field in del_user_defined_ordinary_fields:
                        if field in user_defined_ordinary_fields:
                            existing_fields_in_del_user_defined_ordinary_fields.append(
                                field
                            )
                        else:
                            print(
                                COLOR_YELLOW
                                + "【提示】图片仓库原来并没有您希望删除的“"
                                + field
                                + "”字段。"
                                + STYLE_DEFULT
                            )
                    if len(existing_fields_in_del_user_defined_ordinary_fields) > 0:
                        warehouse_keeper.del_user_defined_ordinary_fields(
                            existing_fields_in_del_user_defined_ordinary_fields
                        )
                    else:
                        print("没有删除任何字段。")
                    num_user_defined_ordinary_fields = len(user_defined_ordinary_fields)
                    print(
                        "当前仓库中的用户定义普通字段数量："
                        + str(num_user_defined_ordinary_fields)
                    )
                    print("当前仓库中的用户定义普通字段：")
                    user_defined_ordinary_fields_str = ""
                    for field in user_defined_ordinary_fields:
                        user_defined_ordinary_fields_str += (
                            field + INLINE_INFO_SEPARATOR
                        )
                    print(user_defined_ordinary_fields_str[:-1])

                elif user_input[0] == "D" or user_input[0] == "d":
                    print("-添加备注字段-")
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    num_user_defined_comment_fields = len(user_defined_comment_fields)
                    print(
                        "当前仓库中的备注字段数量："
                        + str(num_user_defined_comment_fields)
                    )
                    print("当前仓库中的备注字段：")
                    user_defined_comment_fields_str = ""
                    for field in user_defined_comment_fields:
                        user_defined_comment_fields_str += field + INLINE_INFO_SEPARATOR
                    print(user_defined_comment_fields_str[:-1])
                    print(
                        "图片信息备注字段是可以存储多行信息的字段，Pic_Collector会在图片信息备注字段名称后自动添加“备注”二字"
                    )
                    print("对于图片仓库中已有的图片的新普通字段的值，将置为空字符串。")
                    print("输入多个字段时使用“" + INLINE_INFO_SEPARATOR + "”分隔。")
                    user_input = input("请输入您希望增加的备注字段：")
                    print()
                    raw_new_user_defined_comment_fields = user_input.split(
                        INLINE_INFO_SEPARATOR
                    )
                    num_raw_new_user_defined_comment_field = len(
                        raw_new_user_defined_comment_fields
                    )
                    new_user_defined_comment_fields = sorted(
                        set(raw_new_user_defined_comment_fields),
                        key=raw_new_user_defined_comment_fields.index,
                    )
                    if (
                        len(new_user_defined_comment_fields)
                        != num_raw_new_user_defined_comment_field
                    ):
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的想要增加的图片信息备注字段名称存在重复，重复的图片信息备注字段名称将仅保留一个。"
                            + STYLE_DEFULT
                        )
                    if "" in new_user_defined_comment_fields:
                        new_user_defined_comment_fields.remove("")
                    user_defined_ordinary_fields = (
                        warehouse_keeper.get_user_defined_ordinary_fields()
                    )
                    conflicting_fields = []
                    for field_i in range(len(new_user_defined_comment_fields)):
                        new_user_defined_comment_fields[field_i] = (
                            new_user_defined_comment_fields[field_i] + "备注"
                        )
                        if (
                            new_user_defined_comment_fields[field_i]
                            in user_defined_ordinary_fields
                        ):
                            print(
                                COLOR_YELLOW
                                + "【提示】图片仓库中已存在名称为“"
                                + field
                                + "”的普通字段。"
                                + STYLE_DEFULT
                            )
                            conflicting_fields.append(
                                new_user_defined_comment_fields[field_i]
                            )
                        else:
                            if (
                                new_user_defined_comment_fields[field_i]
                                in user_defined_comment_fields
                            ):
                                print(
                                    COLOR_YELLOW
                                    + "【提示】图片仓库中已存在名称为“"
                                    + field
                                    + "”的备注字段。"
                                    + STYLE_DEFULT
                                )
                                conflicting_fields.append(field)
                    for field in conflicting_fields:
                        new_user_defined_comment_fields.remove(field)
                    if len(new_user_defined_comment_fields) > 0:
                        warehouse_keeper.add_user_defined_comment_fields(
                            new_user_defined_comment_fields
                        )
                    else:
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的希望增加的备注字段均无法添加。"
                            + STYLE_DEFULT
                        )
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    num_user_defined_comment_fields = len(user_defined_comment_fields)
                    print(
                        "当前仓库中的备注字段数量："
                        + str(num_user_defined_comment_fields)
                    )
                    print("当前仓库中的备注字段：")
                    user_defined_comment_fields_str = ""
                    for field in user_defined_comment_fields:
                        user_defined_comment_fields_str += field + INLINE_INFO_SEPARATOR
                    print(user_defined_comment_fields_str[:-1])

                elif user_input[0] == "E" or user_input[0] == "e":
                    print("-删除备注字段-")
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    num_user_defined_comment_fields = len(user_defined_comment_fields)
                    print(
                        "当前仓库中的备注字段数量："
                        + str(num_user_defined_comment_fields)
                    )
                    print("当前仓库中的备注字段：")
                    user_defined_comment_fields_str = ""
                    for field in user_defined_comment_fields:
                        user_defined_comment_fields_str += field + INLINE_INFO_SEPARATOR
                    print(user_defined_comment_fields_str[:-1])
                    print(
                        COLOR_YELLOW
                        + "注意：删除字段会删除图片仓库中已有的图片的被删除字段的信息。"
                        + STYLE_DEFULT
                    )
                    print(
                        "若您现在改变主意不想删除任何字段了，您可以随意输入一个当前图片仓库中并不存在的备注字段名称，Pic_Collector会提示后返回上一级菜单。"
                    )
                    print("输入多个字段时使用“" + INLINE_INFO_SEPARATOR + "”分隔。")
                    user_input = input("请输入您希望删除的备注字段：")
                    print()
                    raw_del_user_defined_comment_fields = user_input.split(
                        INLINE_INFO_SEPARATOR
                    )
                    num_raw_del_user_defined_comment_field = len(
                        raw_del_user_defined_comment_fields
                    )
                    del_user_defined_comment_fields = sorted(
                        set(raw_del_user_defined_comment_fields),
                        key=raw_del_user_defined_comment_fields.index,
                    )
                    if (
                        len(del_user_defined_comment_fields)
                        != num_raw_del_user_defined_comment_field
                    ):
                        print(
                            COLOR_YELLOW
                            + "【提示】您输入的想要删除的图片信息备注字段名称存在重复。"
                            + STYLE_DEFULT
                        )
                    if "" in del_user_defined_comment_fields:
                        del_user_defined_comment_fields.remove("")
                    existing_fields_in_del_user_defined_comment_fields = []
                    for field in del_user_defined_comment_fields:
                        if field in user_defined_comment_fields:
                            existing_fields_in_del_user_defined_comment_fields.append(
                                field
                            )
                        else:
                            print(
                                COLOR_YELLOW
                                + "【提示】图片仓库原来并没有您希望删除的“"
                                + field
                                + "”字段。"
                                + STYLE_DEFULT
                            )
                    if len(existing_fields_in_del_user_defined_comment_fields):
                        warehouse_keeper.del_user_defined_comment_fields(
                            existing_fields_in_del_user_defined_comment_fields
                        )
                    else:
                        print("没有删除任何字段。")
                    user_defined_comment_fields = (
                        warehouse_keeper.get_user_defined_comment_fields()
                    )
                    num_user_defined_comment_fields = len(user_defined_comment_fields)
                    print(
                        "当前仓库中的备注字段数量："
                        + str(num_user_defined_comment_fields)
                    )
                    print("当前仓库中的备注字段：")
                    user_defined_comment_fields_str = ""
                    for field in user_defined_comment_fields:
                        user_defined_comment_fields_str += field + INLINE_INFO_SEPARATOR
                    print(user_defined_comment_fields_str[:-1])

                elif user_input[0] == "F" or user_input[0] == "f":
                    current_ii = InteractiveInterface.main_menu
                    break

                else:
                    print("本程序未能理解您的输入，请您重新输入。")

        elif current_ii == InteractiveInterface.settings:
            print("---设置---")
            print(
                "导入图片时填补空缺编号："
                + str(warehouse_keeper.get_import_fill_vacancy_num())
            )
            print(
                "导入图片时显示细节：" + str(warehouse_keeper.get_import_show_details())
            )
            print("自动整理图片编号：" + str(warehouse_keeper.get_auto_sort_pic_id()))
            print()
            while True:
                print("A.调整 导入图片时填补空缺编号 设置项")
                print("B.调整 导入图片时显示细节 设置项")
                print("C.调整 自动整理图片编号 设置项")
                print("D.返回主菜单")
                user_input = input("请输入：")
                print()

                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")

                elif user_input[0] == "A" or user_input[0] == "a":
                    warehouse_keeper.set_import_fill_vacancy_num(
                        not warehouse_keeper.get_import_fill_vacancy_num()
                    )
                    print(
                        "导入图片时填补空缺编号："
                        + str(warehouse_keeper.get_import_fill_vacancy_num())
                    )
                    print(
                        "导入图片时显示细节："
                        + str(warehouse_keeper.get_import_show_details())
                    )
                    print(
                        "自动整理图片编号："
                        + str(warehouse_keeper.get_auto_sort_pic_id())
                    )

                elif user_input[0] == "B" or user_input[0] == "b":
                    warehouse_keeper.set_import_show_details(
                        not warehouse_keeper.get_import_show_details()
                    )
                    print(
                        "导入图片时填补空缺编号："
                        + str(warehouse_keeper.get_import_fill_vacancy_num())
                    )
                    print(
                        "导入图片时显示细节："
                        + str(warehouse_keeper.get_import_show_details())
                    )
                    print(
                        "自动整理图片编号："
                        + str(warehouse_keeper.get_auto_sort_pic_id())
                    )

                elif user_input[0] == "C" or user_input[0] == "c":
                    warehouse_keeper.set_auto_sort_pic_id(
                        not warehouse_keeper.get_auto_sort_pic_id()
                    )
                    print(
                        "导入图片时填补空缺编号："
                        + str(warehouse_keeper.get_import_fill_vacancy_num())
                    )
                    print(
                        "导入图片时显示细节："
                        + str(warehouse_keeper.get_import_show_details())
                    )
                    print(
                        "自动整理图片编号："
                        + str(warehouse_keeper.get_auto_sort_pic_id())
                    )

                elif user_input[0] == "D" or user_input[0] == "d":
                    current_ii = InteractiveInterface.main_menu
                    break

                else:
                    print("本程序未能理解您的输入，请您重新输入。")

        elif current_ii == InteractiveInterface.about:
            print("---关于---")
            print_about_info()
            print()
            print_update_log()
            while True:
                print("A.返回主菜单")
                user_input = input("请输入：")
                print()

                if user_input == "":
                    print("您没有输入任何内容，请您重新输入。")

                elif user_input[0] == "A" or user_input[0] == "a":
                    current_ii = InteractiveInterface.main_menu
                    break

                else:
                    print("本程序未能理解您的输入，请您重新输入。")
