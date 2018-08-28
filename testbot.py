import discord
from discord.ext import commands
from discord.utils import get
import datetime
import time,datetime
from datetime import datetime,timezone,timedelta
import requests
import json
import random

# 1.透過user_total_money()查詢時此時若使用者不在名單上因為呼叫search_money()所以也會直接新增一列
# 2.def addTrophy(rows):戰利品登記函數，沒有檢查是否為空值


#     cpulimit --pid 2902 --limit 90      
#     nohup python testbot.py &>myout.txt &      
#     nohup cpulimit --pid 2902 --limit 90 &>myout.txt &  
#     nohup python testbot.py > nohup.log 2>&1 &                       
google_db_url="{https://script.google.com/macros/s/123456789/exec}"

week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期日',
}

Trophydict = {'<:1000g:476274938395885568>': 0,'<:blue:476262599177011240>': 0, '<:red:476262607335063552>': 0, '<:skin:476262626519941120>': 0 ,'<:tooth:476262644287012865>': 0 ,'<:nashark:476262658669281294>' : 0,'<:Carapace:476262683189182464>' : 0,'<:coin:476262700532367371>':0}

Trophydict_2_ch = {
    '<:1000g:476274938395885568>' : '金塊1000g',
    '<:blue:476262599177011240>' : '怪獸內丹',
    '<:red:476262607335063552>' : '赫卡魯的突起',
    '<:skin:476262626519941120>' : '漂流追蹤者的外皮',
    '<:tooth:476262644287012865>' : '幽冥鐵牙的顎骨',
    '<:nashark:476262658669281294>' : '納恩薩克的角破片',
    '<:Carapace:476262683189182464>' : '坎迪杜姆的甲殼',
    '<:coin:476262700532367371>' : '古德蒙特海賊團的金幣'
}
Trophydict_2_eng = {
    '金塊1000g' :'<:1000g:476274938395885568>' ,
    '怪獸內丹'  :'<:blue:476262599177011240>' ,
    '赫卡魯的突起':'<:red:476262607335063552>',
    '漂流追蹤者的外皮'  :'<:skin:476262626519941120>',
    '幽冥鐵牙的顎骨' :'<:tooth:476262644287012865>' ,
    '納恩薩克的角破片'  :'<:nashark:476262658669281294>' ,
    '坎迪杜姆的甲殼':'<:Carapace:476262683189182464>',
    '古德蒙特海賊團的金幣'  :'<:coin:476262700532367371>'
}

def whatdayistoday(n): 
    """n=0回傳年月日&星期幾，n=其他數字，回傳星期幾""" 
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)
    tzutc_8 = timezone(timedelta(hours=8))
    local_dt = dt.astimezone(tzutc_8)
    today = (str(local_dt)[:10])#今天幾月幾號  '2018-08-08'
    
    day = local_dt.weekday()
    if (n == 0):
        return (today + week_day_dict[day]) # week_day_dict[day] 星期三
    return (week_day_dict[day]) #  星期三

# print (whatdayistoday(1))

def search_money(name,day = "nullll"):
    """搜尋並列出使用者的金額"""
    payload = {'method': 'read','name': name}
    r = requests.post(google_db_url, params=payload)
    allmoney = json.loads(r.text)
    # {'星期日': '123456789123456789', '星期二': 0, '星期六': 0, '星期五': 0, 'total': 9487, '星期三': 123, '星期四': 0, '星期一': '123456789123456789'}
    if (r.status_code != 200):
        print("無法連上google資料庫，或未知的錯誤 查詢資料失敗")

    if (day != "nullll"): #如果有指定天數就回傳指定日期的金額
        return allmoney[day]
    else: #若無指定日期則回傳整個禮拜的資料
        return allmoney
# print(search_money("Serapin","星期日"))

