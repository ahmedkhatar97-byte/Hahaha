import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import os

# --- 🛡️ نظام فحص الأمان ---
# استبدل النجوم بمفتاحك الجديد (يفضل تعمل واحد جديد من Google AI Studio)
MY_API_KEY = "AIzaSyAN2p6_RGUqOCHf83ETrOXRV-0cDiDqfZI" 

st.set_page_config(page_title="X ASSISTANT v2", layout="wide")

# محاولة الاتصال وتحديد الخطأ بدقة
try:
    genai.configure(api_key=MY_API_KEY)
    # السطر ده بيجبر السيرفر ينسى v1beta خالص
    model = genai.GenerativeModel('gemini-1.5-flash')
    # فحص بسيط للاتصال
    test_list = genai.list_models()
    api_status = "✅ المتصل شغال"
except Exception as e:
    api_status = f"❌ مشكلة في المفتاح: {str(e)}"

st.markdown(f"<h1 style='text-align:center;'>⚡ X ASSISTANT v2</h1>", unsafe_allow_html=True)
st.sidebar.info(api_status)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# القائمة الجانبية (صور وصوت)
with st.sidebar:
    st.title("⚙️ الأدوات")
    img_file = st.file_uploader("📸 ارفع صورة", type=["jpg", "png", "jpeg"])
    audio = mic_recorder(start_prompt="سجل صوتك", stop_prompt="إرسال", key='mic')

# معالجة المدخلات
if prompt := st.chat_input("اسألني أي حاجة يا Harreef..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if img_file:
                img = Image.open(img_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # لو الـ API Key فيه مشكلة Permission، هيظهر هنا بوضوح
            st.error("⚠️ حصل خطأ في استلام الرد")
            if "PermissionDenied" in str(e):
                st.warning("المفتاح بتاعك ملوش صلاحية (Permission Denied). يرجى عمل API Key جديد من Google AI Studio.")
            else:
                st.info(f"الخطأ: {e}")
