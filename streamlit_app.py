import os
import streamlit as st
from cryptobot.src.bot.chat import CryptoChat

def initialize_chat():
    if "chat_bot" not in st.session_state:
        st.session_state.chat_bot = CryptoChat()

def main():
    st.title("Crypto助手")
    st.write("欢迎使用 Crypto 助手！我是您的加密货币和链上交易专家。")
    
    initialize_chat()
    
    if prompt := st.chat_input("请输入您的问题"):
        response = st.session_state.chat_bot.chat(prompt)
        st.write(response)

if __name__ == "__main__":
    main() 