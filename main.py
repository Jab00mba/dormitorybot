import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
# from background import keep_alive

key = 'vk1.a.cYbZSudlLlL1Ix-bfRR-49y0cTdMVpS-p3-QwAIa3gXhyPaJgHMGevLHIyjmH4GdX3mfFqXIsiew5cZTBpNYBRszbtH-BB4ruOYeqtwqIvdk4hm4jUQ_VZ8S0jB_J_F5m3TOPYueRytCsY8yIuK1bhJKl_34UsJQmIMjYG9BweICunBdhf7qyrF8uYQtheFJzSIdvqOtZwn4MlECxwrtEA'

vk_session = vk_api.VkApi(token=key)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

contacts = '''
Помощник проректора по административно-хозяйственной работе:
Кравченко Галина Валерьевна
Тел.: +74996008080, доб. 31848
Email: kravchenko_g@mirea.ru

Заведующий общежитием:
Гуккаев Владимир Михайлович
Тел.: +74996008080, доб. 35330
Email: vladmgupi@mail.ru

Заместитель зав. общежитием
Ларионов Алексей Сергеевич
Тел.: +74996008080, доб. 35331
Email: larionov_a@mirea.ru

Паспортист общежития:
Гурджи Ольга Дмитриевна
Тел.: +74996008080, доб. 21189
'''

about = "https://student.mirea.ru/regulatory_documents/?LINK=accordion-11-body-03#accordion-11-heading-03"
rules = "https://www.mirea.ru/upload/iblock/db1/mek7dw2judaj51eljktxhe764f703hzv/Pravila-vnutrennego-rasporyadka-v-studencheskikh-obshchezhitiyakh_prover_2023.pdf"


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('расписание смены белья', 'positive')],
        [get_but('контакты администрации', 'positive')]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def send_msg(id, some_text):
    session_api.messages.send(
        user_id=id,
        forward_messages=0,
        message=some_text,
        random_id=0,
        keyboard=keyboard
    )


with open('schedule.txt') as f:
    f = f.read().split()
    schedule = {}
    schedule[f[0]] = f[1:-1]



# keep_alive()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == "hi":
                send_msg(id, msg.upper())
            if msg == "контакты администрации":
                send_msg(id, contacts)
            if msg == "правила проживания":
                send_msg(id,
                         'https://www.mirea.ru/upload/iblock/db1/mek7dw2judaj51eljktxhe764f703hzv/Pravila-vnutrennego-rasporyadka-v-studencheskikh-obshchezhitiyakh_prover_2023.pdf')
            if msg == "Нормативные документы":
                send_msg(id,
                         "https://student.mirea.ru/regulatory_documents/?LINK=accordion-11-body-03#accordion-11-heading-03")
            if msg == "расписание смены белья":
                send_msg(id, f"в этом месяце смена белья производится по следующим числам:\n{(' ').join(schedule['Month'])}")
