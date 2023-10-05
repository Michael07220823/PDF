import re
import logging
from PyPDF2 import PdfReader

# Set logging config.
FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATE_FORMAT)

# Read PDF file.
pdf_reader = PdfReader("example.pdf")
pdf_pages = len(pdf_reader.pages)

# RE role build.
topic_role = re.compile(r"..登記第二類謄本", flags=re.S)
land_title_role = re.compile(r"..區..段.*?地號", flags=re.M)
building_title_role = re.compile(r"..區..段.*?建號", flags=re.M)
# 土地標示部
land_area_role = re.compile(r"面.*?平方公尺", flags=re.S)
building_area_role = re.compile(r"總.*?平方公尺", flags=re.S)
use_kind_role = re.compile(r"使用分區............")
use_kind_detail_role = re.compile(r"使用地類別............")
land_value_role = re.compile(r"公告土地現值.*?平方公尺")
# 土地所有權部
# registration_date_role = re.compile(r"登記日期.*?日")
caues_date_role = re.compile(r"原因發生日期.*?日")
owner_role = re.compile(r"所有權人：..........")
id_num_role = re.compile(r"統一編號：..........")
address_role = re.compile(r"住.*?址：....................")
scope_role = re.compile(r"權利範圍：.*?\d..\d")



for page in range(1, pdf_pages+1):
    # Read content from PDF.
    pdf_content = pdf_reader.pages[page-1].extract_text()
    # logging.debug(pdf_content)

    # Search data.
    # Search land or building.
    topic = topic_role.search(pdf_content)
    if topic != None:
        topic = topic.group()[:2]
        logging.debug(topic + " 謄本" + "第" + str(page) + "頁")
    else:
        logging.debug("**" + " 謄本" + "第" + str(page) + "頁")


    # Search 區域地段第號
    land_title = land_title_role.search(pdf_content)
    if land_title != None:
        land_title = land_title.group()
        logging.debug("地段地號: " + land_title)
    else:
        logging.debug("地段地號: None")
    
    # Search 區域地段建號
    building_title = building_title_role.search(pdf_content)
    if building_title != None:
        building_title = building_title.group()
        logging.debug("地段建號: " + building_title)
    else:
        logging.debug("地段建號: None")

    # 土地標示部
    # Search Area.
    if topic == "土地":
        land_area = land_area_role.search(pdf_content)
        if land_area != None:
            land_area = land_area.group()[6:]
            logging.debug("面積： " + land_area)
        else:
            logging.debug("面積： None")
    else:
        building_area = building_area_role.search(pdf_content)
        if building_area != None:
            building_area = building_area.group()[4:]
            logging.debug("總面積： " + building_area)
        else:
            logging.debug("總面積： None")

    # Search use land kind
    use_kind = use_kind_role.search(pdf_content)
    if use_kind != None:
        use_kind = use_kind.group()[5:]
        logging.debug("使用分區： " + use_kind)
    else:
        logging.debug("使用分區： None")
    
    # Search use land kind detail.
    # use_kind_detail = use_kind_detail_role.search(pdf_content)
    # if use_kind_detail != None:
    #     use_kind_detail = use_kind_detail.group()
    #     logging.debug("使用地類別： " + use_kind_detail)
    # else:
    #     logging.debug("使用地類別： None")
    
    # Search land value.
    land_value = land_value_role.search(pdf_content)
    if land_value != None:
        land_value = land_value.group()[7:]
        logging.debug("公告土地現值： " + land_value)
    else:
        logging.debug("公告土地現值： None")

    # 土地所有權部
    # Search 登記日期
    # registration_date = registration_date_role.search(pdf_content)
    # if registration_date != None:
    #     registration_date = registration_date.group()[5:]
    #     logging.debug("登記日期： " + registration_date)
    # else:
    #     logging.debug("登記日期： None")
    
    # Search 原因發生日期
    caues_date = caues_date_role.search(pdf_content)
    if caues_date != None:
        caues_date = caues_date.group()[7:]
        logging.debug("原因發生日期： " + caues_date)
    else:
        logging.debug("原因發生日期： None")
    
    # Search 所有權人
    owner = owner_role.search(pdf_content)
    if owner != None:
        owner = owner.group()[5:]
        logging.debug("所有權人： " + owner)
    else:
        logging.debug("所有權人： None")
    
    # Search 統一編號
    id_num = id_num_role.search(pdf_content)
    if id_num != None:
        id_num = id_num.group()[5:]
        logging.debug("統一編號： " + id_num)
    else:
        logging.debug("統一編號： None")
    
    # Search 住址
    address = address_role.search(pdf_content)
    if address != None:
        address = address.group()[5:]
        logging.debug("住址： " + address)
    else:
        logging.debug("住址： None")
    
    # Search 住址
    scope = scope_role.search(pdf_content)
    if scope != None:
        scope = scope.group()[17:]
        logging.debug("權利範圍： " + scope)
    else:
        logging.debug("權利範圍： None")


    # 分隔每筆地號建號
    logging.debug("*"*50)