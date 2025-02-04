import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from cryptobot.src.kb.knowledge_base import KnowledgeBase
from dotenv import load_dotenv
from typing import List, Dict
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class CryptoChat:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
    def chat(self, query: str) -> str:
        try:
            # 增加搜索结果数量以获取更完整的上下文
            search_results = self.kb.search(query, k=5)
            
            if not search_results:
                return "抱歉，我的知识库中没有找到相关信息。请问其他问题。"
            
            # 构建更精确的 prompt
            context = "\n".join([r["content"][:1200] for r in search_results])
            prompt = f"""你是一个专业的加密货币交易助手。请基于背景信息回答问题。

核心规则：
1. 严格遵守原文定义，不得改写或简化
2. 对于GMGN的四种打法，必须使用PDF中的原始定义：
   - 内盘：在pumpfun内盘寻找标的投资
   - 外盘一段：内盘标的迁移到外盘后的PVP交易
   - 外盘二段：外盘一段PVP结束后，下跌50%甚至80%时的买入机会
   - 准上所资产：可能在CEX上市的资产
3. 如果发现之前的回答有误，要明确承认错误并纠正
4. 保持答案的一致性，避免自相矛盾
5. 不要编造或推测未提及的内容

背景信息：
{context}

用户问题：{query}"""
            
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo-16k",
                temperature=0.1
            )
            response = self.llm.invoke(prompt).content
            return response
            
        except Exception as e:
            print(f"处理问题时出错: {str(e)}")
            return "抱歉，处理您的问题时出现了错误。请稍后再试。"

def main():
    chat = CryptoChat()
    print("欢迎使用 Crypto 助手！我是您的加密货币和链上交易专家。")
    print("您可以询问我关于：")
    print("- MEME 币市场分析")
    print("- 链上交易工具和策略")
    print("- 成功案例分析")
    print("- 风险管理建议")
    print("\n输入 'q' 退出。")
    
    while True:
        query = input("\n请输入您的问题：")
        if query.lower() == 'q':
            break
            
        response = chat.chat(query)
        print(f"\n助手：{response}")

if __name__ == "__main__":
    main() 