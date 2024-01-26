import gradio as gr

yaku_list = [
    "立直", "門前清自摸和", "一発", "ドラ", 
    "海底撈月", "河底撈魚", "嶺上開花", "槍槓", 
    "ダブル立直", "七対子", "混全帯幺九", "一気通貫",
    "三色同順", "三色同刻", "三槓子", "対々和",
    "三暗刻", "小三元", "混老頭", "二盃口",
    "純全帯幺九", "混一色", "清一色", "国士無双",
    "大三元", "四暗刻", "小四喜",
    "大四喜", "字一色", "緑一色", "清老頭",
    "九蓮宝燈", "四槓子", "天和",
    "地和",
]

yaku_hand = {
    "立直":1, "門前清自摸和":1, "一発":1, "ドラ":1, 
    "海底撈月":1, "河底撈魚":1, "嶺上開花":1, "槍槓":1, 
    "ダブル立直":2, "七対子":1.5, "混全帯幺九":2, "一気通貫":2,
    "三色同順":2, "三色同刻":2, "三槓子":2, "対々和":2,
    "三暗刻":2, "小三元":2, "混老頭":2, "二盃口":3,
    "純全帯幺九":3, "混一色":3, "清一色":6, "国士無双":13,
    "大三元":13, "四暗刻":13, "小四喜":13,
    "大四喜":13, "字一色":13, "緑一色":13, "清老頭":13,
    "九蓮宝燈":13, "四槓子":13, "天和":13,
    "地和":13, 
}

parent_points = {1:2000, 1.5:2400, 2:3900, 2.5:4800,3:7700, 3.5:9600,4:12000,5:12000,6:18000,7:18000,8:24000,9:24000,10:36000,11:36000,12:36000,13:48000}
children_points = {1:1000, 2:2000, 3:3900, 4:8000,5:8000,6:12000,7:12000,8:16000,9:16000,10:24000,11:24000,12:24000,13:32000}

def calculate_score(selected_yaku):
    hand = 0
    for yaku in selected_yaku:
        # 各役の翻数を加算
        hand += yaku_hand[yaku]
    if hand > 13:
        hand = 13
    # 少数点以下切り捨て
    elif hand > 4:
        hand = int(hand)

    return hand, parent_points[hand], children_points[hand]



def mahjong_score_interface(selected_yaku):
    hand, parent_score, children_score = calculate_score(selected_yaku)
    return f"選択された役: {selected_yaku}\n翻数: {hand}\n(役満以上は全て13翻、七対子は1.5翻とした。)\n親の点数: {parent_score}\n子の点数: {children_score}"

yaku_checkboxes = [gr.Checkbox(label=yaku) for yaku in yaku_list]

interface = gr.Interface(
    fn=mahjong_score_interface,
    inputs=[gr.components.CheckboxGroup(choices=yaku_list, label="役を選択")],
    outputs="text",
    title="簡易版麻雀点数計算アプリ"
)

interface.launch(share=True)
