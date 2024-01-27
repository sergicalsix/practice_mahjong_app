import gradio as gr

yaku_list = [
    "門前清自摸和", "立直", "一発", "ドラ", "平和","断么九",
    "白","發","中","東","南","西","北",
    "海底撈月", "河底撈魚", "嶺上開花", "槍槓", 
    "ダブル立直", "七対子", "混全帯幺九", "一気通貫",
    "三色同順", "三色同刻", "三槓子", "対々和",
    "三暗刻", "小三元", "混老頭", "二盃口",
    "純全帯幺九", "混一色", "清一色", 
]
#     "国士無双","大三元", "四暗刻", "小四喜",
#     "大四喜", "字一色", "緑一色", "清老頭",
#     "九蓮宝燈", "四槓子", "天和", "地和"
# ]



yaku_hand_dict = {
    "門前清自摸和":1, "立直":1, "一発":1, "ドラ":1, "平和":1,"断么九":1,
    "白":1,"發":1,"中":1,"東":1,"南":1,"西":1,"北":1,
    "海底撈月":1, "河底撈魚":1, "嶺上開花":1, "槍槓":1, 
    "ダブル立直":2, "七対子":2, "混全帯幺九":2, "一気通貫":2,
    "三色同順":2, "三色同刻":2, "三槓子":2, "対々和":2,
    "三暗刻":2, "小三元":2, "混老頭":2, "二盃口":3,
    "純全帯幺九":3, "混一色":3, "清一色":6, 
    "国士無双":13, "大三元":13, "四暗刻":13, "小四喜":13,
    "大四喜":13, "字一色":13, "緑一色":13, "清老頭":13,
    "九蓮宝燈":13, "四槓子":13, "天和":13, "地和":13
}

#ロン
parent_ron_points = {1:2000, 2:3900, 3:7700, 4:12000,5:12000,6:18000,7:18000,8:24000,9:24000,10:24000,11:36000,12:36000,13:48000}
children_ron_points = {1:1300, 2:2600, 3:5200, 4:8000,5:8000,6:12000,7:12000,8:16000,9:16000,10:16000,11:24000,12:24000,13:32000}

parent_pinhu_ron_points = {1:1500, 2:2900, 3:5800}
children_pinhu_ron_points = {1:1000, 2:2000, 3:3900}

parent_seven_pairs_ron_points = {2:2400, 3:4800, 4:9600}
children_seven_pairs_ron_points = {2:1600, 3:3200, 4:6400}

#ツモ
parent_tumo_points = {1:500, 2:1000, 3:2000, 4:4000,5:4000,6:6000,7:6000,8:8000,9:8000,10:8000,11:12000,12:12000,13:16000}
children_tumo_points = {1:"300-500", 2:"500-1000", 3:"1000-2000", 4:"2000-4000",5:"2000-4000",6:"3000-6000",7:"3000-6000",8:"4000-8000",9:"4000-8000",10:"4000-8000",11:"6000-12000",12:"6000-12000",13:"8000-16000"}

parent_pinhu_tumo_points = {2:700, 3:1300, 4:2600}
children_pinhu_tumo_points = {2:"400-700", 3:"700-1300", 4:"1300-2600"}

parent_seven_pairs_tumo_points = {3:1600, 4:3200}
children_seven_pairs_tumo_points = {3:"800-1600", 4:"1600-3200"}


#役から翻数と親子の点数を計算する関数
def calculate_score(selected_yaku):
    hand = 0
    flag_pinhu = False
    flag_seven_pairs = False
    flag_tumo = False

    parent_tumo_score, children_tumo_score, parent_ron_score, children_ron_score = 0, 0, 0, 0

    for yaku in selected_yaku:
        if yaku == "平和":
            flag_pinhu = True
        elif yaku == "七対子":
            flag_seven_pairs = True
        elif yaku == "門前清自摸和":
            flag_tumo = True
        hand += yaku_hand_dict[yaku] # 各役の翻数を加算

    if flag_pinhu and flag_seven_pairs:
        return -1, parent_tumo_score, children_tumo_score, parent_ron_score, children_ron_score 

    if hand > 13:
        hand = 13

    if flag_tumo:
        parent_tumo_score, children_tumo_score = parent_tumo_points[hand], children_tumo_points[hand]
        if hand <=4:
            if flag_pinhu:
                parent_tumo_score, children_tumo_score = parent_pinhu_tumo_points[hand], children_pinhu_tumo_points[hand]
            elif flag_seven_pairs:
                parent_tumo_score, children_tumo_score =  parent_seven_pairs_tumo_points[hand], children_seven_pairs_tumo_points[hand]
    
    else:
        parent_ron_score, children_ron_score = parent_ron_points[hand], children_ron_points[hand]
        if hand <=4:
            if flag_pinhu:
                parent_ron_score, children_ron_score = parent_pinhu_ron_points[hand], children_pinhu_ron_points[hand]
            elif flag_seven_pairs:
                parent_ron_score, children_ron_score =  parent_seven_pairs_ron_points[hand], children_seven_pairs_ron_points[hand]
        
    return hand, parent_tumo_score, children_tumo_score, parent_ron_score, children_ron_score 

#役と翻数をテキストで表示するための文字列を作る関数
def join_yaku_hand(selected_yaku):
    yaku_hand_text = ""
    for yaku in selected_yaku:
        yaku_hand_text += f"{yaku}({yaku_hand_dict[yaku]})"
    return yaku_hand_text


def mahjong_score_interface(selected_yaku):
    hand, parent_tumo_score, children_tumo_score, parent_ron_score, children_ron_score = calculate_score(selected_yaku)
    yaku_hand_text = join_yaku_hand(selected_yaku)
    if hand == -1:
        return f"選択された役({yaku_hand_text})は同時に成立できません。"
    elif parent_tumo_score == 0:
        return f"""
        選択された役: {yaku_hand_text}
        翻数: {hand}
        親(ロン): {parent_ron_score}
        子(ロン): {children_ron_score}
        (役満以上は全て13翻とした。)
        """
    return f"""
        選択された役: {yaku_hand_text}
        翻数: {hand}
        親(ツモ): {parent_tumo_score}オール
        子(ツモ): {children_tumo_score}
        (役満以上は全て13翻とした。)
        """

yaku_checkboxes = [gr.Checkbox(label=yaku) for yaku in yaku_list]

interface = gr.Interface(
    fn=mahjong_score_interface,
    inputs=[gr.components.CheckboxGroup(choices=yaku_list, label="役を選択")],
    outputs=gr.components.Textbox(label="翻数と親子の点数"),
    title="簡易版面前麻雀点数計算アプリ"
)

interface.launch()
