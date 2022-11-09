from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals import get_festival
import datetime
from botoy import Action
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.schedule import scheduler
import requests
import re
__doc__ = "摸鱼提醒（auto)"


def get_nums():
    new_date = datetime.date.today().strftime('%Y年%m月%d日')
    today = LunarDate.today()
    lunardate = today.strftime('%L%M月%D')

    festivals_zh = ['清明', '劳动节', '端午节', '中秋节', '国庆节', '元旦', '春节']
    festivals_zh2 = ['清明节', '劳动节', '端午节', '中秋节', '国庆节', '元旦节', '春节']

    festivals_num = []
    for festival in festivals_zh:
        festivals_num.append(get_festival(festival).countdown())

    festivals = list(zip(festivals_zh2, festivals_num))

    # 获取农历节假日，并排序
    festivals.sort(key=lambda x: x[1])

    res = []

    for item in festivals:
        res.append(item)
        if item[0] == '春节':
            break

    s1 = "今天是%s, 农历%s,早上好,摸鱼人！\n工作再累,一定不要忘记摸鱼哦！有事没事起身去茶水间,去厕所,去廊道走走别老在工位上坐着,钱是老板的, 但命是自己的。\n" % (
        new_date, lunardate)

    s2 = ''
    for i in res:
        s2 += '距离%s还有%d天,\n' % (i[0], i[1])

    virus_begin = datetime.datetime(2019, 12, 16)
    virus_ = datetime.datetime.today()
    s2 += '【新冠】至今已有%d天！\n' % (virus_-virus_begin).days

    s3 = '''上班是帮老板赚钱,摸鱼是赚老板的钱！最后,祝愿天下所有摸鱼人,都能愉快的渡过每一天......
【友情提示】三甲医院ICU躺一天平均费用大概一万块,你晚一天进ICU,就等于为你的家庭多赚一万块。少上班,多摸鱼！！！'''

    s = s1+s2+s3

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
               'Content-Type': "application/x-www-form-urlencoded"}

    url = 'https://api.j4u.ink/v1/store/other/proxy/remote/moyu.json'

    content = requests.get(url, headers=headers, timeout=10)
    img_url = re.findall(r'https:.*?png', content.text)[0].replace('\\', '')
    action = Action(qq=jconfig.bot)
    action.sendGroupPic(773933325,
                        picUrl=img_url,
                        content=s)


job1 = scheduler.add_job(get_nums, 'cron', hour=9, minute=10)
