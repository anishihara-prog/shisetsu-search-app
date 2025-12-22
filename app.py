import streamlit as st
import pandas as pd
import re

st.title("事業所一覧検索アプリ")

FILE_URL = "https://docs.google.com/spreadsheets/d/1caVKtJSJGkTq681J-fH6duvrOAHzY1uA/export?format=xlsx&v=5"

# ✅ まず施設名をトップに表示（UI順だけ先に）
shisetsu = st.text_input("施設名（部分一致）")

# ✅ 次にタブ選択
def load_sheets():
    return pd.read_excel(FILE_URL, sheet_name=None)

all_sheets = load_sheets()

tab_names = ["オプションを選択してください"] + list(all_sheets.keys())
selected_tab = st.selectbox("Excelのタブ名（シート名）を選択", tab_names)

if selected_tab == "オプションを選択してください":
    st.stop()

# ✅ シート読み込み
df = all_sheets[selected_tab].copy()

# ✅ 列名整形
df.columns = df.columns.str.strip().str.replace("\n", "", regex=False)

# ✅ 住所列の統一
ADDRESS_CANDIDATES = ["住所", "所在地", "住所地", "住所１", "住所1", "所在地住所"]
for col in ADDRESS_CANDIDATES:
    if col in df.columns:
        df = df.rename(columns={col: "住所"})
        break

# ✅ 内容プルダウン
NAIYO_MASTER = {...}  # ← ここはあなたの元の辞書をそのまま入れてください

naiyo_list = NAIYO_MASTER.get(selected_tab, [])
selected_naiyo = st.multiselect("内容（複数選択できます）", naiyo_list)

# ✅ その他検索
address = st.text_input("住所（部分一致）")
jigyosho = st.text_input("事業所（部分一致）")
jigyosho_no = st.text_input("事業所番号（完全一致）")
tel = st.text_input("電話番号（完全一致）")

# ✅ 検索処理
result = df.copy()

if selected_naiyo:
    for word in selected_naiyo:
        result = result[result["内容"].astype(str).str.contains(rf"\b{word}\b", na=False)]

if shisetsu and "施設名" in result.columns:
    result = result[result["施設名"].astype(str).str.contains(shisetsu, case=False)]

if address and "住所" in result.columns:
    result = result[result["住所"].astype(str).str.contains(address, case=False)]

if jigyosho and "事業所" in result.columns:
    result = result[result["事業所"].astype(str).str.contains(jigyosho, case=False)]

if jigyosho_no and "事業所番号" in result.columns:
    result = result[result["事業所番号"].astype(str) == jigyosho_no]

if tel and "電話番号" in result.columns:
    result = result[result["電話番号"].astype(str) == tel]

st.write(f"検索結果：{len(result)} 件")
st.dataframe(result)






