# import requests
# import xml.etree.ElementTree as ET
#
#
# CB_URL = 'http://www.cbr.ru/scripts/XML_valFull.asp'
# response = requests.get(CB_URL)
#
# tree = ET.parse('index.xml')
# root = tree.getroot()
# currencies = list(root)
#
# currency_dict = {}
# currencies_list = []
# currency_tags = ['ISO_Char_Code', 'Name', 'EngName']
#
# for currency in currencies:
#     for elem in currency:
#         if elem.tag not in currency_tags:
#             continue
#         currency_dict[elem.tag] = elem.text
#     currencies_list.append(currency_dict)
#     currency_dict = {}
#
import requests
import xml.etree.ElementTree as ET

data_req1 = '2001-03-02'  # переделать на извлекаемые из введенной ссылки данные
data_req2 = '2001-03-14'

data_req1 = data_req1.split('-')
data_req2 = data_req2.split('-')
ISO_Num_Code = 'R01010'

CB_URL = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={data_req1[2]}/{data_req1[1]}/{data_req1[0]}" \
         f"&date_req2={data_req2[2]}/{data_req2[1]}/{data_req2[0]}&VAL_NM_RQ={ISO_Num_Code}"
response = requests.get(CB_URL)

tree = ET.fromstring(response.text)
quotation_list = list(tree)
quotation_list = [quotation_list[0], quotation_list[-1]]

quotation_dict_output = {}
quotation_dict = {}

data_req1 = '2001-03-02'  # переделать на извлекаемые из введенной ссылки данные
data_req2 = '2001-03-14'

# quotation_list_output = []
# for quotation in quotation_list:
#     print(quotation.attrib)
#     for num_id, elem in enumerate(quotation):
#         if elem.tag == 'Value':
#             print(num_id, elem.tag, elem.text)
#             elem.text = elem.text.replace(',', '.')
#         quotation_dict[elem.tag] = elem.text
#         quotation_list_output.append(quotation_dict)
#         quotation_dict = {}

# for quotation in quotation_list:
#     print(quotation.attrib)
#     for num_id, elem in enumerate(quotation):
#         if elem.tag == 'Value':
#             print(num_id, elem.tag, elem.text)
#             elem.text = elem.text.replace(',', '.')
#             quotation_dict[elem.tag] = elem.text
#         quotation_list_output[num_id] = quotation_dict
#     # quotation_dict = {}
num = 0
for quotation in quotation_list:
    for elem in quotation:
        if elem.tag == 'Value':
            elem.text = elem.text.replace(',', '.')
            quotation_dict[elem.tag] = elem.text
            quotation_dict['Date'] = quotation.attrib['Date']
            quotation_dict_output[num] = quotation_dict
            num += 1
        quotation_dict = {}
        quotation_dict_output['Id'] = quotation.attrib['Id']
print(quotation_dict_output)
