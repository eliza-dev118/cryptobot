import os
from cryptobot.src.kb.knowledge_base import KnowledgeBase

def test_kb():
    print("=== 开始测试知识库 ===")
    print(f"当前工作目录: {os.getcwd()}")
    
    try:
        kb = KnowledgeBase()
        print("知识库初始化成功")
        
        # 测试搜索功能
        results = kb.search("测试查询", k=1)
        print(f"搜索结果: {results}")
        
        print("=== 测试完成 ===")
    except Exception as e:
        print(f"发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    test_kb() 