def update_money(name,day,money):
    """上傳金額"""
    tmp = search_money(name,day)
    if (not tmp): #空值自動帶入0
        tmp = 0

    total = money + int(tmp)    
    payload = {'method': 'write','name': name ,'day': day,'money': total }
    if (day =="total"): #如果是要上傳當周總金額則不需要在把total重新加上原本的資料
        payload = {'method': 'write','name': name ,'day': day,'money': money }
    r = requests.post(google_db_url, params=payload)

    if (r.status_code != 200):
        print("無法連上google資料庫，或未知的錯誤 新增資料失敗")
    elif ( day == "total"):
        print("已成功結算使用者 "+name+" 的總金額"+str(money)+ " 元")
    else:
        print("使用者 "+name+" 於 "+day+" 已成功新增 "+str(money)+ " 元，目前當日總金額為 "+str(total))
# update_money("Serapin2","星期一",123)

def user_total_money(name): 
    """查詢並計算該使用者當周的總金額"""
    everyday_money = search_money(name)
    total = 0
    # print(everyday_money)
    for i in range(0,7):
        tmp = everyday_money[week_day_dict[i]]
        if (not tmp): #空值自動帶入0
            tmp = 0
        total += int(tmp)
    # print(total)
    if (total == 0):
        print("使用者 "+name+" 尚未有任何登記紀錄喔")
        return -1
    update_money(name,"total",total)
    return total
# print (user_total_money("Serapin"))


def getTrophy(day):
    """從google資料庫上下載海怪戰利品 回傳字典"""
    payload = {'method': 'read_Trophy','day': day}
    r = requests.post(google_db_url, params=payload)
    allTrophy = json.loads(r.text)
    # print(allTrophy)
    return allTrophy
# print(getTrophy("星期一"))


def addTrophy(rows):  #登記戰利品
    """登記戰利品"""
    
    today = whatdayistoday(0)   # today = '2018-08-14星期二'
    allTrophy = getTrophy(today) #下載戰利品數量    
    # print("allTrophy",allTrophy)
    payload = {'method': 'write_Trophy',"day":today}
    # payload.update(allTrophy)
    # r = requests.post(google_db_url, params=payload)

    for i in range(0,len(rows)):
        if(i%2==0):#戰利品
            allTrophy[Trophydict_2_ch[rows[i]]] += int(rows[i+1])
            # 2018-08-07 <:blue:476262599177011240> 10
            # 2018-08-07 <:red:476262607335063552> 20    
    payload.update(allTrophy)
    # print("payload",payload)
    r = requests.post(google_db_url, params=payload)
    if (r.status_code != 200):
        print("無法連上google資料庫，或未知的錯誤 新增戰利品資料失敗")
    else:
        print("已成功更新戰利品")
    # print(r.text)
    ######################################################
    payload = {'method': 'write_Trophy_raw',"day":today}
    # payload.update(allTrophy)
    # r = requests.post(google_db_url, params=payload)
    # print(r.text)

    for i in allTrophy:
        allTrophy[i] = 0
    # print(allTrophy)
    for i in range(0,len(rows)):
        if(i%2==0):#戰利品
            allTrophy[Trophydict_2_ch[rows[i]]] = int(rows[i+1])
    payload.update(allTrophy)
    # print(payload)
    r = requests.post(google_db_url, params=payload)
    if (r.status_code != 200):
        print("無法連上google資料庫，或未知的錯誤 新增記錄檔戰利品資料失敗")
    else:
        print("已成功更新記錄檔戰利品")        
# rows = {'<:1000g:476274938395885568>', '10','<:blue:476262599177011240>', '20','<:Carapace:476262683189182464>', '30','<:coin:476262700532367371>', '40'}
# addTrophy(rows)

# def checkTrophy():
#     """輸出當天總戰利品數量""" 
#     send_msg_text=""
#     allTrophy = getTrophy("星期一") #下載戰利品數量
#     for i in allTrophy:
#         send_msg_text += i +" "+ Trophydict_2_eng[i] + " : "+ str(allTrophy[i]) +'\n'
#     print(send_msg_text)
#     print(ctx.message.author.display_name+"使用本系統查詢了當日目前的戰利品總數量")
# checkTrophy()


