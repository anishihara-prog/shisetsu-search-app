import streamlit as st
import pandas as pd
import re

st.title("施設一覧検索アプリ")

FILE_URL = "https://docs.google.com/spreadsheets/d/1caVKtJSJGkTq681J-fH6duvrOAHzY1uA/export?format=xlsx"

# ✅ タブ名ごとの内容マスタ
NAIYO_MASTER = {
    "相談支援事業所": [
        "計画","移行","定着","障害児","発達支援","生活介護","医療的ケア",
        "緊急受け入れ対応","強度行動障害","高次脳機能障害支援体制",
        "高齢者","特定相談支援","就労選択支援"
    ],
    "介護事業所": [
        "移動支援","重度訪問介護","居宅介護","行動援護","同行援護",
        "訪問介護","訪問看護","訪問入浴","医療ケア","訪問マッサージ",
        "精神","生活介護","難病","医療的","短期入所"
    ],
    "訪問看護": [
        "居宅介護","訪問介護","デイサービス","精神","介護予防",
        "認知症","リハビリ","フットケア","終末期","療養","医療"
    ],
    "地域活動支援": ["精神"],
    "就労支援": [
        "時給","日給","皆勤手当","精勤手当","送迎","昼食","PC","IT",
        "カフェ","パン","軽作業","在宅","内職","資格","選択","定着",
        "生活介護","就労"
    ],
    "生活介護": ["基準該当短期入所"],
    "共生型": ["生活介護","自立訓練(機能訓練 生活訓練)"],
    "療養介護": ["なし"],
    "グループホーム": [
        "女性棟","男性棟","マンションタイプ","ワンルームタイプ","個室",
        "手作り","短期入所","ペット可","日中サービス支援型",
        "自立生活援助","住宅型有料","精神","難病","医療","緊急受け入れ対応"
    ],
    "短期入所": [
        "計画","移行","定着","障害児","発達支援","生活介護","医療的ケア",
        "緊急受け入れ対応","強度行動障害","高次脳機能障害支援体制",
        "高齢者","特定相談支援","就労選択支援"
    ],
    "児童": [
        "中高","小中高","児童発達","送迎","重症医児","運動","療育",
        "就労","保育所等訪問支援","居宅訪問型"
    ]
}

@st.cache_data
def load_sheets():
    return pd.read_excel(FILE_URL, sheet_name=None)

all_sheets = load_sheets()

# ✅ ✅ ✅ タブ名プルダウンに「オプションを選択してください」を追加
tab_names = ["オプションを選択してください"] + list(all_sheets.keys())

selected_tab = st.selectbox(
    "Excelのタブ名（シート名）を選択",
    tab_names
)

# ✅ 選択されていない場合は処理を止める（誤爆防止）
if selected_tab == "オプションを選択してください":
    st.stop()

# ✅ 選択されたシートを読み込み
df = all_sheets[selected_tab]

# ✅ 内容プルダウン
naiyo_list = NAIYO_MASTER.get(selected_tab, [])
selected_naiyo = st.multiselect(
    "内容（複数選択できます）",
    naiyo_list,
    placeholder="オプションを選択してください"
)

#st.write("=== 使用している naiyo_list ===", naiyo_list)

# ✅ その他検索
shisetsu = st.text_input("施設名（部分一致）")
address = st.text_input("住所（部分一致）")
jigyosho = st.text_input("事業所（部分一致）")
jigyosho_no = st.text_input("事業所番号（完全一致）")
tel = st.text_input("電話番号（完全一致）")

# ✅ 検索処理
result = df.copy()

# ✅ 内容（語単位 AND 条件）
if selected_naiyo:
    for word in selected_naiyo:
        result = result[result["内容"].astype(str).str.contains(rf"\b{word}\b", na=False)]

# ✅ 部分一致検索
if shisetsu:
    result = result[result["施設名"].astype(str).str.contains(shisetsu, case=False)]

if address:
    result = result[result["住所"].astype(str).str.contains(address, case=False)]

if jigyosho:
    result = result[result["事業所"].astype(str).str.contains(jigyosho, case=False)]

# ✅ 完全一致
if jigyosho_no:
    result = result[result["事業所番号"].astype(str) == jigyosho_no]

if tel:
    result = result[result["電話番号"].astype(str) == tel]

st.write(f"検索結果：{len(result)} 件")

st.dataframe(result)
