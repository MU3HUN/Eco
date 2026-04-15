from paddleocr import PaddleOCR, draw_ocr
import re

def runOrc(self,path):
    #ocr = PaddleOCR()  # need to run only once to download and load model into memory
    ocr = PaddleOCR(rec_model_dir=r'E:\paddleOrcModel\rec',
                    cls_model_dir=r'E:\paddleOrcModel\cls',
                    det_model_dir=r'E:\paddleOrcModel\det')
    #img_path = r"E:\InvoicePics\fapiao.jpg";
    img_path = path;
    result = ocr.ocr(img_path)
    inform = [];
    for line in result:
        # print(line)
        inform.append(line[1][0])
    String2 = '【' + '】【'.join(inform) + '】';
    print(String2)
    if '发' in String2 or '票' in String2:
        invoice2 = re.sub('[a-zA-Z]', '', String2);
        # 公司
        try:
            inform_reverse =inform[::-1];#倒叙取到的所有信息
            for item in inform_reverse:
                if('公司' in item):
                    self.gongsi = item
                    break
        except:
            self.gongsi = ""
        # 发票号码
        try:
            self.number = re.findall('【([0-9]{8})】', invoice2)[0]
        except:
            self.number = ""


        # 发票代码
        try:
            self.daima = re.findall('【([0-9]{10,12})】', invoice2)[0];
        except:
            self.daima = '';
        # 发票日期
        try:
            patter = '([0-9]*[年|月].*?)】'
            dateo = re.findall(patter, invoice2)[0]
            year = ''.join(re.findall('(2020)|(2021)|(2022)|(2023)|(2024)|(2025)|(2026)|(2027)|(2028)|(2029)|(2030)', dateo)[0])
            #month = ''.join(re.findall('(01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)', dateo)[0])
            month=dateo[5:-4]
            date = dateo[-3:-1]
            self.ymd = year + month + date;
        except:
            self.ymd = '';
        # 发票金额
        try:
            amounts = re.findall('([0-9]*?\..*?)】', invoice2);
            arr_clean = list()
            # 去掉非数字的字符
            for elm in amounts:
                try:
                    float(elm)
                    print("could     convert string to float:", elm)
                    arr_clean.append(elm)
                except ValueError as e:
                    print(e)
            amounts = [float(i) for i in arr_clean];
            amounts.sort();
            # 取重复的一个数字,如果不存在取第二大的数字
            for i in range(1, len(amounts)):
                if amounts[i] == amounts[i - 1]:
                    self.amount = amounts[i]
                else:self.amount = amounts[-2];
        except:
            self.amount = 0
        self.OneModel = [self.number, self.daima, self.ymd, self.amount,self.gongsi];
        print(self.OneModel)
    return self.OneModel
