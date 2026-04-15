# encoding:utf-8

import requests

'''
OCR-增值税发票验真
'''

'''
invoice_code 代码
invoice_date 日期
invoice_num 编号
total_amount 开票金额
invoice_type 发票类型 special_vat_invoice
'''
def check(invoice_code,invoice_date,invoice_num,total_amount,invoice_type,access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice_verification"
    params = {"check_code": "", "invoice_code":invoice_code, "invoice_date": invoice_date, "invoice_num":invoice_num,
              "invoice_type":invoice_type, "total_amount": total_amount}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        return response.json()

def getToken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=adL7AWIj4jidVzlcFHn4FzeF&client_secret=DGnVEfh40NLp0ptAIipXp681BQsIfbL3'
    response = requests.get(host)
    if response:
        # print(response.json())
        # print(response.json()["access_token"])
        return response.json()["access_token"]
if __name__ == '__main__':
    check()