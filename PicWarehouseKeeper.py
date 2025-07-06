# Pic_Collector
# WarehouseKeeper.py

from copy import deepcopy
from os import mkdir, path, remove, rename
from shutil import copy, rmtree

from constants import *


class PicWarehouseKeeper(object):
    def __init__(self):
        self._pic_warehouse_name = ""
        self._user_defined_ordinary_fields = []
        self._num_user_defined_ordinary_field = 0
        self._user_defined_comment_fields = []
        self._num_user_defined_comment_field = 0
        self._pic_info_dict = {}
        self._import_fill_vacancy_num = False  # 导入图片时填补空缺编号设置项
        self._import_show_details = True  # 导入图片时显示细节设置项
        self._auto_sort_pic_id = True  # 自动整理图片编号设置项

        self._pwk_print("开始读取图片仓库信息...")
        with open(PIC_WAREHOUSE_INFO_FILE_PATH, "r", encoding="utf-8") as f:
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            self._pic_warehouse_name = f.readline()[:-1]
            self._user_defined_ordinary_fields = f.readline()[:-1].split(
                INLINE_INFO_SEPARATOR
            )
            self._num_user_defined_ordinary_field = len(
                self._user_defined_ordinary_fields
            )
            self._user_defined_comment_fields = f.readline()[:-1].split(
                INLINE_INFO_SEPARATOR
            )
            self._num_user_defined_comment_field = len(
                self._user_defined_comment_fields
            )
            f.readline()
            import_fill_vacancy_num_set_str = f.readline()[:-1].split("：")[1]
            if import_fill_vacancy_num_set_str == "T":
                self._import_fill_vacancy_num = True
            else:
                self._import_fill_vacancy_num = False
            import_show_details_str = f.readline()[:-1].split("：")[1]
            if import_show_details_str == "T":
                self._import_show_details = True
            else:
                self._import_show_details = False
            auto_sort_pic_id_str = f.readline()[:-1].split("：")[1]
            if auto_sort_pic_id_str == "T":
                self._auto_sort_pic_id = True
            else:
                self._auto_sort_pic_id = False
        self._pwk_print("图片仓库信息读取完成")

        self._pwk_print("开始读取图片信息...")
        with open(PIC_INFO_FILE_PATH, "r", encoding="utf-8") as f:
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            while True:
                pic_id_str = f.readline()[:-1]
                if pic_id_str == "":
                    break
                pic_id = int(pic_id_str)
                self._pic_info_dict[pic_id] = {}
                pic_file_name = f.readline()[:-1].split("：")[1]
                self._pic_info_dict[pic_id]["文件名"] = pic_file_name
                for i in range(self._num_user_defined_ordinary_field):
                    value = f.readline()[:-1].split("：")[1]
                    self._pic_info_dict[pic_id][
                        self._user_defined_ordinary_fields[i]
                    ] = value
                tags_str = f.readline()[:-1].split("：")[1]
                self._pic_info_dict[pic_id]["标签"] = tags_str.split(
                    INLINE_INFO_SEPARATOR
                )
                for i in range(self._num_user_defined_comment_field):
                    num_comment_line = int(f.readline()[:-1].split("：")[1])
                    comment = ""
                    for _ in range(num_comment_line):
                        comment += f.readline()
                    self._pic_info_dict[pic_id][
                        self._user_defined_comment_fields[i]
                    ] = comment[:-1]
                f.readline()
            sorted(self._pic_info_dict)
        self._pwk_print("图片信息读取完成")

        if self._auto_sort_pic_id:
            self._sort_pic_number()
            self._pwk_print("图片编号整理完成")

    def _get_new_pic_id(self):
        """
        获取新导入的图片的编号
        本函数将根据导入图片时填补空缺编号设置项给出当前情况下下一张新导入的图片的编号。
        返回值：下一张新导入的图片的编号。
        """
        new_pic_id = -1
        if self._import_fill_vacancy_num:
            new_pic_id = 1
            while True:
                if new_pic_id not in self._pic_info_dict.keys():
                    break
                new_pic_count += 1
        else:
            biggest_pic_id = 0
            for pic_id in self._pic_info_dict.keys():
                if pic_id > biggest_pic_id:
                    biggest_pic_id = pic_id
            new_pic_id = biggest_pic_id + 1
        return new_pic_id

    def _modify_pic_id(self, old_pic_id, target_pic_id):
        """
        修改图片编号
        本函数会修改图片编号，执行操作包括修改图片文件名和self._pic_info_dict中的图片信息。
        参数old_pic_id：要修改编号的图片的当前编号；
        参数target_pic_id：要修改编号的图片的修改目标编号。
        无返回值。
        """
        old_pic_path = PIC_FOLDER_PATH + "/" + self._pic_info_dict[old_pic_id]["文件名"]
        pic_file_extension = self._pic_info_dict[old_pic_id]["文件名"].split(".")[-1]
        target_pic_path = (
            PIC_FOLDER_PATH + "/" + str(target_pic_id) + "." + pic_file_extension
        )
        rename(old_pic_path, target_pic_path)
        self._pic_info_dict[target_pic_id] = self._pic_info_dict[old_pic_id]
        del self._pic_info_dict[old_pic_id]
        self._pic_info_dict[target_pic_id]["文件名"] = (
            str(target_pic_id) + "." + pic_file_extension
        )

    def _pwk_print(self, content):
        print(STYLE_LOWLIGHT + content + STYLE_DEFULT)

    def _sort_pic_number(self):
        """
        整理图片编号
        整理使得图片仓库中的所有的图片的编号从1开始连续编排，会更新图片信息文件内容。
        无返回值。
        """
        num_pic = len(self._pic_info_dict)
        pic_info_dict_keys_view = self._pic_info_dict.keys()
        check_pointer = 1
        while check_pointer <= num_pic:
            if check_pointer not in pic_info_dict_keys_view:
                next_id = check_pointer + 1
                while next_id not in pic_info_dict_keys_view:
                    next_id += 1
                self._modify_pic_id(next_id, check_pointer)  # 修改图片编号
            check_pointer += 1
        self._update_pic_info_file()

    def _update_pic_info_file(self):
        """
        更新图片信息文件
        利用当前self._pic_info_dict中存储的图片信息更新图片信息文件。
        无返回值。
        """
        with open(PIC_INFO_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(PIC_INFO_FILE_HEAD)
            f.write("\n\n")
            for pic_id in sorted(self._pic_info_dict.keys()):
                f.write(str(pic_id) + "\n")
                f.write("文件名：" + self._pic_info_dict[pic_id]["文件名"] + "\n")
                for field in self._user_defined_ordinary_fields:
                    f.write(field + "：" + self._pic_info_dict[pic_id][field] + "\n")
                tags_info_line_str = "标签："
                for tag in self._pic_info_dict[pic_id]["标签"]:
                    tags_info_line_str += tag + INLINE_INFO_SEPARATOR
                f.write(tags_info_line_str[:-1] + "\n")
                for field in self._user_defined_comment_fields:
                    if self._pic_info_dict[pic_id][field] == "":
                        f.write(field + "：0\n")
                    else:
                        f.write(
                            field
                            + "："
                            + str(self._pic_info_dict[pic_id][field].count("\n") + 1)
                            + "\n"
                        )
                        f.write(self._pic_info_dict[pic_id][field] + "\n")
                f.write("\n")

    def _update_pic_warehouse_info_file(self):
        """
        更新图片仓库信息文件
        利用当前运行中的Pic_Collector程序中保存的图片仓库信息更新图片仓库信息文件。
        无返回值。
        """
        with open(PIC_WAREHOUSE_INFO_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(PIC_WAREHOUSE_INFO_FILE_HEAD)
            f.write("\n\n")
            f.write(self._pic_warehouse_name + "\n")
            user_defined_ordinary_fields_str = ""
            for field in self._user_defined_ordinary_fields:
                user_defined_ordinary_fields_str += field + INLINE_INFO_SEPARATOR
            f.write(user_defined_ordinary_fields_str[:-1])
            f.write("\n")
            user_defined_comment_fields_str = ""
            for field in self._user_defined_comment_fields:
                user_defined_comment_fields_str += field + INLINE_INFO_SEPARATOR
            f.write(user_defined_comment_fields_str[:-1])
            f.write("\n\n")
            if self._import_fill_vacancy_num:
                f.write("导入图片时填补空缺编号：T\n")
            else:
                f.write("导入图片时填补空缺编号：F\n")
            if self._import_show_details:
                f.write("导入图片时显示细节：T\n")
            else:
                f.write("导入图片时显示细节：F\n")
            if self._auto_sort_pic_id:
                f.write("自动整理图片编号：T\n")
            else:
                f.write("自动整理图片编号：F\n")

    def add_user_defined_comment_fields(self, new_comment_fields):
        """
        在图片仓库中添加备注字段
        参数new_comment_fields：要添加的新备注字段名称组成的列表，注意应保证这个列表中不存在不支持或图片仓库中已存在的字段名称。
        无返回值
        """
        self._user_defined_comment_fields += new_comment_fields
        self._num_user_defined_comment_field = len(self._user_defined_comment_fields)
        for pic_id in self._pic_info_dict.keys():
            for field in new_comment_fields:
                self._pic_info_dict[pic_id][field] = ""
        self._update_pic_warehouse_info_file()
        self._update_pic_info_file()
        self._pwk_print("成功添加" + str(len(new_comment_fields)) + "个备注字段")

    def add_user_defined_ordinary_fields(self, new_ordinary_fields):
        """
        在图片仓库中添加用户定义普通字段
        参数new_ordinary_fields：要添加的新用户定义普通字段名称组成的列表，注意应保证这个列表中不存在不支持或图片仓库中已存在的字段名称。
        无返回值
        """
        self._user_defined_ordinary_fields += new_ordinary_fields
        self._num_user_defined_ordinary_field = len(self._user_defined_ordinary_fields)
        for pic_id in self._pic_info_dict.keys():
            for field in new_ordinary_fields:
                self._pic_info_dict[pic_id][field] = ""
        self._update_pic_warehouse_info_file()
        self._update_pic_info_file()
        self._pwk_print("成功添加" + str(len(new_ordinary_fields)) + "个普通字段")

    def common_field_file_name_search(self, search_term_dict):
        """
        按普通字段和文件名搜索
        将在图片库中搜索成功匹配给定的所有搜索信息的图片。
        搜索匹配范围包括图片仓库中所有图片的文件名和用户定义的图片信息普通字段。
        参数search_term_dict：给定的搜索信息字典，该字典的键可以为“"文件名"”或用户定义的图片信息普通字段；
        返回值：搜索结果，类型为列表，其中每一项对应一个搜索结果且也是一个列表，其中第0项为搜索结果图片的编号，第1项为搜索结果图片的信息字典，第3项目为搜索结果图片的匹配信息。
        """
        self._pwk_print("开始搜索...")
        results = []
        for pic_id in self._pic_info_dict.keys():
            matching = True
            for field in self._pic_info_dict[pic_id]:
                if field in self._user_defined_comment_fields or field=="标签":
                    continue
                else:
                    if field in search_term_dict.keys():
                        if (
                            self._pic_info_dict[pic_id][field].lower()
                            != search_term_dict[field].lower()
                        ):
                            matching = False
            if matching:
                results.append(
                    [
                        pic_id,
                        deepcopy(self._pic_info_dict[pic_id]),
                        ["文件名"]+self.get_user_defined_ordinary_fields()
                    ]
                )
        self._pwk_print("搜索完成")
        return results

    def check_pic_exist(self, pic_id):
        """
        检查图片仓库中是否存在给定编号对应的图片
        参数pic_id：给定图片编号。
        返回值：若图片仓库中存在给定编号对应的图片则返回True，反之则返回False。
        """
        return pic_id in self._pic_info_dict.keys()

    def copy_pics(self, pic_ids, target_folder_path):
        """
        复制图片到目标文件夹
        参数pic_ids：要被复制的图片的编号列表；
        参数target_folder_path：复制目标文件夹路径。
        无返回值。
        """
        self._pwk_print("开始复制...")
        copy_pic_count = 0
        for pic_id in pic_ids:
            copy(
                PIC_FOLDER_PATH + "/" + self._pic_info_dict[pic_id]["文件名"],
                target_folder_path,
            )
            copy_pic_count += 1
        self._pwk_print("复制成功（共复制" + str(copy_pic_count) + "张图片）")

    def del_user_defined_comment_fields(self, del_comment_fields):
        """
        在图片仓库中删除备注字段
        参数del_comment_fields：要删除的备注字段名称组成的列表，注意应保证这个列表中的字段名称均为图片仓库中已存在的备注字段名称且在图片仓库中删除这个列表指定的备注字段后还剩余至少一个备注字段。
        无返回值
        """
        for field in del_comment_fields:
            self._user_defined_comment_fields.remove(field)
        self._num_user_defined_comment_field = len(self._user_defined_comment_fields)
        for pic_id in self._pic_info_dict.keys():
            for field in del_comment_fields:
                del self._pic_info_dict[pic_id][field]
        self._update_pic_warehouse_info_file()
        self._update_pic_info_file()
        self._pwk_print("成功删除" + str(len(del_comment_fields)) + "个备注字段")

    def del_user_defined_ordinary_fields(self, del_ordinary_fields):
        """
        在图片仓库中删除用户定义普通字段
        参数del_ordinary_fields：要删除的用户定义普通字段名称组成的列表，注意应保证这个列表中的字段名称均为图片仓库中已存在的用户定义普通字段名称。
        无返回值
        """
        for field in del_ordinary_fields:
            self._user_defined_ordinary_fields.remove(field)
        self._num_user_defined_ordinary_field = len(self._user_defined_ordinary_fields)
        for pic_id in self._pic_info_dict.keys():
            for field in del_ordinary_fields:
                del self._pic_info_dict[pic_id][field]
        self._update_pic_warehouse_info_file()
        self._update_pic_info_file()
        self._pwk_print("成功删除" + str(len(del_ordinary_fields)) + "个普通字段")

    def delete_all_pics(self):
        """
        删除图片仓库中的所有图片
        无返回值。
        """
        self._pwk_print("开始删除图片仓库中的所有图片...")
        rmtree(PIC_FOLDER_PATH)
        mkdir(PIC_FOLDER_PATH)
        self._pic_info_dict = {}
        self._update_pic_info_file()
        self._pwk_print("已删除图片仓库中的所有图片")

    def delete_pic(self, pic_id):
        """
        删除指定图片
        参数pic_id：要删除的图片的编号。
        无返回值。
        """
        remove(PIC_FOLDER_PATH + "/" + self._pic_info_dict[pic_id]["文件名"])
        del self._pic_info_dict[pic_id]
        if self._auto_sort_pic_id:
            self._sort_pic_number()  # 调用的这个函数会执行self._update_pic_info_file()。
        else:
            self._update_pic_info_file()
        self._pwk_print("已删除编号为" + str(pic_id) + "的图片")

    def export_pics_info(self, target_txt_path):
        """
        导出图片信息
        导出图片信息到指定文件。
        参数target_txt_path：导出图片信息目标文件路径，应为txt文件路径。
        无返回值
        """
        self._update_pic_info_file()
        self._pwk_print("开始导出图片信息...")
        with open(target_txt_path, "w", encoding="utf-8") as f:
            for pic_id in sorted(self._pic_info_dict.keys()):
                f.write(str(pic_id) + "\n")
                f.write("文件名：" + self._pic_info_dict[pic_id]["文件名"] + "\n")
                for field in self._user_defined_ordinary_fields:
                    f.write(field + "：" + self._pic_info_dict[pic_id][field] + "\n")
                tags_info_line_str = "标签："
                for tag in self._pic_info_dict[pic_id]["标签"]:
                    tags_info_line_str += tag + INLINE_INFO_SEPARATOR
                f.write(tags_info_line_str[:-1] + "\n")
                for field in self._user_defined_comment_fields:
                    if self._pic_info_dict[pic_id][field] == "":
                        f.write(field + "：0\n")
                    else:
                        f.write(
                            field
                            + "："
                            + str(self._pic_info_dict[pic_id][field].count("\n") + 1)
                            + "\n"
                        )
                        f.write(self._pic_info_dict[pic_id][field] + "\n")
                f.write("\n")
        self._pwk_print("图片信息导出成功")

    def fast_search(self, search_term):
        """
        快速搜索
        对给定的单个搜索关键词在图片仓库中进行快速搜索。
        搜索范围包括图片仓库中所有图片的编号、用户定义的图片信息普通字段和标签，不包括图片的文件名和备注字段。
        参数search_term：给定的单个搜索关键词，应为字符串类型；
        返回值：搜索结果，类型为列表，其中每一项对应一个搜索结果且也是一个列表，其中第0项为搜索结果图片的编号，第1项为搜索结果图片的信息字典，第3项目为搜索结果图片的匹配信息。
        """
        self._pwk_print("开始搜索...")
        search_term = search_term.lower()
        results = []
        search_term_figure = -1
        if search_term.isdigit():
            search_term_figure = int(search_term)
        for pic_id in self._pic_info_dict.keys():
            matching = False
            matching_info = []
            if pic_id == search_term_figure:
                matching = True
                matching_info.append("编号")
            for field in self._pic_info_dict[pic_id].keys():
                if field == "标签":
                    for tag in self._pic_info_dict[pic_id][field]:
                        if tag.lower() == search_term:
                            matching = True
                            matching_info.append("【标签】" + tag)
                            break
                elif field == "文件名":
                    continue
                elif field in self._user_defined_comment_fields:
                    continue
                else:
                    if self._pic_info_dict[pic_id][field].lower() == search_term:
                        matching = True
                        matching_info.append(field)
            if matching:
                results.append(
                    [pic_id, deepcopy(self._pic_info_dict[pic_id]), matching_info]
                )
        self._pwk_print("搜索完成")
        return results

    def get_all_ids(self):
        """
        获取图片仓库中所有图片的编号
        返回值：图片仓库中所有图片的编号组成的列表。
        """
        return list(self._pic_info_dict.keys())

    def get_auto_sort_pic_id(self):
        """
        获取 自动整理图片编号 设置项的设置
        返回值：自动整理图片编号设置项的设置，为True或False。
        """
        return self._auto_sort_pic_id

    def get_biggest_pic_id(self):
        """
        获取图片仓库中最大的图片编号
        返回值：图片仓库中最大的图片编号。
        """
        biggest_pic_id = 0
        for pic_id in self._pic_info_dict.keys():
            if pic_id > biggest_pic_id:
                biggest_pic_id = pic_id
        return biggest_pic_id

    def get_import_fill_vacancy_num(self):
        """
        获取 导入图片时填补空缺编号 设置项的设置
        返回值：导入图片时填补空缺编号设置项的设置，为True或False。
        """
        return self._import_fill_vacancy_num

    def get_import_show_details(self):
        """
        获取 导入图片时显示细节 设置项的设置
        返回值：导入图片时显示细节设置项的设置，为True或False。
        """
        return self._import_show_details

    def get_num_pic(self):
        """
        获取图片仓库中的图片数量
        返回值：图片仓库中的图片数量。
        """
        return len(self._pic_info_dict)

    def get_pic_info(self, pic_id):
        """
        获取给定的编号对应的图片的信息
        参数pic_id：给定的编号。
        返回值：给定的编号对应的图片的信息，为一个列表，列表第0项为图片编号，第1项为图片信息字典。
        """
        return [pic_id, deepcopy(self._pic_info_dict[pic_id])]

    def get_user_defined_comment_fields(self):
        """
        获取用户定义的图片信息备注字段
        返回值：用户定义的图片信息备注字段名称列表（经深拷贝）。
        """
        return deepcopy(self._user_defined_comment_fields)

    def get_user_defined_ordinary_fields(self):
        """
        获取用户定义的图片信息普通字段
        返回值：用户定义的图片信息普通字段名称列表（经深拷贝）。
        """
        return deepcopy(self._user_defined_ordinary_fields)

    def get_warehouse_name(self):
        """
        获取图片仓库名称
        返回值：图片仓库名称。
        """
        return self._pic_warehouse_name

    def import_pics(self, pic_paths, pic_info_list):
        """
        导入图片
        本函数负责将给定图片导入图片仓库并记录给定信息。
        导入是将给定图片复制到图片仓库。
        参数pic_paths：要导入的图片的路径列表；
        参数pic_info_list：要导入的图片的信息列表，列表的每一项应为一个描述一张图片信息的字典，需与参数pic_paths中的路径对应的图片一一对应。
        无返回值。
        """
        self._pwk_print("开始导入图片...")
        import_pic_count = 0
        for i in range(len(pic_paths)):
            new_pic_id = self._get_new_pic_id()
            _, new_pic_name_extension = path.splitext(pic_paths[i])
            imported_pic_filename = str(new_pic_id) + new_pic_name_extension
            self._pic_info_dict[new_pic_id] = pic_info_list[i]
            self._pic_info_dict[new_pic_id]["文件名"] = imported_pic_filename
            copy(pic_paths[i], PIC_FOLDER_PATH + "/" + imported_pic_filename)
            import_pic_count += 1
            if self._import_show_details:
                self._pwk_print(
                    "成功导入第"
                    + str(import_pic_count)
                    + "张图片  图片被分配的编号："
                    + str(new_pic_id)
                    + "  图片源地址："
                    + pic_paths[i]
                )
        self._update_pic_info_file()
        self._pwk_print("导入完成（共导入" + str(import_pic_count) + "张图片）")

    def modify_pic_info(self, pic_id, new_info_dict):
        """
        修改指定图片信息
        参数pic_id：指定的图片的编号；
        参数new_info_dict：新的指定图片信息。
        无返回值。
        """
        self._pic_info_dict[pic_id] = new_info_dict
        self._update_pic_info_file()
        self._pwk_print("成功修改编号为" + str(pic_id) + "的图片的信息")

    def modify_pic_warehouse_name(self, new_pic_warehouse_name):
        """
        修改图片仓库名称
        参数new_pic_warehouse_name：新图片仓库名称
        无返回值。
        """
        self._pic_warehouse_name = new_pic_warehouse_name
        self._update_pic_warehouse_info_file()
        self._pwk_print("已成功修改图片仓库名称")

    def set_auto_sort_pic_id(self, v):
        """
        设置 自动整理图片编号 设置项的设置
        参数v：将自动整理图片编号设置项改为的设置，应为True或False。
        无返回值。
        """
        self._auto_sort_pic_id = v
        self._update_pic_warehouse_info_file()
        if self._auto_sort_pic_id:
            self._sort_pic_number()  # 调用的这个函数会执行self._update_pic_info_file()。
        self._pwk_print(
            "自动整理图片编号设置项设置为" + str(self._auto_sort_pic_id) + "。"
        )

    def set_import_fill_vacancy_num(self, v):
        """
        设置 导入图片时填补空缺编号 设置项的设置
        参数v：将导入图片时填补空缺编号设置项改为的设置，应为True或False。
        无返回值。
        """
        self._import_fill_vacancy_num = v
        self._update_pic_warehouse_info_file()
        self._pwk_print(
            "导入图片时填补空缺编号设置项设置为"
            + str(self._import_fill_vacancy_num)
            + "。"
        )

    def set_import_show_details(self, v):
        """
        设置 导入图片时显示细节 设置项的设置
        参数v：将导入图片时显示细节设置项改为的设置，应为True或False。
        无返回值。
        """
        self._import_show_details = v
        self._update_pic_warehouse_info_file()
        self._pwk_print(
            "导入图片时显示细节设置项设置为" + str(self._import_show_details) + "。"
        )

    def tag_search(self,and_or_flag,search_tags):
        """
        按标签搜索
        参数and_or_flag：若为True则搜索图片仓库中拥有search_tags中的所有标签的图片；若为False则搜索图片仓库中拥有search_tags中的任意至少一个标签的图片；
        参数search_tags：希望搜索的标签组成的列表，注意这个列表不应为空列表。
        返回值：搜索结果，类型为列表，其中每一项对应一个搜索结果且也是一个列表，其中第0项为搜索结果图片的编号，第1项为搜索结果图片的信息字典，第3项目为搜索结果图片的匹配信息。
        """
        self._pwk_print("开始搜索...")
        for tag_i in range(len(search_tags)):
            search_tags[tag_i]=search_tags[tag_i].lower()
        results = []

        if and_or_flag:
            for pic_id in self._pic_info_dict.keys():
                matching = True
                pic_tags_lower=[]
                for tag in self._pic_info_dict[pic_id]["标签"]:
                    pic_tags_lower.append(tag.lower())
                for tag in search_tags:
                    if tag not in pic_tags_lower:
                        matching=False
                        break
                if matching:
                    results.append([pic_id, deepcopy(self._pic_info_dict[pic_id]), ["标签"]])

        else:
            for pic_id in self._pic_info_dict.keys():
                pic_tags_lower=[]
                for tag in self._pic_info_dict[pic_id]["标签"]:
                    pic_tags_lower.append(tag.lower())
                for tag in search_tags:
                    if tag in pic_tags_lower:
                        results.append([pic_id, deepcopy(self._pic_info_dict[pic_id]), ["标签"]])
                        break

        self._pwk_print("搜索完成")
        return results

