"""
目標：將謄本的特定資訊提取出後，使用表格呈現。
"""
import re, logging
from collections import OrderedDict
import pandas
from PyPDF2 import PdfReader

# Set logging config.
FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATE_FORMAT)

# Build container.
information_dict = OrderedDict()

pdf_reader = PdfReader("example.pdf")
pdf_page_num = len(pdf_reader.pages)
logging.info("PDF總頁數: " + str(pdf_page_num) + " 頁")

for i in range(1, pdf_page_num+1):
    information_dict[i] = dict()
    
    logging.info("PDF當前讀取頁數: 第 " + str(i) + " 頁")
    # 提取文字
    page_content = pdf_reader.pages[i-1].extract_text()
    
    # 尋找地段、地號或建號
    word_index = page_content.find("區")
    logging.debug(page_content[word_index-2:word_index+20].split("\n")[0])

    information_dict[i]["地段"] = page_content[word_index-2:word_index+20].split("\n")[0]
    
    # 尋找地土地面積
    area_index = page_content.find("面    積：******")
    logging.debug("面積索引位置：" + str(area_index))

    # 只儲存有效面積
    if area_index != -1:
        area = page_content[area_index+13:area_index+25].split("平方公尺\n")[0]
        information_dict[i]["面積"] = float(area)
        logging.debug("面積： " + str(area) + " 平方公尺")

    # 尋找土地使用分區和使用地類別
    use_kind_index = page_content.find("使用分區：")
    use_kind_detail_index = page_content.find("使用地類別：")
    logging.debug("使用分區位置索引值: " + str(use_kind_index))
    
    if use_kind_index != -1:
        use_kind = page_content[use_kind_index+5:use_kind_index+10]
        use_kind_detail = page_content[use_kind_detail_index+5:use_kind_detail_index+10]
        logging.debug("使用分區：" + use_kind)
        logging.debug("使用分區類別：" + use_kind_detail)

        information_dict[i]["使用分區"] = use_kind
        information_dict[i]["使用分區類別"] = use_kind_detail
    
    # 尋找公告土地現值
    land_value_index = page_content.find("公告土地現值：")
    logging.debug("公告土地現值位置索引值: " + str(land_value_index))
    
    if land_value_index != -1:
        land_value = page_content[land_value_index+7:land_value_index+25].split("元／平方公尺\n")[0].split('*')[-1]
        logging.debug("公告土地現值：" + land_value)

        information_dict[i]["公告土地現值"] = int(''.join(land_value.split(',')))

logging.debug(information_dict[1])