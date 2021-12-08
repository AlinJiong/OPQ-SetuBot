from io import BytesIO
import requests
import httpx
import base64
import json
from PIL import Image, ImageFilter
import re

# url = "https://v2.alapi.cn/api/zaobao"
# payload = "token=EFolx1cxAdqqSWqy&format=json"
# headers = {'Content-Type': "application/x-www-form-urlencoded"}
# response = requests.request("POST", url, data=payload, headers=headers)
# text_to_dic = json.loads(response.text)
# img_url = text_to_dic['data']['image']

# print(img_url)
# content = httpx.get(img_url).content
# with BytesIO() as bf:
#     image = Image.open(BytesIO(content))
#     if image.format == 'WEBP':
#         image.save(bf, format="JPEG")
#         img = base64.b64encode(bf.getvalue()).decode()
#         print(img)

# url = "https://v2.alapi.cn/api/dog"
# payload = "token=EFolx1cxAdqqSWqy&format=json"
# headers = {'Content-Type': "application/x-www-form-urlencoded"}
# response = requests.request("POST", url, data=payload, headers=headers)
# text_to_dic = json.loads(response.text)
# print(text_to_dic['data'])
# content = text_to_dic['data']['content']
# print(content)


# url = "http://api.nmb.show/xiaojiejie1.php"
# content = requests.request("get", url).content
# with BytesIO() as bf:
#     image = Image.open(BytesIO(content))
#     image.save(bf, format="JPEG")
#     img = base64.b64encode(bf.getvalue()).decode()
#     print(img)


str_list = '''
{"Content":"\u003c?xml version='1.0' encoding='UTF-8' standalone='yes'?\u003e\u003cmsg templateID=\"123\" url=\"https://b23.tv/KdSp3tS?share_medium=android\u0026amp;share_source=qq\u0026amp;bbid=XXB8AC5BE894D54048AE47A6867AE6170B60B\u0026amp;ts=1638968909599\" serviceID=\"1\" action=\"web\" actionData=\"\" a_actionData=\"\" i_actionData=\"\" brief=\"[QQ小程序]哔哩哔哩\" flag=\"0\"\u003e\u003citem layout=\"2\"\u003e\u003cpicture cover=\"http://pubminishare-30161.picsz.qpic.cn/8651bcb5-6ce2-43dc-aae9-9b79c6bf21cd\"/\u003e\u003ctitle\u003e哔哩哔哩\u003c/title\u003e\u003csummary\u003e那天我戴着头套排队做核酸……社死了但没完全社死\u003c/summary\u003e\u003c/item\u003e\u003csource url=\"https://b23.tv/KdSp3tS?share_medium=android\u0026amp;share_source=qq\u0026amp;bbid=XXB8AC5BE894D54048AE47A6867AE6170B60B\u0026amp;ts=1638968909599\" icon=\"https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1638951012\" name=\"哔哩哔哩\" appid=\"0\" action=\"web\" actionData=\"\" a_actionData=\"tencent0://\" i_actionData=\"\"/\u003e\u003c/msg\u003e"}
'''

info = re.findall(r"(https://b23\.tv/\w*)", str_list)

for i in range(len(str_list.split("\""))):
    print(i, str_list.split("\"")[i])
# print(str_list.split("\\")[31])

img_url = str_list.split("\"")[24]
content = requests.request("get", img_url).content
with BytesIO() as bf:
    image = Image.open(BytesIO(content))
    image.save(bf, format="JPEG")
    img = base64.b64encode(bf.getvalue()).decode()
    print(img)
