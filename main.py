import vk_api
import random
import datetime

token = "c37b3bdf092530ff8d86cdb71bf46acf57991707861447dd66584db62b6425e4dd5684b018a0b810fa342"
mon_fa = 20
vk = vk_api.VkApi(token=token)

vk._auth_token()

now = datetime.datetime.now()
timeA = now.hour
BL = [True, False]
ENERG_MAX = 10
ENERG_HOUSE = 5
Curs = random.randint(10, 40)
org = 2000
c = 0
KAZIN_KOF = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.10, 0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 0.5, 0.75, 10, 0.25, 0.5, 0, 0.25, 0.5]


def construct(id, name, money, power):
    p = {}
    p["name"] = name
    p["money"] = money
    p["messegNumb"] = 0
    p["power"] = power
    p["famer"] = 1
    p["energe"] = 10
    p["resurs"] = 0
    p["xp"] = 0
    p["lvl_fam"] = 1
    data[str(id)] = p

    return "normal"


def perev(txt):
    a = txt
    return txt[::-1]


def savebd():
    with open("data.txt", "w") as file:
        for i in data:  # проходимся по data и получаем id в нем
            p = str(i) + " " + str(data[i]["name"]) + " " + str(data[i]["money"]) + " " + str(
                data[i]["messegNumb"]) + " " + str(data[i]["power"]) + " " + str(data[i]["famer"]) + " " \
                + str(data[i]["energe"]) + " " + str(data[i]["resurs"]) + " " + str(data[i]["xp"]) + ' ' + \
                str(data[i]["lvl_fam"])

            file.write(p + '\n')  # записываем в data.txt построчно пользователей


def loadbd():
    file = open("data.txt", "r")
    datas = file.read()
    datas = datas.splitlines()
    file.close()
    data = {}
    for i in datas:
        i = i.split()
        if len(i) > 4:  # проверка на полноту данных
            data[str(i[0])] = {}
            data[str(i[0])]["name"] = i[1]
            data[str(i[0])]["money"] = i[2]
            data[str(i[0])]["messegNumb"] = i[3]
            data[str(i[0])]["power"] = i[4]
            data[str(i[0])]["famer"] = i[5]
            data[str(i[0])]["energe"] = i[6]
            data[str(i[0])]["resurs"] = i[7]
            data[str(i[0])]["xp"] = i[8]
            data[str(i[0])]["lvl_fam"] = i[9]
    return (data)


def vib(a, b):
    l = [str(a), str(b)]
    return random.choice(l)


def stok(n):
    a = random.randint(1, 3)
    if int(n) == a:
        return True
    return False


def top():
    lst = []
    for i in data:
        lst.append((data[i]["name"], int(data[i]["money"])))
    lst = sorted(lst, key=lambda x: x[1], reverse=True)
    lst = lst[:10]
    return lst


def energ(n, cons):
    return cons - n


data = loadbd()  # загружаем в переменную data информацию из функции loadbd и файла data.txt

