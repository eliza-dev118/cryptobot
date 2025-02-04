import os
import streamlit as st
from cryptobot.src.bot.chat import CryptoChat

def initialize_chat():
    if "chat_bot" not in st.session_state:
        st.session_state.chat_bot = CryptoChat()
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("Crypto助手")
    st.write("欢迎使用 Crypto 助手！我是您的加密货币和链上交易专家。")
    
    initialize_chat()
    
    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("请输入您的问题"):
        # 显示用户问题
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 显示助手回答
        with st.chat_message("assistant"):
            response = st.session_state.chat_bot.chat(prompt)
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 
