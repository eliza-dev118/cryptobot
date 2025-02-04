import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

print(f"Python 路径: {sys.path}")
print(f"当前工作目录: {os.getcwd()}")

import streamlit as st
from cryptobot.src.bot.chat import CryptoChat

def initialize_chat():
    if "chat_bot" not in st.session_state:
        st.session_state.chat_bot = CryptoChat()
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.set_page_config(
        page_title="Crypto助手",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 Crypto助手")
    st.markdown("""
    欢迎使用 Crypto 助手！我是您的加密货币和链上交易专家。
    
    您可以询问我关于：
    - MEME 币市场分析
    - 链上交易工具和策略
    - 成功案例分析
    - 风险管理建议
    """)

    initialize_chat()

    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 聊天输入
    if prompt := st.chat_input("请输入您的问题"):
        # 显示用户问题
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 显示助手回答
        with st.chat_message("assistant"):
            response = st.session_state.chat_bot.chat(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 