while True:
    # добавления монет каждый час пользователя
    # часть игровой механики бота
    try:
        now = datetime.datetime.now()
        timeB = now.hour
        if timeA < timeB:
            timeA = timeB

            for i in data:
                data[i]["money"] = str(int(data[i]["money"]) + int(data[i]["power"]))
                if int(data[i]["energe"]) < ENERG_MAX:
                    a = energ(int(data[i]["energe"]), ENERG_MAX)
                    if a <= ENERG_HOUSE:
                        data[i]["energe"] = int(data[i]["energe"]) + a
                    else:
                        data[i]["energe"] = int(data[i]["energe"]) + ENERG_HOUSE
                Curs = random.randint(10, 40)
                savebd()



        elif (timeA > timeB) and (timeB == 0):
            timeA = 0
            Curs = random.randint(10, 40)
            for i in data:
                data[i]["money"] = str(int(data[i]["money"]) + int(data[i]["power"]))
                if int(data[i]["energe"]) < ENERG_MAX:
                    a = energ(int(data[i]["energe"]), ENERG_MAX)
                    if a <= ENERG_HOUSE:
                        data[i]["energe"] = int(data[i]["energe"]) + a
                    else:
                        data[i]["energe"] = int(data[i]["energe"]) + ENERG_HOUSE
            savebd()
    except Exception:
        print(str(datetime.datetime.now()) + ' В это время произошла не извесная ошибка')
    messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})

    if messages["count"] >= 1:
        id = messages["items"][0]["last_message"]["from_id"]
        body = messages["items"][0]["last_message"]["text"]

        # авторизация пользователя в боте
        n = 0
        for i in data:
            if str(id) == i:
                n = 1
        if n == 0:
            construct(id, id, 10, 10)

        # простые команды
        if body.lower() == "начать":

            vk.method("messages.send",
                      {"peer_id": id, "message": "Привет! Напиши помощь", "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "кто я?":
            vk.method("messages.send",
                      {"peer_id": id, "message": "ты хороший человек и очередной нужный игрок нашего бота",
                       "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "топ":
            mes = f'Топ Игроков\n №  Ник(id)  Деньги\n'
            num1 = 1
            for i in top():
                mes += f'{num1}№ {i[0]}  {i[1]}$\n'
                num1 += 1
            vk.method("messages.send",
                      {"peer_id": id,
                       "message": mes,
                       "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "профиль":
            smg = "привет " + str(data[str(id)]["name"]) + "\n"
            smg = smg + str(data[str(id)]["money"]) + "$"
            smg = smg + "\n" + str(data[str(id)]["power"]) + " доход/в час"
            smg = smg + "\n" + str(data[str(id)]["famer"]) + " из " + str(org) + "ферм " + \
                  str(data[str(id)]["lvl_fam"]) + " уровня"
            smg = smg + "\n" + str(data[str(id)]["energe"]) + " из 10 энергии"
            smg = smg + "\n" + str(data[str(id)]["resurs"]) + " ресурсов"
            smg = smg + "\n" + str(data[str(id)]["xp"]) + " опыта"
            vk.method("messages.send", {"peer_id": id, "message": smg, "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "работать":
            if int(data[str(id)]["energe"]) >= 1:
                data[str(id)]["energe"] = int(data[str(id)]["energe"]) - 1
                if (100 * (int(data[str(id)]["xp"]) // 100)) < 5:
                    mon = 5
                else:
                    mon = 100 * (int(data[str(id)]["xp"])) // 100
                data[str(id)]["money"] = int(data[str(id)]["money"]) + mon
                data[str(id)]["xp"] = int(data[str(id)]["xp"]) + 1
                smg = f'Вы работая заработали {mon}$.' \
                      f'\nУ вас теперь {data[str(id)]["money"]}$.\n' \
                      f'У вас {data[str(id)]["energe"]} энергия.\n' \
                      f'Повышайте ваш опыт чтобы больше получать.'
                vk.method("messages.send", {"peer_id": id,
                                            "message": smg,
                                            "random_id": random.randint(1, 2147483647)})
            else:
                smg = 'У вас нет энергии. Энергия восполняется каждый час'
                vk.method("messages.send", {"peer_id": id,
                                            "message": smg,
                                            "random_id": random.randint(1, 2147483647)})
        elif body.lower() == "помощь":
            smg = f'Команды:\nНачать\nкто я?\nпрофиль\nник[желаемый ник]\nкупить ферму [1-3][кол-во]\nстаканчик [1-3]' \
                  f'[Деньги]\nпереверни [фраза]\nвыбери [слово] или [слово]\nкурс\nпродать ресурс [кол-во]' \
                  f'\nпродать фермы [кол-во]\nкопать [карьер/шахту/скважену]\nказино[сумма более 100$]\n' \
                  f'Топ\nработать\nтут есть промокод можешь попробывать угадать'
            vk.method("messages.send", {"peer_id": id,
                                        "message": smg,
                                        "random_id": random.randint(1, 2147483647)})
        elif body.lower() == 'курс':
            vk.method("messages.send", {"peer_id": id,
                                        "message": f"1 ресурс = {Curs} $", "random_id": random.randint(1, 2147483647)})
        elif body == 'ЯЛ':
            # Промокод
            data[str(id)]["money"] = int(data[str(id)]["money"]) + 1000
            vk.method("messages.send", {"peer_id": id,
                                        "message": f'Промокод на 1000$. Спасибо что вы с нами',
                                        "random_id": random.randint(1, 2147483647)})
        else:
            # состав кдм
            try:
                bodyone = body.split()
                if bodyone[0].lower() == "ник":
                    if len(bodyone) == 2:
                        data[str(id)]["name"] = bodyone[1]  # меняем имя пользователя в боте на новое

                        vk.method("messages.send", {"peer_id": id, "message": "ник изменен на " + str(bodyone[1]),
                                                    "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send",
                                  {"peer_id": id, "message": "Не указан ник на который требуется сменить" \
                                                             + str(bodyone[1]),
                                   "random_id": random.randint(1, 2147483647)})
                elif bodyone[0].lower() == "казино":
                    if len(bodyone) == 2:
                        if int(data[str(id)]["money"]) >= int(bodyone[1]) and int(bodyone[1]) >= 100:
                            kof = random.choice(KAZIN_KOF)
                            if kof < 1:
                                data[str(id)]["money"] = str(int(int(data[str(id)]["money"]) -
                                                                 (int(bodyone[1]) - (int(bodyone[1]) * kof))))
                            elif kof == 1:
                                pass
                            else:
                                data[str(id)]["money"] = str(int(int(data[str(id)]["money"])
                                                                 + int(int(bodyone[1]) * kof)) - int(bodyone[1]))
                            m = f'Вам выпал коффициент х{kof}. Вы на этом заработали {int(bodyone[1]) * kof}$.' \
                                f' Ваши средства на данный момент {data[str(id)]["money"]}$'
                            vk.method("messages.send",
                                      {"peer_id": id,
                                       "message": m,
                                       "random_id": random.randint(1, 2147483647)})
                        else:
                            vk.method("messages.send",
                                      {"peer_id": id,
                                       "message": 'У вас не достаточно средств для игры или вы ввели сумму меньше 100$',
                                       "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send",
                                  {"peer_id": id,
                                   "message": 'Введите команду казино [кол-во на которое будете играть]',
                                   "random_id": random.randint(1, 2147483647)})
                elif bodyone[0].lower() == "купить" and bodyone[1].lower() == 'ферму':
                    if len(bodyone) == 4:
                        lvl = int(bodyone[2])
                        number = int(bodyone[3])
                        if int(lvl) == 1 and (int(data[str(id)]["lvl_fam"]) == 1 or int(data[str(id)]["lvl_fam"]) == 0):
                            if int(data[str(id)]["famer"]) + number <= org and number * mon_fa <= \
                                    int(data[str(id)]["money"]):
                                data[str(id)]["lvl_fam"] = 1
                                data[str(id)]["money"] = str(int(data[str(id)]["money"]) - number * mon_fa)
                                data[str(id)]["power"] = str(int(data[str(id)]["power"]) + number * 10)
                                data[str(id)]["famer"] = str(int(data[str(id)]["famer"]) + number)
                                m = f'Вы купили {number} ферм за {number * mon_fa} $'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                            else:
                                m = f'У вас не хватает наличности или вы покупаете слишком много ферм.' \
                                    f' Цена 1 фермы 1 уровня 20$'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})

                        elif (int(lvl) == 2) and \
                                ((int(data[str(id)]["lvl_fam"]) == 2) or (int(data[str(id)]["lvl_fam"]) == 0)):
                            if int(data[str(id)]["famer"]) + number <= org and number * mon_fa <= \
                                    int(data[str(id)]["money"]):
                                data[str(id)]["lvl_fam"] = 2
                                data[str(id)]["money"] = str(int(data[str(id)]["money"]) - number * (mon_fa ** 2))
                                data[str(id)]["power"] = str(int(data[str(id)]["power"]) + number * 200)
                                data[str(id)]["famer"] = str(int(data[str(id)]["famer"]) + number)
                                m = f'Вы купили {number} ферм 2lvl за {number * mon_fa} $'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                            else:
                                m = f'У вас не хватает наличности или вы покупаете слишком много ферм.' \
                                    f' Цена 1 фермы 2 уровня 400'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})

                        elif int(lvl) == 3 and (int(data[str(id)]["lvl_fam"]) == 3 or
                                                int(data[str(id)]["lvl_fam"]) == 0):
                            if int(data[str(id)]["famer"]) + number <= org and number * mon_fa <= \
                                    int(data[str(id)]["money"]):
                                data[str(id)]["lvl_fam"] = 3
                                data[str(id)]["money"] = str(int(data[str(id)]["money"]) - number * (mon_fa ** 2 * 2))
                                data[str(id)]["power"] = str(int(data[str(id)]["power"]) + number * 400)
                                data[str(id)]["famer"] = str(int(data[str(id)]["famer"]) + number)
                                m = f'Вы купили {number} ферм 3lvl за {number * mon_fa ** 2 * 2} $'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                            else:
                                m = f'У вас не хватает наличности или вы покупаете слишком много ферм.' \
                                    f' Цена 1 фермы 3 уровня 800'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                        else:
                            m = f'Вам надо продать фермы и купить того уровня которого пожелаете т.к.' \
                                f' можно иметь фермы только одного лвла'
                            vk.method("messages.send",
                                      {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send",
                                  {"peer_id": id,
                                   "message": 'Введите команду купить ферму [уровень фермы] [кол-во]',
                                   "random_id": random.randint(1, 2147483647)})
                elif bodyone[0].lower() == "стаканчик":
                    if len(bodyone) == 3:
                        if int(data[str(id)]["money"]) >= int(bodyone[2]):
                            if stok(bodyone[1]):
                                data[str(id)]["money"] = str(int(data[str(id)]["money"]) + int(bodyone[2]))
                                m = f'Вы выиграли {bodyone[2]}$'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                            else:
                                data[str(id)]["money"] = str(int(data[str(id)]["money"]) - int(bodyone[2]))
                                m = f'Вы проиграли {bodyone[2]}$'
                                vk.method("messages.send",
                                          {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                        else:
                            vk.method("messages.send",
                                      {"peer_id": id, "message": 'У вас не достаточно средств',
                                       "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send",
                                  {"peer_id": id,
                                   "message": 'Не правильный формат',
                                   "random_id": random.randint(1, 2147483647)})
                elif bodyone[0].lower() == "переверни":
                    if len(bodyone) >= 2:
                        vk.method("messages.send",
                                  {"peer_id": id,
                                   "message": perev(' '.join(bodyone[1:])),
                                   "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send",
                                  {"peer_id": id,
                                   "message": 'Не правильный формат',
                                   "random_id": random.randint(1, 2147483647)})
                elif bodyone[0].lower() == "выбери" and bodyone[2].lower() == "или":
                    if len(bodyone) == 4:
                        vk.method("messages.send",
                                  {"peer_id": id,
                                   "message": vib(bodyone[1], bodyone[3]),
                                   "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send",
                                  {"peer_id": id,
                                   "message": 'Не правильный формат',
                                   "random_id": random.randint(1, 2147483647)})
                elif bodyone[0].lower() == "копать":
                    if len(bodyone) == 2:
                        if bodyone[1].lower() == 'карьер':
                            if int(data[str(id)]["energe"]) >= 1:
                                if int(data[str(id)]["xp"]) >= 0:
                                    r = random.randint(1, 4)
                                    data[str(id)]["resurs"] = int(data[str(id)]["resurs"]) + r
                                    data[str(id)]["energe"] = int(data[str(id)]["energe"]) - 1
                                    data[str(id)]["xp"] = int(data[str(id)]["xp"]) + 2
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": f"Вы выкопали {r} ресурсов. У вас {data[str(id)]['resurs']}"
                                                          f" ресурсов и {data[str(id)]['energe']} энергии",
                                               "random_id": random.randint(1, 2147483647)})
                                else:
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": f"У вас не хватает опыта. У вас: {data[str(id)]['xp']}. Надо 0",
                                               "random_id": random.randint(1, 2147483647)})
                            else:
                                vk.method("messages.send",
                                          {"peer_id": id,
                                           "message": f"У вас нет энергии для выполнения этого действия. "
                                                      f"Энергия востанавливается каждый час",
                                           "random_id": random.randint(1, 2147483647)})
                        elif bodyone[1].lower() == 'шахту':
                            if int(data[str(id)]["energe"]) >= 1:
                                if int(data[str(id)]["xp"]) >= 100:
                                    r = random.randint(5, 10)
                                    data[str(id)]["resurs"] = int(data[str(id)]["resurs"]) + r
                                    data[str(id)]["energe"] = int(data[str(id)]["energe"]) - 1
                                    data[str(id)]["xp"] = int(data[str(id)]["xp"]) + 5
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": f"Вы выкопали {r} ресурсов. У вас {data[str(id)]['resurs']}"
                                                          f" ресурсов и {data[str(id)]['energe']} энергии",
                                               "random_id": random.randint(1, 2147483647)})
                                else:
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": f"У вас не хватает опыта. У вас: {data[str(id)]['xp']}. Надо 100",
                                               "random_id": random.randint(1, 2147483647)})
                            else:
                                vk.method("messages.send",
                                          {"peer_id": id,
                                           "message": f"У вас нет энергии для выполнения этого действия. "
                                                      f"Энергия востанавливается каждый час",
                                           "random_id": random.randint(1, 2147483647)})
                        elif bodyone[1].lower() == 'скважену':
                            if int(data[str(id)]["energe"]) >= 1:
                                if int(data[str(id)]["xp"]) >= 200:
                                    r = random.randint(10, 20)
                                    data[str(id)]["resurs"] = int(data[str(id)]["resurs"]) + r
                                    data[str(id)]["energe"] = int(data[str(id)]["energe"]) - 1
                                    data[str(id)]["xp"] = int(data[str(id)]["xp"]) + 10
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": f"Вы выкопали {r} ресурсов. У вас {data[str(id)]['resurs']}"
                                                          f" ресурсов и {data[str(id)]['energe']} энергии",
                                               "random_id": random.randint(1, 2147483647)})
                                else:
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": f"У вас не хватает опыта. У вас: {data[str(id)]['xp']}. Надо 200",
                                               "random_id": random.randint(1, 2147483647)})
                            else:
                                vk.method("messages.send",
                                          {"peer_id": id,
                                           "message": f"У вас нет энергии для выполнения этого действия. "
                                                      f"Энергия востанавливается каждый час",
                                           "random_id": random.randint(1, 2147483647)})
                    else:
                        vk.method("messages.send",
                                  {"peer_id": id, "message": "Уточните что копать. Карьер, шахту или скважену",
                                   "random_id": random.randint(1, 2147483647)})
                elif bodyone[0].lower() == "продать":
                    if len(bodyone) > 1:
                        # Если вдруг что удалить
                        if bodyone[1].lower() == "фермы":
                            if len(bodyone) > 2:
                                try:
                                    a = int(bodyone[2])
                                    if int(data[str(id)]["famer"]) > a:
                                        data[str(id)]["famer"] = int(data[str(id)]["famer"]) - a
                                        if int(data[str(id)]["lvl_fam"]) == 1:
                                            data[str(id)]["famer"] = int(data[str(id)]["famer"]) - a
                                            data[str(id)]["power"] = str(int(data[str(id)]["power"]) - a * 10)
                                            c = 10
                                        elif int(data[str(id)]["lvl_fam"]) == 2:
                                            data[str(id)]["famer"] = int(data[str(id)]["famer"]) - a
                                            data[str(id)]["power"] = str(int(data[str(id)]["power"]) - a * 200)
                                            c = 100
                                        elif int(data[str(id)]["lvl_fam"]) == 3:
                                            data[str(id)]["famer"] = int(data[str(id)]["famer"]) - a
                                            data[str(id)]["power"] = str(int(data[str(id)]["power"]) - a * 400)
                                            c = 400
                                    elif int(data[str(id)]["famer"]) == a:
                                        if int(data[str(id)]["lvl_fam"]) == 1:
                                            data[str(id)]["famer"] = int(data[str(id)]["famer"]) - a
                                            data[str(id)]["power"] = str(int(data[str(id)]["power"]) - a * 10)
                                            data[str(id)]["lvl_fam"] = 0
                                            c = 10
                                        elif int(data[str(id)]["lvl_fam"]) == 2:
                                            data[str(id)]["famer"] = int(data[str(id)]["famer"]) - a
                                            data[str(id)]["power"] = str(int(data[str(id)]["power"]) - a * 200)
                                            data[str(id)]["lvl_fam"] = 0
                                            c = 100
                                        elif int(data[str(id)]["lvl_fam"]) == 3:
                                            data[str(id)]["famer"] = int(data[str(id)]["famer"]) - a
                                            data[str(id)]["power"] = str(int(data[str(id)]["power"]) - a * 400)
                                            data[str(id)]["lvl_fam"] = 0
                                            c = 400
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": id,
                                                   "message": "У вас нет такого кол во ферм",
                                                   "random_id": random.randint(1, 2147483647)})
                                        raise Exception
                                    data[str(id)]["money"] = int(data[str(id)]["money"]) + a * c
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": f"Вы продали {a} ферм за {a * c} монет",
                                               "random_id": random.randint(1, 2147483647)})
                                except Exception:
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": "Укажите количиство цыфрами",
                                               "random_id": random.randint(1, 2147483647)})
                        elif bodyone[1].lower() == "ресурсы":
                            if len(bodyone) > 2:
                                try:
                                    a = int(bodyone[2])
                                    if int(data[str(id)]["resurs"]) >= a:
                                        data[str(id)]["resurs"] = int(data[str(id)]["resurs"]) - a
                                        data[str(id)]["money"] = int(data[str(id)]["money"]) + a * Curs
                                        vk.method("messages.send",
                                                  {"peer_id": id,
                                                   "message": f"Вы продали {a} ресурсов за {a * Curs} монет",
                                                   "random_id": random.randint(1, 2147483647)})
                                    else:
                                        vk.method("messages.send",
                                                  {"peer_id": id,
                                                   "message": "У вас нет столько ресурсов",
                                                   "random_id": random.randint(1, 2147483647)})

                                except Exception:
                                    vk.method("messages.send",
                                              {"peer_id": id,
                                               "message": "Укажите количиство цыфрами",
                                               "random_id": random.randint(1, 2147483647)})
                            else:
                                vk.method("messages.send",
                                          {"peer_id": id,
                                           "message": "Укажите количиство",
                                           "random_id": random.randint(1, 2147483647)})
                        else:
                            vk.method("messages.send",
                                      {"peer_id": id,
                                       "message": "Укажите что хотите продать",
                                       "random_id": random.randint(1, 2147483647)})
                else:
                    pass
            except Exception:
                pass

        savebd()
