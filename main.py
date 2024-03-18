import os
import re
import random
import vk_api
import time
from threading import Thread

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

templates = ['1', '2']
peers = []
messages = []
typing_type = "typing"
gamlet = 0
print(len(peers))

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)
def check_peer(input_str):
    pattern = r'^-?\d+$' # регулярное выражение для цифр и знака минус
    if re.match(pattern, input_str):
        return True
    else:
        return False

#token = os.environ['TOKEN']
token = ""
peerID = ""
vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
vk_session._auth_token()
vk = vk_session.get_api()

def get_dialogs():
  result = ""
  response = vk.messages.getConversations(count=20)
  for items in response['items']:
    if items['conversation']['peer']['type'] == 'user':
      fname = vk.users.get(user_ids=items['conversation']['peer']['id'])
      #print(fname)
      fname = color.BOLD + fname[0]['first_name']+' '+fname[0]['last_name'] + color.END
      result += fname + " | ChatID: " + str(items['conversation']['peer']['id']) + " | Сообщение: " + items['last_message']['text'][:100] + "\n"
    elif items['conversation']['peer']['type'] == 'chat':
      title = color.BOLD + items['conversation']['chat_settings']['title'] + color.END
      result += title + " | ChatID: " + str(items['conversation']['peer']['id']) + " | Сообщение: " + items['last_message']['text'][:100] + "\n"
  os.system('cls')
  print(result)
  print("Теперь выбери чат, скопируй его ChatID и введи в peer_id для начала спама!\n")

#def remover(message_id, peer_id):
#  vk.messages.delete(message_ids=message_id, peer_id=peer_id, delete_for_all=1)

def worker():
    while True:
      if len(peers) == 0:
        time.sleep(4)
      elif len(peers) > 0:
        for i in peers:
          try:
            vk.messages.setActivity(peer_id=i,type=typing_type)
          except:
            print('В чате '+i+' произошла ошибка при наборе.')
        time.sleep(10)
def gamlet_worker():
  while True:
    global messages
    if gamlet == 1:
      cycle = 1
      for i in peers:
        cycle += 1
        try:
          messages.append(vk.messages.send(peer_id=i, random_id=random.randint(1, 999999999), message=templates[random.randint(0, len(templates)-1)]))
        except:
          print('В чате '+i+' произошла ошибка при отправке сообщения.')
      time.sleep(30)
      for a in messages:
        try: vk.messages.delete(message_ids=a, delete_for_all=1)
        except (RuntimeError, TypeError, NameError):
          pass
        time.sleep(5)
      messages = []
      time.sleep(10)
      
Thread(target=worker).start()
Thread(target=gamlet_worker).start()

while True:
  if len(token) < 75:
    os.system('cls')
    print("VK Crazy Typing Reborn")
    print("Токен можно получить здесь: vkhost.github.io")
    print("Пожалуйста, введите полученный токен:")
    token = input()
    vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
    vk_session._auth_token()
    vk = vk_session.get_api()
  if len(peers) == 0:
    print("Вам необходимо добавить хотя бы одну из бесед для начала работы скрипта!\n"
          + color.GREEN +
         "1. Получить список диалогов.\n2. Ввести peer_id" + color.END)
    select = input()
    if select == "1":
      os.system('cls')
      print("Смотрю последние диалоги... Подожди немного...\n")
      get_dialogs()
    elif select == "2":
      input_str = input("Введите peer_id: ")
      if check_peer(input_str):
        peers.append(input_str)
        print("Добавлено:" + peers[-1])
        time.sleep(1.5)
        os.system('cls')
      else:
        print(color.RED + "Строка содержит недопустимые символы или введён пустой запрос. Пожалуйста, проверьте, нет ли пробелов." + color.END)
        time.sleep(1.5)
        os.system('cls')
    else:
      print ("Не понимаю команду. Введите только цифру.")
      os.system('cls')
  if len(peers) > 0:
    print(color.GREEN + "Статус: Включён!\n"
          + color.END +
          "(Для прекращения спама закройте скрипт или удалите диалог из списка для спама)\n\n"
          "Выберите опцию:\n"
          + color.GREEN +
         "1. Получить список диалогов.\n2. Добавить диалог.\n"
          + color.END + color.RED +
          "3. Удалить диалог.\n4. Режим призрака 👻 (Быстрая отправка и удаление сообщений)\n" 
          + color.END +
          "5. Сменить метод набора (Текущий - "
          + typing_type +
          ")"
         )
    select = input()
    if select == "1":
      get_dialogs()
    elif select == "2":
      input_id = input("Введите peer_id: ")
      exist_count = peers.count(input_id)
      # Проверяем, есть ли он в списке
      if exist_count > 0:
        print("Такой диалог уже добавлен!")
      elif check_peer(input_id):
        peers.append(input_id)
        print(color.GREEN + "Добавлено: " + peers[-1] + color.END)
        time.sleep(1.5)
        os.system('cls')
      else:
        print(color.RED + "Строка содержит недопустимые символы или введён пустой запрос. Пожалуйста, проверьте, нет ли пробелов." + color.END)
        time.sleep(1.5)
        os.system('cls')
    elif select == "3":
      input_id = input("Введите peer_id для удаления: ")
      exist_count = peers.count(input_id)
      # Проверяем, есть ли он в списке для удаления
      if exist_count == 0:
        print("Такого диалога нет.")
        time.sleep(1.5)
        os.system('cls')
      else:
        peers.remove(input_id)
        print(color.RED + "Удалено: " + input_id + color.END)
        time.sleep(1.5)
        os.system('cls')
    elif select == "4":
      if gamlet == 0:
        gamlet = 1
        print("Включено!")
      else:
        gamlet = 0
        print("Выключено!")
      time.sleep(1.5)
      os.system('cls')
    elif select == "5":
      if typing_type == "typing":
        typing_type = "audiomessage"
        print('Изменено на аудиосообщение')
        time.sleep(1.5)
        os.system('cls')
      else:
        typing_type = "typing"
        print('Изменено на текстовый набор')
        time.sleep(1.5)
        os.system('cls')
    else:
      print ("Не понимаю команду. Введите только цифру.")
      time.sleep(1.5)
      os.system('cls')
