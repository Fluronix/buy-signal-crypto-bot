from ta.momentum import RSIIndicator
import pandas as pd
from colorama import Fore,Back
import datetime, requests,random,math


def open_file(fpath):
    with open(fpath, encoding="utf8") as f:
        file = f.read()
    return file

def save_file(path, file):
    with open(path, "w") as fp:
        fp.write(file)
        return True

def reverse(data, reverse=True):
    output = []
    for i in data:
       output.append(i)
    try:
        output = [x for x in output if not math.isnan(x)]
    except:
        None
    if reverse == True:
        return output[::-1]
    else:
        return output

# structure candlestick in pd dataframe
def candle_stick_dataf(candle_sticks_list):
    df = pd.DataFrame(candle_sticks_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Fetch candlestick 
def get_kline(symbol,time_frame, bar_limit, exchange):
    candles_sticks = exchange.fetch_ohlcv(symbol, timeframe=time_frame, limit=bar_limit)
    return candles_sticks

# RSI technical indicator
def RSI_is_buy(close, RSIP, RSI0B, RSI0S):
    RSI = RSIIndicator(close=close, window=RSIP).rsi()
    RSI = reverse(RSI)
    return RSI[2]<RSI0S and  RSI[1]>RSI0S and RSI[0]>RSI0S

def log(mesage, type="wairning", path="./logs.log"):
    time = str(datetime.datetime.now())
    event_log = ''
    
    try:
        event_log = open_file(path)
    except:
        None
 
    text_format = f"{time} --> {type}: {mesage}\n"
    event_log = event_log + text_format
    
    save_file(path, event_log)


def sendtlm(message, telegram_apikey, usr_id):
    for id in usr_id:
        requests.get(f"https://api.telegram.org/bot{telegram_apikey}/sendmessage?chat_id={id}&text={message}")

def gen_sticker():
    allalpha = """😀😙😩🥸🤭🫥🫡🥱😈🫰🤞🤝👌😬😑😱😕🥸👉👈👌👄💋👀👁💂‍♀👮‍♀🧕🧑‍🦰👨‍🦰👱‍♀👱👩‍🦳🧑‍🦳👩🏼🧠🩳🧵👔👖🥷🎩🐶🐭🐷🐧🐔🐒🐌🐞🐝🐥🙈🐵🐣🐆🐅🐊🦭🦈🐋🐬🦕🐙🦑🦐🦞🦀🐡🐠🐟🦖🦎🐍🐢🦂🕸🕷🦗🦟🪱🐛🦋🐌🐞🐜🪰🪲🪳🐈‍⬛🕊🐑🦒🐫🐪🐏🐖🐎🦮🦜🦚🐩🐕🦤🐓🪶🦙🐐🦌🐃🦬🦘🦨🦡🦫🐲🐉🌵🐲🎄🌲🌳🎋🪴🎍🍀☘🌿🌱🪵🌴🍃🍂🪺🍄🐚🪸🪨🌾🌷🌷💐🌹🥀🪷🌺🌸🌼🌗🌖🌕🌚🌜🌛🌝🌻🌘🌑🌒🌓🌔🌙🌎🌍🌏🔥💥☄⚡✨🌟⭐💫🪐🌪🌈☀🌤⛅🌦🌧☂🌊🌫🍏🍎🥦🍠🥬🥐🥞🍷🥂🍷🍻🍺🧊🥄🥡🍹🧋🥜🎂🍰🍦🍨🍫🍿🍪🍵⚽🏀🏸🏓🪀🎱🥅⛳🪁🏹🎣🤿🎽🛹🛼🧘🏽🤼‍♀🥇🥈🥉🎖🏵🚴‍♀🚗🚕🚙🚌🚎🚓🚑🚒🚐🛻🚛🚜🦯🦽🦼🛴🚲🏍🛺🛞🚨🚔🚍🚖🚡🚠🚟🚃🚋🚞🚝🚂🚆🚇🚊🚉✈🛫🛬💺🛰🚀🛸🚁🛶⛵🛳⛴🚢🛟⚓🪝⛽🚧🚦🚥🚏🗺🗿🗽🗼🏛🏣💒🏬🏩🏢🏭🏫🏪🏗🏚🏨🏥🏡🏠🏤⛪🕋🕋⛩🛤🛣🛣⌚📱📲💻⌨🖥🖨🖱🖲📸📺📠📷📼📟☎📀💿📞🎞💾💽📽🎥🗜🕹📹📻🎙🎚🎛🧭⏱⏲⏰🕰🕯💡🔌🪫🔋📡⏳⌛🪔🛢💸💵💴💶💷🪙💰💳🪪💎❤🧡💛💚💙💜🖤🤍🤎💖💗💓💞💕❣❤‍🩹❤‍🔥💝💘💔💯❌✅"""
    index =  random.sample(range(len(allalpha)), 1)[0]
    return allalpha[index]


