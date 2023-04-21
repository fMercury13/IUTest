import pyautogui
import time
import re
import webbrowser
from PIL import Image
from requests_html import HTMLSession, HTML
import requests
from fake_useragent import UserAgent
import json
import clipboard
import PySimpleGUI as sg
import logging
logging.basicConfig(filename="IUTestlogs.log", level=logging.INFO)

IUDark = {'BACKGROUND': '#0D1017',
                'TEXT': '#FFFFFF',
                'INPUT': '#55007c',
                'TEXT_INPUT': '#FFFFFF',
                'SCROLL': '#55007c',
                'BUTTON': ('white', '#55007c'),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}
sg.theme_add_new('IUDark', IUDark)
sg.theme('IUDark')
font = ('Cassiacdia Code', 12)
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
pyautogui.FAILSAFE = True
session = HTMLSession()
currentask = 0
nextimg = './nextbtn.png'
infoimg = './infbtn.png'
capimg = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAABHxJREFUWEeNV9FVI0cQrBo/f0MGKAQ5gsMRGCKwHAG6CCQiQEQARAAXASgC4wxQBCf+jy2/6pnRrnZXgvkBrWanq6urq0fEFxcB6Et7vdOru3vsWd5Vv4l/VKKMBet+P4bjKMADX/rxDkB76NdzbXPoZ6ucUD30yJF7AEhAItihLw7pHVA/NtI0siBf9wkdK9b+IfXTCAOfEyzpXMACwrlBA3gBcE3yJdBSRwXTDT4KIHMwpFWNzgEsBJzHi8S79xE8KbA7QD5X7AENDAvnjB0YgP8a2juAFYGVPzdo5klpDuKkANoB+UxRBxjIDEqaSLojGYEBvQN00BXJbTdHSacA5gLmgE7MYinNPyTf9qXUwtoXYUe5v6Tlb5luHxUZjwXuKzSANJgjaY62NEuS10NuC8xeJs72BsK0qP8W1JJMkfFxS2l1YyANsErC335JwCuB7yHUjk53DBQKFxLmWdnaQJwxWdkOnN9SieHyNMAiAVuS3/utWpkJ/Qj3IM5KombSHdMmJOkCwB2E05LidSKXY93cCTwLNOQ7Sdf/qJdJWmYhx6lbgJdOLucqOctvWWd4g/CEhIfWYGKPg1xJWOYWDHU8AHB9347Uxu9O4VIAF6AmpZBri7sCmEYrwWpnpipnZzCmbAtiCWESgRo8IJXAY5kTaBpNCPzlzgAwyZnTx27IMK4VE62L/SVpBekqO1oF4tdj64bALDve+MqeoSuILmtv2vy6TfzdrbpbuQ86T/ShJZJr1VwDyR7/2AvlZ/aBh25HSJpBWLQUhx3/AHkPYFqMLLQVTJSgYww8IVNnA7mXl/NXKN10nmW8eiN8WCz/nZT/N9kzdF9bV2pmAO+A0NWsk/5wHKuR+9SC/BOAhfdYzOgykU+NM80Ba1uV6mIjaJmYnPEesaUszxLXKVVXzbtGGGg80SoAH3ZmLgW+JvKPij4oz0CCAbPVrWwVnclu8ix5BhDK3wEsMusygo9GL2wZKADiuP8S6VqOrmNDJ49vPVNcM+XW696+yoF5CDcuOYBEsskG9ViyuST51OV2OLZLbvU+UFA10imBn/EtU2E9K2kwjD7kO1EsU/wDwE8Bm0RWkR0iYejGZWcpl50WTOUKU8IPNRAi1Lcetl3tdrCH95U9YNU584gOBpxve04ZSAFnz/M9uRoLTDNlMbo0W4grELf9e0Cfjjaw5hBPTSehNcB7CzXHax2kZaCOyFqhRhMI/4IxA2JJ3JKeljEDBquY0Y2I0zwqsIZnx26iDq+K1W97s8Se/fFiBgg42D08zdwdcXBYsWd73IbL7fimc2VbM7dmsexDPTLiAzlTXUB4BLUBODXtMYPycw+nszKUVkiR1TwTF/vNkN30oChb6oieBjJS11G2UtBZ5Dt/SaLcdOYJWriZS43d2NcgVoncjv2WGAPkIwddkNFVylrq+iT6YhKe70lBzlO5eB7q0cNF6LxRjeWYq335N1c5dyyF3bNqxV1rPJTB0ec9wo4l0LfhAyWo4YZHDYvThdbdb4G1l9gobPz23E/lfwVGPE/BE3hzAAAAAElFTkSuQmCC'
bookimg = './guide.png'
regex = r"""\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"""
#FUNCTIONS
def tab_forth():
    pyautogui.hotkey('ctrl', 'tab')

