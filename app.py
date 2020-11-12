from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
CB_URL = 'http://www.cbr.ru/scripts/XML_valFull.asp'


@app.route('/', methods=['GET'])
def get_all_currencies():
    response = requests.get(CB_URL)
    tree = ET.fromstring(response.text)
    currencies = list(tree)

    currency_dict = {}
    currencies_list = []
    currency_tags = ['ISO_Char_Code', 'Name', 'EngName']

    for currency in currencies:
        for elem in currency:
            if elem.tag not in currency_tags:
                continue
            currency_dict[elem.tag] = elem.text
        currencies_list.append(currency_dict)
        currency_dict = {}

    return jsonify({"currencies_list": currencies_list})


@app.route('/<iso_num_code>_<data1>_<data2>/', methods=['GET'])
def get_difference(iso_num_code, data1, data2):
    data_req1 = data1.split('-')
    data_req2 = data2.split('-')

    CB_URL = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={data_req1[2]}/{data_req1[1]}/{data_req1[0]}" \
             f"&date_req2={data_req2[2]}/{data_req2[1]}/{data_req2[0]}&VAL_NM_RQ={iso_num_code}"
    response = requests.get(CB_URL)

    tree = ET.fromstring(response.text)
    quotation_list = list(tree)
    quotation_list = [quotation_list[0], quotation_list[-1]]
    quotation_dict_output = {}
    quotation_dict = {}

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

    quotation_dict_output['difference'] = float(quotation_dict_output[0]['Value']) - \
                                          float(quotation_dict_output[1]['Value'])

    return quotation_dict_output


if __name__ == '__main__':
    app.run(debug=True)
