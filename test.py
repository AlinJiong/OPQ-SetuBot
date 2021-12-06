from io import BytesIO
import requests
import httpx
import base64
import json
from PIL import Image, ImageFilter

url = "https://v2.alapi.cn/api/zaobao"
payload = "token=EFolx1cxAdqqSWqy&format=json"
headers = {'Content-Type': "application/x-www-form-urlencoded"}
response = requests.request("POST", url, data=payload, headers=headers)
text_to_dic = json.loads(response.text)
img_url = text_to_dic['data']['image']

print(img_url)
content = httpx.get(img_url).content
with BytesIO() as bf:
    image = Image.open(BytesIO(content))
    if image.format == 'WEBP':
        image.save(bf, format="JPEG")
        img = base64.b64encode(bf.getvalue()).decode()
        print(img)
        
