from cryptobot.src.kb.loaders.pdf_loader import PDFLoader
from cryptobot.src.chat import CryptoChat

def test_pdf_loading():
    print("\n=== 测试 PDF 加载器 ===")
    
    # 先创建一个 chat 实例
    chat = CryptoChat()
    
    # 使用同一个知识库实例
    loader = PDFLoader()
    
    # 测试目录
    pdf_dir = "cryptobot/data/pdfs"
    
    # 加载PDF
    success_count = loader.load_directory(pdf_dir)
    print(f"\n成功加载 {success_count} 个PDF文件")
    
    # 测试查询
    test_queries = [
        "这些PDF主要讲了什么内容？",
        "有哪些具体的交易案例？",
        "文章中提到了哪些风险？"
    ]
    
    print("\n=== 开始查询测试 ===")
    for query in test_queries:
        print(f"\n问题: {query}")
        response = chat.chat(query)
        print(f"回答: {response}")

if __name__ == "__main__":
    test_pdf_loading() 