TOKEN = '{dis token}'

description = '''Bot in Python'''
bot = commands.Bot(command_prefix='$', description=description)

print (whatdayistoday(0)) #2018-08-08 星期三
print("hi 你好 本呆呆機器人將為您服務")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def hello(ctx):
    """Says world"""    
    await bot.say('hi {}'.format(ctx.message.author.display_name))    
    # await bot.say('hi {}'.format(ctx.message.channel))    #hi bot-test測試頻道


@bot.command(pass_context=True)
async def game(ctx):
    """game"""    
    await bot.say('請輸入0~9的數字')   
    def guess_check(m):
        # print(m)
        return m.content.isdigit()
    guess = await bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=guess_check)
    answer = random.randint(1, 10)
    if guess is None:
        await bot.say('必須輸入0~9的數字喔，別問為什麼我只是在測試怎麼讓bot限定時間內回應')
        return
    if int(guess.content) == answer:
        await bot.say('你猜對了')
    else:
        await bot.say("猜錯了喔 正確答案是 "+str(answer))


# @bot.command(pass_context=True)
# async def reset(ctx,*args):
#     """reset data"""    
#     print(ctx.message.author.display_name+"使用了刪除資料的功能")
#     await bot.say('確定要刪除當周玩家的收入表和獲得戰利品的資料表? 請在5秒內輸入通關密語:12345678987654321')   

#     def num_check(m):
#         return m.content.isdigit()
#     guess = await bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=num_check)

#     # answer = random.randint(1, 10)
#     if (guess is None):
#         print(ctx.message.author.display_name+"刪除數據失敗")
#         await bot.say('必須輸入12345678987654321喔')
#         return
#     elif (int(guess.content) == 12345678987654321 ):
#         print(ctx.message.author.display_name+"開始刪除 戰利品資料表")
#         await bot.say('開始刪除 戰利品資料表 後悔也來不及啦')
#         cleanall()

#     else:
#         print(ctx.message.author.display_name+"刪除數據時發生未知的錯誤")
#         await bot.say("未知的錯誤")


@bot.command(pass_context=True)
async def check(ctx):
    """輸出當天總戰利品數量"""     
    await bot.say('hi {}'.format(ctx.message.author.display_name))
    send_msg_text=""
    today = whatdayistoday(0)   # today = '2018-08-14星期二'
    allTrophy = getTrophy(today) #下載戰利品數量
    for i in allTrophy:
        send_msg_text += i +" "+ Trophydict_2_eng[i] + " : "+ str(allTrophy[i]) +'\n'
    await bot.say(send_msg_text)
    print(ctx.message.author.display_name+"使用本系統查詢了當日目前的戰利品總數量")

@bot.command(pass_context=True)
async def total(ctx):
    """查詢玩家一個禮拜以來的總收入"""    
    # await bot.say('hi {}'.format(ctx.message.author.display_name))
    display_name = str(ctx.message.author.display_name)
    total_money = user_total_money(display_name)

    if (total_money <= 0):
        print(display_name+" 查詢收入失敗，因為當天尚未有收入")
        await bot.say("還沒有收入喔")
    elif (total_money > 0):
        # print(display_name+" 的收入是:"+str(total_money))
        # "{:,}".format(99999999)
        print(display_name+" 的收入是:"+"{:,}".format(total_money))
        await bot.say("hi "+display_name+" 你的收入是:"+"{:,}".format(total_money))


# @bot.command(pass_context=True)
# async def Backup(ctx):
#     """檔案備份指令"""    
#     print(ctx.message.author.display_name+"使用了備份指令")
#     await bot.say('hi {} start Backup'.format(ctx.message.author.display_name))
#     await bot.send_file(ctx.message.channel, 'output.csv')
#     await bot.send_file(ctx.message.channel, 'Trophy.csv')