def tab_back():
    pyautogui.hotkey('ctrl', 'shift', 'tab')

def dotest(tasklink):
    webbrowser.open_new(tasklink)
    time.sleep(7)
    pyautogui.scroll(-15)

def newses():
    isstopped = pyautogui.locateCenterOnScreen('sesstop.png')
    if isstopped != None:
        pyautogui.hotkey('ctrl', 'r')

def radio(tasks):
    loops = 0
    while pyautogui.locateCenterOnScreen('spinner.png') == None:   
        global currentask
        currentask += 1
        #founding the select mark on iutools
        selectorit = pyautogui.locateCenterOnScreen('selector.png')
        logging.info('Found right answer radio at ' + str(selectorit))
        #screenshoting right answer
        pos1 = int(selectorit[0]) +15, int(selectorit[1]) -6
        scr = pyautogui.screenshot(region=(pos1[0], pos1[1], 50, 20))
        #founding right answer option on iu
        ansbtn = pyautogui.locateCenterOnScreen(scr, region=(0, 0, 960, 1080), confidence=0.7)
        if ansbtn != None:
            #selecting the right option on iu
            logging.info('Found right answer option on IU at ' + str(ansbtn))
            pyautogui.moveTo(ansbtn)
            pyautogui.click()
            #submiting the answer
            donebtn = pyautogui.locateCenterOnScreen('done.png', confidence=0.9)
            logging.info('Found done button at' + str(donebtn))
            pyautogui.moveTo(donebtn)
            pyautogui.click()
            logging.info('Done')
            #switching to next question on iutools
            nextbtn = pyautogui.locateCenterOnScreen('next.png')
            logging.info('Found next button at' + str(nextbtn))
            pyautogui.moveTo(nextbtn)
            pyautogui.click()
            logging.info('Next')
            time.sleep(0.5)
        else:
            logging.error('Answer button on IU not found')

        loops = loops + 1
        if loops >= tasks:
            break
   
def checkbox(tasks):
    loops = 0
    while pyautogui.locateCenterOnScreen('spinner.png') == None:   
        global currentask
        currentask += 1
        #founding the selected checkboxes on iutools
        checkbox1 = pyautogui.locateAllOnScreen('checkbox1.png')
        logging.info('Found right answer checkbox(es) at ' + str(checkbox1))
        #screenshoting right answers
        scrlist = []
        for x in list(checkbox1):
            pos1 = int(x[0]) +15, int(x[1]) -6
            scr = pyautogui.screenshot(region=(pos1[0], pos1[1], 75, 30))
            scrlist.append(scr)
        logging.info(scrlist)
        #founding right answer option on iu
        for x in list(scrlist):
            ansbtn = pyautogui.locateCenterOnScreen(scr, region=(0, 0, 960, 1080), confidence=0.7)
            if ansbtn != None:
                #selecting the right option on iu
                logging.info('Found right answer option on IU at ' + str(ansbtn))
                pyautogui.moveTo(ansbtn)
                pyautogui.click()
            #submiting the answer
            donebtn = pyautogui.locateCenterOnScreen('done.png', confidence=0.9)
            logging.info('Found done button at' + str(donebtn))
            pyautogui.moveTo(donebtn)
            pyautogui.click()
            logging.info('Done')
            #switching to next question on iutools
            nextbtn = pyautogui.locateCenterOnScreen('next.png')
            logging.info('Found next button at' + str(nextbtn))
            pyautogui.moveTo(nextbtn)
            pyautogui.click()
            logging.info('Next')
            time.sleep(0.5)
        else:
            logging.error('Answer button on IU not found')

        loops = loops + 1
        if loops >= tasks:
            break

