import ccxt, os, colorama, time
from bot_functions.functions import *
colorama.init(autoreset=True)
os.system("")


# CONFIG 
EXCHANGE_NAME           = "binance"
TIMEFRAME               = "1d" 
RSI_PERIOD              = 8
RSI_OVERBOUGHT          = 70
RSI_OVERSOLD            = 30
RSI_APPLIED_PRICE       = "low"
FILTER_SYMBOL           = "USDT"
SELECTED_SYMBOL_ONLY    = False

SELECTED_SYMBOLS = """BTC,BNB,ETH,ARB,MATIC,XRP,ADA,TRX,DOGE,LTC,TON"""

TELEGRAM_API_KEY = ""
TELEGRAM_IDS = [] #format [1234, 4321, ...etc]


SELECTED_SYMBOLS = SELECTED_SYMBOLS.replace(" ","").replace("\n","").strip()
# instanciate the exchange class
try:
    exchange_class = getattr(ccxt, EXCHANGE_NAME)
    exchange = exchange_class({
        'apiKey': "",
        'secret': "",
        'enableRateLimit': True
    })
    # load all the symbols market from the excahnge
    exchange.load_markets()
except Exception as e:
    input(f"{Fore.RED}[Error]:{e}")
    exit()



# FILTER ONLY USDT pairs
all_symbols = []

if SELECTED_SYMBOL_ONLY:
    all_symbols = SELECTED_SYMBOLS.split(",")
else:  
    for symbol in exchange.symbols:
        if FILTER_SYMBOL in symbol:
            all_symbols.append(symbol)


print(Fore.GREEN+"TOTAL Filtered Symbols:", len(all_symbols))
# store the open time of the candle when a signal is sent
last_message_time = {}


def main():
    while True:
        for symbol in all_symbols:
            try:
                # fecth candle stick
                condle_stick = get_kline(symbol, TIMEFRAME, 500, exchange)
                # structure candle stick in a dataframe
                candle_dataframe = candle_stick_dataf(condle_stick)
                
                buy_signal = RSI_is_buy(candle_dataframe[RSI_APPLIED_PRICE],RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD)
                
                if buy_signal:
                    timestamp = reverse(candle_dataframe["timestamp"])[0]
                    s = gen_sticker()
                    try:
                        last_sent = last_message_time[symbol]  
                        if last_sent != timestamp:
                            # SEND ALERT
                            # print(buy_signal, symbol)
                            alert =f"""======={s}{symbol}{s}======= 
            buy'n HOLD signal found"""
                            sendtlm(alert, TELEGRAM_API_KEY, TELEGRAM_IDS)
                            last_message_time[symbol]  = timestamp
                    except:
                        # SEND ALERT
                        # print(buy_signal, symbol)
                        alert =f"""======={s}{symbol}{s}======= 
            buy'n HOLD signal found"""
                        sendtlm(alert, TELEGRAM_API_KEY, TELEGRAM_IDS)
                        last_message_time[symbol]  = timestamp  
                
                time.sleep(1)
            except Exception as err:
                log(str(err))


if __name__ == "__main__":
    print(Fore.YELLOW+"RUNING signal bot")
    main()