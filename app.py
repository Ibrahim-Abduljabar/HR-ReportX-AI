import streamlit as st
import pandas as pd
import requests
import PyPDF2

st.set_page_config(page_title="HR ReportX AI", layout="wide")

API_KEY = st.secrets["API_hrhr"]

st.title("HR ReportX AI")
st.write("منصة توليد تقارير الموارد البشرية باستخدام Groq Llama 3.3 70B.")

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
            if uploaded_file.type in [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "text/csv"
            ]:
                df = pd.read_csv(uploaded_file) if uploaded_file.type == "text/csv" else pd.read_excel(uploaded_file)
                file_text = df.to_string()

            elif uploaded_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        file_text += text

        final_input = f"""
عنوان التقرير: {title}
وصف التقرير: {desc}

محتوى الملف:
{file_text}
        """

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": f"حلل البيانات التالية واكتب تقرير HR احترافي ومفصل:\n\n{final_input}"
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=15
            )

            st.write("Status:", response.status_code)

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                st.success("تم توليد التقرير!")
                st.write(content)
            else:
                st.error(response.text)

        except Exception as e:
            st.error(f"خطأ غير متوقع: {e}")

for form_id in st.session_state.forms:
    render_form(form_id)

if st.button("إضافة تقرير جديد"):
    st.session_state.forms.append(len(st.session_state.forms) + 1)

st.markdown("---")
st.markdown("### اضغط Ctrl + P لتحويل الصفحة إلى PDF")
