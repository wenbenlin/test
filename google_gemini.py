import streamlit as st
import google.generativeai as genai

genai.configure(api_key='AIzaSyDd3iw5YvLE5q66wlzwtQN0HeS7ZGrCs7c')

def generate_response(prompt):
    # 調用 ChatGPT 模型生成回應
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt) # 動手實作：執行同一個問題 => 將執行結果貼到聊天室上
    return response.text

# Streamlit 介面
st.title("ChatGPT Streamlit Demo")

# 用戶輸入框
user_input = st.text_input("輸入你的訊息：", "")

# 按下按鈕後生成 ChatGPT 回應
if st.button("送出"):
    if user_input:
        # 顯示用戶的輸入
        st.text(f"你： {user_input}")

        # 使用 ChatGPT 生成回應
        google_response = generate_response(user_input)

        # 顯示 ChatGPT 的回應
        st.text(f"ChatGPT： {google_response}")
    else:
        st.warning("請輸入訊息後再點擊送出。")