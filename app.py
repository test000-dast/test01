import streamlit as st
import pandas as pd
import altair as alt

# ตั้งค่าหน้า Dashboard
st.set_page_config(page_title="Multi-File Dashboard", page_icon="📊", layout="wide")

# ✅ อัปโหลดไฟล์ CSV (หลายไฟล์)
uploaded_files = st.file_uploader("📂 อัปโหลดไฟล์ CSV", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # อ่านข้อมูลจากไฟล์
        df = pd.read_csv(file)

        if df.empty:
            st.warning(f"⚠️ ไฟล์ **{file.name}** ไม่มีข้อมูล")
            continue

        columns = df.columns.tolist()

        # ให้ผู้ใช้เลือกคอลัมน์ X และ Y
        x_axis = st.sidebar.selectbox(f"📌 เลือกแกน X ({file.name})", columns, key=f"x_{file.name}")
        y_axis = st.sidebar.selectbox(f"📌 เลือกแกน Y ({file.name})", columns, key=f"y_{file.name}")

        chart_title = st.sidebar.text_input(f"📝 ชื่อกราฟ ({file.name})", f"กราฟของ {file.name}")

        if x_axis and y_axis and pd.api.types.is_numeric_dtype(df[y_axis]):
            sort_order = st.sidebar.checkbox(f"🔽 เรียงจากมากไปน้อย ({file.name})", value=True, key=f"sort_{file.name}")

            # เรียงข้อมูลถ้าเลือกตัวเลือกนี้
            if sort_order:
                df = df.sort_values(by=y_axis, ascending=False)

            # แสดงกราฟ
            x_type = 'ordinal' if df[x_axis].dtype == object else 'quantitative'

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),
                y=alt.Y(y_axis, type='quantitative')
            ).properties(title=chart_title, width=1000, height=500)

            # เพิ่มตัวเลขบนหัวแท่ง
            text = alt.Chart(df).mark_text(
                align='center', baseline='bottom', dy=-5, fontSize=12, color='black'
            ).encode(
                x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),
                y=alt.Y(y_axis, type='quantitative'),
                text=y_axis
            )

            st.altair_chart(chart + text, use_container_width=True)

        else:
            st.warning(f"⚠️ กรุณาเลือกคอลัมน์ที่ถูกต้องสำหรับไฟล์ **{file.name}**")
