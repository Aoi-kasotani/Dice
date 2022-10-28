import asyncio
import discord
import random  # 乱数計算用
import re      # 正規表現
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

#tokenの設定
token = "xxx"

@bot.event
async def on_ready():
    print('My bot ready!')
    print('discord.py version is ' + discord.__version__)
    activity = discord.Activity(name='このサーバー', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)


# -----ここからダイスロール用の関数-----

# nDm
pattern1 = '\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}'

# nDm+k
pattern2 = '\d{1,2}d\d{1,3}\+\d{1,3}|\d{1,2}D\d{1,3}\+\d{1,3}'
# nDm+nDm
pattern3 = '\d{1,2}d\d{1,3}\+\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}\+\d{1,2}D\d{1,3}'

# nDm-k
pattern4 = '\d{1,2}d\d{1,3}\-\d{1,3}|\d{1,2}D\d{1,3}\-\d{1,3}'
# nDm-nDm
pattern5 = '\d{1,2}d\d{1,3}\-\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}\-\d{1,2}D\d{1,3}'

patterns = [pattern1,pattern2,pattern3,pattern4,pattern5]

# 与えられた文字列が用意した正規表現にマッチするか後ろから順にチェック
def judge_nDn(src,n):
    repatter = re.compile(patterns[n])
    result = repatter.fullmatch(src)
    if result is not None:
        return n  # マッチしているなら何番目のパターンか返す（0~4）
    elif n==0:
        return -1  #nが0になってもマッチしなかったら-1を返す（もっと良い方法ありそう）
    else:
        return judge_nDn(src,n-1)  # マッチしなかったら別の正規表現に対してもう一度チェック

# 与えられた文字列から数字の部分のみを抽出
def split_nDn(src, n):
    if n > 2:
        split_pattern = 'd|D|\-'  # 何番目のパターンにマッチしているかによって分割に使う文字列を変更
    else:
        split_pattern = 'd|D|\+'
    return re.split(split_pattern,src)

# ダイスロール
def role_nDn(src,n):
    role_index = split_nDn(src, n)

    result_1 = []  # 1種類目のダイスロール結果
    result_2 = []
    sum_dice_1 = 0  # 1種類目のダイス合計値
    sum_dice_2 = 0

    dice_count_1 = int(role_index[0])  # 1種類目のダイス個数
    dice_size_1 = int(role_index[1])  # 1種類目のダイスの種類

    for i in range(dice_count_1):
        tmp = random.randint(1,dice_size_1)
        result_1.append(tmp)
        sum_dice_1 += tmp
    only_one_dice_1 = True if dice_count_1 == 1 else False  # 1種類目のダイスが1つだけならTrue（メッセージの成型に利用）
    
    if n in [2,4]:
        dice_count_2 = int(role_index[2])
        dice_size_2 = int(role_index[3])

        for i in range(dice_count_2):
            tmp = random.randint(1,dice_size_2)
            result_2.append(tmp)
            sum_dice_2 += tmp
        only_one_dice_2 = True if dice_count_2 == 1 else False
    else:
        only_one_dice_2 = False

    if n in [1,3]:
        sub = int(role_index[2])  # 足される値ないし引かれる値
    else:
        sub = 0

    return result_1, sum_dice_1, only_one_dice_1, result_2, sum_dice_2, only_one_dice_2, sub

# 文字の読み取りと結果の出力
def nDn(text):
    mode = judge_nDn(text,4)
    if mode >= 0:
        result_1, sum_dice_1, only_one_dice_1, result_2, sum_dice_2, only_one_dice_2, sub = role_nDn(text,mode)
        if mode > 2:
            sign = -1
        else:
            sign = 1       
        if mode in [0,1,3]:     
            if only_one_dice_1:
                return 'ダイス：' + text + '\n出目：' + str(sum_dice_1) + '\n合計：' + str(sum_dice_1+sub*sign)
            else:
                return 'ダイス：' + text + '\n出目：' + str(result_1) + '\n合計：' + str(sum_dice_1+sub*sign)
        elif mode in [2,4]:
            if only_one_dice_1:
                if only_one_dice_2:
                    return 'ダイス：' + text + '\n出目：' + str(sum_dice_1) + ", " + str(sum_dice_2) + '\n合計：' + str(sum_dice_1+sum_dice_2*sign)
                else:
                    return 'ダイス：' + text + '\n出目：' + str(sum_dice_1) + ", " + str(result_2) + '\n合計：' + str(sum_dice_1+sum_dice_2*sign)
            else:
                if only_one_dice_2:
                    return 'ダイス：' + text + '\n出目：' + str(result_1) + ", " + str(sum_dice_2) + '\n合計：' + str(sum_dice_1+sum_dice_2*sign)
                else:
                    return 'ダイス：' + text + '\n出目：' + str(result_1) + ", " + str(result_2) + '\n合計：' + str(sum_dice_1+sum_dice_2*sign)
    else:
        return None


# -----ここまでダイスロール用の関数-----


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    result = nDn(message.content)  # メッセージの内容でダイスロールできるか試す（ダイスロールできなければNoneが返ってくる）

    if result is not None:
        await message.reply(result)  # ダイスロールの結果が無事に出れば、それを送信する

    await bot.process_commands(message)

# botを起動する
bot.run(token)