def getiucode(link):
    regex = r"(?:https://interneturok.ru/school/lesson/)*(.*)(?:/homework/228696)"
    code = re.match(regex, link, re.MULTILINE).group(1)
    return code

def iutools(iucode):
    cmd = 'https://iutools.ru/solution/' + str(iucode)
    r = requests.get(cmd, headers= header)
    link = json.loads(r.content)[0]['link']
    return link

def getasks(ses, link):
    r = ses.get(link)
    nmbrs = r.html.find('span.adjust')
#    logging.info(nmbrs[-1].text)
    clnmbrs = []
    for x in nmbrs:
        nbr = str(x.text).lstrip('0')
        list.append(clnmbrs, int(nbr))
#    logging.info(clnmbrs)
    return clnmbrs[-1]

def inputfield(testlink):
    global currentask
    currentask += 1

    
#tasks = int(pyautogui.prompt(text='Введите количество вопростов в тесте', title='Количество вопросов' , default=''))
#hwmap = session.get('https://iutools.ru/hwmap/' + grade + '?quarter=' + quarter)
#logging.info('Hwmap link is ' + 'https://iutools.ru/hwmap/' + grade + '?quarter=' + quarter)
#twork = hwmap.html.find('a.twork')
#tworklinks = re.findall(regex, str(twork))
#logging.info(tworklinks)
#for x in tworklinks:
#    dotest(x)

sg.Titlebar(title="IUTest")
layout = [  [sg.Push(), sg.Text('IUTest'), sg.Push()],
            [sg.Push(), sg.Text('Класс', key='-grade-'), sg.InputText()],
            [sg.Push(), sg.Text('Четверть', key='-quarter-'), sg.InputText()],
            [sg.Button('', key='about', image_filename=infoimg, image_size=(32, 32)), sg.Button('', key='-instruction-', image_filename=bookimg, image_size=(32, 32)), sg.Push(), sg.Button('', key='-ok-', image_filename=nextimg, image_size=(32, 32))] ]
window = sg.Window('IUTest', layout, use_custom_titlebar=True , alpha_channel=.95, grab_anywhere=True, font=font, icon=capimg, titlebar_icon=capimg, keep_on_top=True)

#values 0 is grade, values 1 is quarter
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    elif event == 'about':
        sg.popup_ok('Эту программу создал Савелий находясь в академии будущего с 05.03.2022. Я сделал её чтобы облегчить учебу всем, но в первую очередь конечно же себе. Создана она на python. Исходный код можно посмотреть на Github: https://github.com/fMercury13/IUTest. Дата начала разработки: 31.03.2023', title = 'About', icon = capimg, font = font, no_titlebar=True, grab_anywhere=True)
    elif event == '-ok-':
        iucode = getiucode('https://interneturok.ru/school/lesson/45899/homework/228696')
        testlink = iutools(iucode)
        tasks = getasks(session, testlink)
        dotest('https://interneturok.ru/school/lesson/45899/homework/228696')
    elif event == '-instruction-':
        sg.popup_ok('Инструкция к программе: 1. Закройте все вкладки в браузере, а потом и сам браузер. 2. Введите ваш класс и четверть которую надо сделать. 3. Нажмите ОК и начнется выполнение тестов. Во время работы программы нельзя пользоваться ноутбуком, трогать клавиатуру и мышь, выключать ноутбук. Не все тесты можно сделать таким образом т.к. некоторые имеют уникальные вопросы. Не будут сделаны тесты по алгебре, геометрии, физике, биологии и английскому. Если вы столкнулись с какой-то проблемой, пишите мне на почту: mercury8591@outlook.com и я постараюсь её исправить.', title = 'Инструкция', icon = capimg, font = font, no_titlebar=True, grab_anywhere=True)
