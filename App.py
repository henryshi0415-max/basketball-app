import streamlit as st
import pandas as pd
import os

# --- 1. 基础配置 ---
st.set_page_config(page_title="篮球记录助手", layout="centered")

# 定义存储数据的文件名
DB_FILE = "basketball_stats.csv"

# --- 2. 数据加载与保存逻辑 ---
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["球员", "得分", "篮板", "助攻", "抢断"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# 初始化 Session State
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- 3. 网页头部 ---
st.title("🏀 场边技术统计")
st.write("点击按钮即刻记录，数据会自动保存。")

# --- 4. 侧边栏：添加球员 ---
with st.sidebar:
    st.header("阵容管理")
    new_name = st.text_input("球员姓名")
    if st.button("添加球员"):
        if new_name and new_name not in st.session_state.df["球员"].values:
            new_row = pd.DataFrame([[new_name, 0, 0, 0, 0]], columns=st.session_state.df.columns)
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            save_data(st.session_state.df)
            st.rerun()
    
    if st.button("清空所有数据", type="primary"):
        st.session_state.df = pd.DataFrame(columns=["球员", "得分", "篮板", "助攻", "抢断"])
        save_data(st.session_state.df)
        st.rerun()

# --- 5. 主界面：球员操作卡片 ---
if st.session_state.df.empty:
    st.info("请先在左侧菜单添加球员姓名 👈")
else:
    for index, row in st.session_state.df.iterrows():
        with st.container():
            # 显示球员姓名和当前主要得分
            st.markdown(f"### {row['球员']} (得分: {row['得分']})")
            
            # 手机端大按钮布局
            col1, col2, col3, col4 = st.columns(4)
            
            if col1.button("＋得分", key=f"p_{index}"):
                st.session_state.df.at[index, "得分"] += 1
                save_data(st.session_state.df)
                st.rerun()

            if col2.button("＋篮板", key=f"r_{index}"):
                st.session_state.df.at[index, "篮板"] += 1
                save_data(st.session_state.df)
                st.rerun()

            if col3.button("＋助攻", key=f"assist_{index}"):
                st.session_state.df.at[index, "助攻"] += 1
                save_data(st.session_state.df)
                st.rerun()

            # 撤销按钮（减1），防止手抖点错
            if col4.button("🔙", key=f"undo_{index}", help="减去 1 分"):
                if st.session_state.df.at[index, "得分"] > 0:
                    st.session_state.df.at[index, "得分"] -= 1
                    save_data(st.session_state.df)
                    st.rerun()
        st.markdown("---")

    # --- 6. 数据总表 ---
    st.subheader("全场统计摘要")
    st.table(st.session_state.df) # 使用 table 在手机端显示更稳固

    # 下载按钮
    csv_data = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("导出 CSV 文件", csv_data, "game_report.csv", "text/csv")
