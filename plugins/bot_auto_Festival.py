from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals import get_festival
import datetime
from botoy import Action
from botoy import FriendMsg, GroupMsg, S, jconfig, logger
from botoy.schedule import scheduler

__doc__ = "发送摸鱼提醒"


def takeSecond(elem):
    return elem[1]


def get_nums():
    new_date = datetime.date.today().strftime('%Y年%m月%d日')
    today = LunarDate.today()
    lunardate = today.strftime('%L%M月%D')

    Festivals_ch = ['清明', '端午节', '中秋节', '国庆节', '元旦', '春节']
    Festivals_ch2 = ['清明节', '端午节', '中秋节', '国庆节', '元旦节', '春节']
    Festivals_num = []
    for festival in Festivals_ch:
        Festivals_num.append(get_festival(festival).countdown())

    Festivals = list(zip(Festivals_ch2, Festivals_num))

    # 获取农历节假日，并排序
    Festivals.sort(key=takeSecond)

    s1 = "今天是%s, 农历%s,早上好,摸鱼人！\n工作再累,一定不要忘记摸鱼哦！有事没事起身去茶水间,去厕所,去廊道走走别老在工位上坐着,钱是老板的, 但命是自己的。\n" % (
        new_date, lunardate)

    s2 = ''
    for i in Festivals:
        s2 += '距离%s还有%d天,\n' % (i[0], i[1])

    s3 = '''上班是帮老板赚钱,摸鱼是赚老板的钱！最后,祝愿天下所有摸鱼人,都能愉快的渡过每一天......
【友情提示】三甲医院ICU躺一天平均费用大概一万块,你晚一天进ICU,就等于为你的家庭多赚一万块。少上班,多摸鱼！！！'''

    s = s1+s2+s3
    print(s)

    action = Action(qq=jconfig.bot)
    action.sendGroupText(257069779, s)


job1 = scheduler.add_job(get_nums, 'cron', hour=9, minute=10)
