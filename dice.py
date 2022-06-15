import random
import re

# nDm
pattern1 = '\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}'
split_pattern1 = 'd|D'

# nDm+k
pattern2 = '\d{1,2}d\d{1,3}\+\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}\+\d{1,2}D\d{1,3}'
split_pattern2 = 'd|D|\+'
# nDm+nDm
pattern3 = '\d{1,2}d\d{1,3}\+\d{1,3}|\d{1,2}D\d{1,3}\+\d{1,3}'
split_pattern3 = 'd|D|\+'

# nDm-k
pattern4 = '\d{1,2}d\d{1,3}\-\d{1,3}|\d{1,2}D\d{1,3}\-\d{1,3}'
split_pattern4 = 'd|D|\-'
# nDm-nDm
pattern5 = '\d{1,2}d\d{1,3}\-\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}\-\d{1,2}D\d{1,3}'
split_pattern5 = 'd|D|\-'

# str nDm
pattern6 = '\D{1,}\s\d{1,2}d\d{1,3}'
split_pattern6 = 'd|\s'

# str nDm+k
pattern7 = '\D{1,}\s\d{1,2}d\d{1,3}\+\d{1,3}'
split_pattern7 = 'd|\+|\s'
# str nDm+nDm
pattern8 = '\D{1,}\s\d{1,2}d\d{1,3}\+\d{1,2}d\d{1,3}'
split_pattern8 = 'd|\+|\s'

# str nDm-k
pattern9 = '\D{1,}\s\d{1,2}d\d{1,3}\-\d{1,3}'
split_pattern9 = 'd|\-|\s'
# str nDm-nDm
pattern10 = '\D{1,}\s\d{1,2}d\d{1,3}\-\d{1,2}d\d{1,3}'
split_pattern10 = 'd|\-|\s'

patterns = [pattern1,pattern2,pattern3,pattern4,pattern5,pattern6,pattern7,pattern8,pattern9,pattern10]
split_patterns = [split_pattern1,split_pattern2,split_pattern3,split_pattern4,split_pattern5,split_pattern6,split_pattern7,split_pattern8,split_pattern9,split_pattern10]

# 対象の文字列かチェック
def judge_nDn(src,n,m):
    repatter = re.compile(patterns[n-1])
    result = repatter.fullmatch(src)
    if result is not None:
        return n
    elif n==m:
        return False
    else:
        judge_nDn(src,n-1,m)

# 文字列の分割
def split_nDn(src,n):
    return re.split(split_patterns[n-1],src)

# ダイスロール
def role_nDn(src,n):
    role_index = split_nDn(src,n)

    print(role_index)

    result1 = []
    result2 = []
    sum_dice1 = 0
    sum_dice2 = 0

    if n<6:
        role_count1 = int(role_index[0])
        nDice1 = int(role_index[1])
    else:
        role_count1 = int(role_index[1])
        nDice1 = int(role_index[2])
    for i in range(role_count1):
        tmp = random.randint(1,nDice1)
        result1.append(tmp)
        sum_dice1 = sum_dice1 + tmp
    is1dice1 = True if role_count1 == 1 else False
    
    if n in [3,5,8,10]:
        if n in [3,5]:
            role_count2 = int(role_index[2])
            nDice2 = int(role_index[3])
        else:
            role_count2 = int(role_index[3])
            nDice2 = int(role_index[4])
        for i in range(role_count2):
            tmp = random.randint(1,nDice2)
            result2.append(tmp)
            sum_dice2 = sum_dice2 + tmp
        is1dice2 = True if role_count2 == 1 else False
    else:
        is1dice2 = False

    if n == 2:
        sub = int(role_index[2])
    elif n == 4:
        sub = int(role_index[2])*-1
    elif n==7:
        sub = int(role_index[3])
    elif n==9:
        sub = int(role_index[3])*-1
    else:
        sub = 0

    return result1,sum_dice1,is1dice1,result2,sum_dice2,is1dice2,sub

# 文字の読み取りと結果の出力
def nDn(text):
    mode = judge_nDn(text,10,1)
    if mode != False:
        result1,sum_dice1,is1dice1,result2,sum_dice2,is1dice2,sub = role_nDn(text,mode)       
        if mode in [1,6]:     
            if is1dice1:
                return 'ダイス：' + text + '\n出目：' + str(sum_dice1) + '\n合計：' + str(sum_dice1)
            else:
                return 'ダイス：' + text + '\n出目：' + str(result1) + '\n合計：' + str(sum_dice1)
        elif mode in [2,4,7,9]:
            if is1dice1:
                return 'ダイス：' + text + '\n出目：' + str(sum_dice1) + '\n合計：' + str(sum_dice1+sub)
            else:
                return 'ダイス：' + text + '\n出目：' + str(result1) + '\n合計：' + str(sum_dice1+sub)
        elif mode in [3,8]:
            if is1dice1:
                if is1dice2:
                    return 'ダイス：' + text + '\n出目：' + str(sum_dice1) + ", " + str(sum_dice2) + '\n合計：' + str(sum_dice1+sum_dice2)
                else:
                    return 'ダイス：' + text + '\n出目：' + str(sum_dice1) + ", " + str(result2) + '\n合計：' + str(sum_dice1+sum_dice2)
            else:
                if is1dice2:
                    return 'ダイス：' + text + '\n出目：' + str(result1) + ", " + str(sum_dice2) + '\n合計：' + str(sum_dice1+sum_dice2)
                else:
                    return 'ダイス：' + text + '\n出目：' + str(result1) + ", " + str(result2) + '\n合計：' + str(sum_dice1+sum_dice2)
        else:
            if is1dice1:
                if is1dice2:
                    return 'ダイス：' + text + '\n出目：' + str(sum_dice1) + ", " + str(sum_dice2) + '\n合計：' + str(sum_dice1-sum_dice2)
                else:
                    return 'ダイス：' + text + '\n出目：' + str(sum_dice1) + ", " + str(result2) + '\n合計：' + str(sum_dice1-sum_dice2)
            else:
                if is1dice2:
                    return 'ダイス：' + text + '\n出目：' + str(result1) + ", " + str(sum_dice2) + '\n合計：' + str(sum_dice1-sum_dice2)
                else:
                    return 'ダイス：' + text + '\n出目：' + str(result1) + ", " + str(result2) + '\n合計：' + str(sum_dice1-sum_dice2)
    else:
        return None