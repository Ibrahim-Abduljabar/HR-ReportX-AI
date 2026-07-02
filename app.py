import streamlit as st
import pandas as pd
import requests
import PyPDF2
from google.colab import userdata

st.set_page_config(page_title="HR ReportX AI", layout="wide")

API_KEY = userdata.get("API_hrhr")

st.title("HR ReportX AI")
st.write("منصة توليد تقارير HR باستخدام requests فقط.")

if "forms" not in st.session_state:
    st.session_state.forms = [1]

def render_form(form_id):
    st.subheader(f"تقرير رقم {form_id}")

    title = st.text_input(f"عنوان التقرير {form_id}", key=f"title_{form_id}")
    desc = st.text_area(f"وصف التقرير {form_id}", key=f"desc_{form_id}")

    uploaded_file = st.file_uploader(
        f"ارفع ملف Excel أو PDF للتقرير {form_id}",
        type=["xlsx", "xls", "csv", "pdf"],
        key=f"file_{form_id}"
    )

    if st.button(f"توليد التقرير {form_id}", key=f"generate_{form_id}"):

        file_text = ""
        if uploaded_file:
            if uploaded_file.type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/csv"]:
                df = pd.read_csv(uploaded_file) if uploaded_file.type == "text/csv" else pd.read_excel(uploaded_file)
                file_text = df.to_string()

            elif uploaded_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                for page in reader.pages:
                    file_text += page.extract_text()

        payload = {
            "title": title,
            "description": desc,
            "file_content": file_text
        }

        headers = {"Authorization": f"Bearer {API_KEY}"}

        response = requests.post(
            "https://example.com/hr-reportx-ai",  # رابط API الوهمي
            json=payload,
            headers=headers
        )

        st.success("تم توليد التقرير بنجاح!")
        st.write("نتيجة الـ API:")
        st.write(response.text if response.status_code == 200 else "خطأ في الاتصال بالـ API")

for form_id in st.session_state.forms:
    render_form(form_id)

if st.button("إضافة تقرير جديد"):
    st.session_state.forms.append(len(st.session_state.forms) + 1)
    st.experimental_rerun()

st.markdown("---")
st.markdown("### لتحويل الصفحة إلى PDF اضغط **Ctrl + P**")