@bot.command(pass_context=True)
async def eat(ctx,*args):
    bot_message_channel = str(ctx.message.channel) #判斷是否在指定伺服器頻道裡面
    display_name = str(ctx.message.author.display_name)

    if( bot_message_channel == "bot-test測試頻道") or (bot_message_channel == "bot公開測試頻道") or (bot_message_channel == "test"):   #判斷是否在指定伺服器頻道裡面
        print(display_name)
        print('{} arguments: {}'.format(len(args), ', '.join(args)))
        await bot.say('{} arguments: {}'.format(len(args), ', '.join(args)))
    else:
        await bot.say('不好意思喔 這裡不是授權的頻道')
        print('這裡不是授權的頻道',str(ctx.message.channel))
        return

    if(len(args)%2 != 0):
        print("輸入錯誤 資料不對襯")
        await bot.say("輸入錯誤 別亂餵我好嗎?")
        return

    total = 0 #輸入總金額
    for i in range(0,len(args)):
        # print(args[i])
        if( len(args) >= 2):
            # if(i < len(args)-1): #意義不明 先註解好了
            if ((i % 2) == 0):  # i%2==0 代表戰利品欄位(單數0,2,4,6,8) i+1代表數量(雙數1,3,5,7)
                if(args[i+1].isdigit()):    #如果數量欄位(1,3,5,7)是數字  

                    if( int(args[i+1]) > 100000000 or int(args[i+1]) <= 0 ):
                        print("數量異常")
                        await bot.say("數量異常 最好別亂輸入喔")
                        return             

                    if (emojis2money(args[i]) == -1):
                        print("戰利品欄位錯誤")
                        await bot.say("戰利品欄位錯誤，必須是戰利品表情符號")
                        return
                    elif (emojis2money(args[i]) != -1):
                        total += emojis2money(args[i])*int(args[i+1]) #物品價錢*數量
                elif(args[i+1].isdigit() == False): #如果數量欄位(1,3,5,7)不是數字
                    print("數量錯誤，必須是數字"+args[i]+args[i+1])
                    await bot.say("數量錯誤，必須是數字")
                    return
        else:
            print('len(args) 必須大於 2')
            await bot.say("別耍我喔ˋˊ")
            return
    # print("args",args)
    addTrophy(args)#把戰利品存入Trophy.csv
    # print(display_name+" today("+ whatdayistoday(0) +") ur inpurt money:"+str(total))
    print(display_name+" today("+ whatdayistoday(0) +") ur inpurt money:"+"{:,}".format(total))

    await bot.say("hi "+display_name+" today("+ whatdayistoday(1) +") ur inpurt money:"+"{:,}".format(total))
    update_money(display_name,whatdayistoday(1),total)#把收入存入output.csv
    user_total_money(display_name)#計算總收入

def emojis2money(emojis):
    if emojis =="<:1000g:476274938395885568>":
        return 100000000
    if emojis == "<:blue:476262599177011240>":
        return 100000
    if emojis == "<:red:476262607335063552>":
        return 82000
    if emojis == "<:skin:476262626519941120>":
        return 42800
    if emojis == "<:tooth:476262644287012865>":
        return 52400
    if emojis == "<:nashark:476262658669281294>":
        return 53700
    if emojis == "<:Carapace:476262683189182464>":
        return 409200
    if emojis == "<:coin:476262700532367371>":
        return 100000

    # print("戰利品欄位錯誤!")
    return -1

bot.run(TOKEN)

# ('<:1000g:476274938395885568>', 
# '<:blue:476262599177011240>', 
# '<:Carapace:476262683189182464>', 
# '<:coin:476262700532367371>', 
# '<:nashark:476262658669281294>', 
# '<:nashark:476262658669281294>', 
# '<:red:476262607335063552>', 
# '<:skin:476262626519941120>', 
# '<:tooth:476262644287012865>')