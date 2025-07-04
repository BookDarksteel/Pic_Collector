# Pic_Collector
# constants.py


PROGRAM_SINGLE_INSTANCE_LOCK_FILE_PATH = "psil.lock"

PIC_WAREHOUSE_INFO_FILE_PATH = "pic_warehouse_info.txt"
PIC_WAREHOUSE_INFO_FILE_HEAD = "图片仓库信息文件\n\
不建议通过直接修改此文件以修改Pic_Collector的数据仓库设置，\n\
如果却要修改此文件，请按照正确的方式修改以避免Pic_Collector不能正常工作，\n\
注意修改此文件可能但没有配套地修改其他相关设置文件或在Pic_Collector运行时修改此文件可能导致Pic_Collector不能正常工作。"

PIC_INFO_FILE_PATH = "pic_info.txt"
PIC_INFO_FILE_HEAD = "图片信息文件\n\
如果却要修改此文件，请按照正确的方式修改以避免Pic_Collector不能正常工作，\n\
注意Pic_Collector运行时修改此文件可能导致Pic_Collector不能正常工作。"

PIC_FOLDER_PATH = "pics"
DEFULT_RESULTS_FOLDER_PATH = "results_pic_copy"

INLINE_INFO_SEPARATOR = "、"

STYLE_LOWLIGHT = "\033[30;1m"
COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
STYLE_DEFULT = "\033[0m"
