from flask import Flask, render_template, request

app = Flask(__name__)

# Prompt templates
SIMPLIFIED_PROMPT = (
    "你是台灣地區的氣象預報專家。請即時查核多來源專業資料（如："
    "CWB、ECMWF/GFS、Himawari-8雲圖、地面觀測），綜合判讀並給出結論、"
    "關鍵依據與信心度。所有時間請以 Asia/Taipei 呈現，並附上引用來源。"
)

STANDARD_PROMPT = (
    "你是台灣地區的氣象預報專家。請整合 CWB、ECMWF/GFS、WRF、Himawari-8、"
    "地面觀測（風、濕度、能見度、露點差）等資料，對〔指定地點/時間〕的"
    "拍攝條件做專業判讀，並：\n\n"
    "以要點摘要 +『是否建議前往(Go/No-Go)』+ 信心度(0–100%) 回覆\n\n"
    "明列關鍵指標：雲量(高/中/低)、風速陣風、降雨機率、視程、露點差、"
    "穩定度/對流參數（如 CAPE）\n\n"
    "說明「最佳時窗」與「備用地點」與風險\n\n"
    "引用與時間戳註明資料來源（站名/跑次/格點時間）\n\n"
    "請以表格或條列清楚呈現；時區一律 Asia/Taipei。"
)

ASTRO_MODULE = (
    "若任務與銀河/星空拍攝相關，另外提供：\n\n"
    "天文條件：月相%、月高度、銀河中心高度/方位，可拍時窗\n\n"
    "透明度/視寧度估計、PWAT、水氣趨勢、低雲封頂高度\n\n"
    "光害/可替代拍攝點（含大略座標）\n\n"
    "『Milky Way Score 0–100』：雲量40%、月光25%、透明度15%、風10%、露點差5%、其他5%\n\n"
    "現地風險與裝備提醒（防潮、防風、結露）。"
)

SUNSET_MODULE = (
    "若任務為夕照判斷，另外提供：\n\n"
    "日落時間與太陽方位、最佳觀測方位\n\n"
    "中高雲覆蓋度(西側地平 10–30°、T-30 至 T+20 分)與低雲干擾\n\n"
    "風切/穩定度、霾/氣膠(能見度)\n\n"
    "『Sunset Glow Index 0–100』與最佳拍攝點。"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    prompt = None
    if request.method == 'POST':
        mode = request.form.get('mode')
        location = request.form.get('location', '')
        date = request.form.get('date', '')
        time_period = request.form.get('time_period', '')
        modules = request.form.getlist('modules')

        base_prompt = SIMPLIFIED_PROMPT if mode == 'simplified' else STANDARD_PROMPT
        user_context = f"\n\n查詢地點/範圍: {location}\n日期/期間: {date}\n時段: {time_period}\n"
        prompt = base_prompt + user_context

        if 'astro' in modules:
            prompt += "\n" + ASTRO_MODULE
        if 'sunset' in modules:
            prompt += "\n" + SUNSET_MODULE
    return render_template('index.html', prompt=prompt)

if __name__ == '__main__':
    app.run(debug=True)
