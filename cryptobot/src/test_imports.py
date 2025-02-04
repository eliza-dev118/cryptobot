def test_imports():
    print("开始测试导入...")
    
    try:
        import chromadb
        print(f"成功导入 chromadb，版本：{chromadb.__version__}")
    except ImportError as e:
        print(f"chromadb 导入失败：{str(e)}")
    
    try:
        from langchain_community.vectorstores import Chroma
        print("成功导入 Chroma")
    except ImportError as e:
        print(f"Chroma 导入失败：{str(e)}")
    
    try:
        from cryptobot.src.kb.knowledge_base import KnowledgeBase
        print("成功导入 KnowledgeBase")
        kb = KnowledgeBase()
        print("成功创建 KnowledgeBase 实例")
    except Exception as e:
        print(f"KnowledgeBase 相关错误：{str(e)}")

if __name__ == "__main__":
    test_imports() 