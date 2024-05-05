import api
from api import generate_role, get_characterglm_response
from data_types import TextMsg, filter_text_msg

import itertools
from typing import Iterator, List

# 風間
role_A_description = generate_role("生日7月19日，和好友小新、妮妮、正男、阿呆是雙葉幼稚園的向日葵班的同班同學藍色頭髮和卷翹的前劉海，家境富裕爸爸旅居國外工作，學識淵博到讓人不敢相信他只是個五歲小孩缺點是死要面子、愛炫耀、也很愛裝大人，不輕易表達自己的情緒")
# 楊過
role_B_description = generate_role("""
楊過，字改之，出生於江南，籍貫山東省。金庸武俠小說《神鵰俠侶》中的男主角，為金庸小說中武功最絕頂的高手之一。父母是《射鵰英雄傳》中的楊康和穆念慈（連載版（舊版）中生母為秦南琴），祖父母分别為楊鐵心和包惜弱；楊過亦是歐陽鋒之義子，小龍女之徒與丈夫，程英、陸無雙及郭襄的義兄，郭靖、黄蓉的義姪。自幼喪父，十一歲前由母親獨自養大。因一生深受郭靖大仁大義、為國為民、忠義等精神和品格的影響，加上黃蓉在其年幼時的教育，才不至於誤入歧途，重蹈父親楊康賣國和作惡忘恩的覆轍。
外貌極為俊美，智商聰明絕頂，或能比肩黃蓉，但出身貧寒，導致性格自卑偏激，常因為激憤，而衝動行事。
在書中初期雖不到二十歲，但因資質奇佳，武功在平輩之中屬最高者；中期斷臂之後遇重劍奇遇，重陽宮大戰以玄鐵重劍擊敗蒙古三傑，將尹克西的金龍鞭震得寸寸斷絕，甚至和金輪法王打成平手。與小龍女分别十六年後武藝大成，以部分九陰真經、玉女心經、蛤蟆功、玉簫劍法等武功及在山洪海潮中練成的剛猛內勁合拼，自創黯然銷魂掌，帶著人皮面具在江湖上行俠仗義被尊稱為“神鵰大俠”或“神鵰俠”。肉身接瑛姑三掌「寒陰箭」而毫髮無傷，在神鵰俠侶結束時，已為當世武功最高者之一，與周伯通及郭靖齊名，連黃藥師、一燈大師也自嘆不如，在第三次華山論劍時被封為“西狂”。
吳靄儀直言他就是令狐沖的前身，並點出他受歡迎的原因：「少年時代的冤屈之情，在楊過身上一一表露出來，自覺世人都看他不起，他們越是要卑賤他，他就越看不起他們。自卑往往使人偏激過度表現得自負，這種經驗很多人都有，少年人及文人分外敏感，因此感受也分外深刻。」。
""")

def output_stream_response(responses: List[str]) -> str:
    # 将列表中的所有响应合并成一个长字符串
    return "".join(responses)


def start_chat(rounds: int):
    query = "你好"
    history = []  # 初始化历史记录列表

    # 初始化对话的第一条消息
    history.append({"role": "user", "content": query})

    meta = {
        "user_info": role_A_description, # 風間
        "bot_info": role_B_description, # 楊過
        "bot_name": "楊過",
        "user_name": "風間"
    }

    for _ in range(rounds):  # 根据指定的轮数进行循环

        # 调用函数获取回应流
        response_stream = get_characterglm_response(filter_text_msg(history), meta)
        bot_responses = list(response_stream)  # 将生成器内容转换为列表

        combined_response = output_stream_response(bot_responses)
        if not combined_response:
            print("生成出错")
            history.pop()  # 移除最后一条历史记录以回退到上一状态
        else:
            # 将新的回应加入历史记录，并打印当前的历史记录
            speaker = "assistant" if history[-1]["role"] == "user" else "user"
            history.append({"role": speaker, "content": combined_response})
            print(history)

    # 将对话历史保存到文本文件
    save_conversation_to_file(history, "conversation_history.txt")

def save_conversation_to_file(history, file_name):
    """将对话历史保存到指定的文件中"""
    with open(file_name, 'w', encoding='utf-8') as file:
        for entry in history:
            line = f"{entry['content']}\n"
            file.write(line)
        print(f"对话已保存到文件：{file_name}")

# 示例调用，进行5轮对话
start_chat(50)
