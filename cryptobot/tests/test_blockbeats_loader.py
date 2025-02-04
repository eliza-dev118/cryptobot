from cryptobot.src.kb.url_loader import URLLoader
from cryptobot.src.kb.knowledge_base import KnowledgeBase

def test_url_loading():
    print("\n=== 测试URL加载器 ===")
    
    url_loader = URLLoader()
    kb = KnowledgeBase()
    
    # 测试URL列表
    test_urls = [
        "https://www.theblockbeats.info/news/55196",
        "https://www.theblockbeats.info/news/56739",
    ]
    
    for test_url in test_urls:
        print(f"\n尝试加载URL: {test_url}")
        try:
            content = url_loader.load_url(test_url)
            
            if content:
                print(f"成功提取内容，长度: {len(content)} 字符")
                print("\n内容预览:")
                print(content[:500] + "...\n")
                
                # 添加到知识库
                print("添加到知识库...")
                kb.add_texts([content])
                
                # 测试查询
                test_queries = [
                    "0xSun的故事是什么",
                    "0xSun在什么案例里挣了大钱"
                    "文章中提到了哪些具体案例？",
                    "作者的主要观点是什么？"
                ]
                
                print("\n测试查询:")
                for query in test_queries:
                    print(f"\n问题: {query}")
                    results = kb.search(query, k=2)
                    for i, result in enumerate(results, 1):
                        print(f"\n结果 {i}:")
                        print(f"相关度: {result['score']:.4f}")
                        print(f"内容: {result['content']}")
            else:
                print(f"无法从URL提取内容: {test_url}")
                
        except Exception as e:
            print(f"处理URL时出错: {test_url}")
            print(f"错误信息: {str(e)}")
            continue

if __name__ == "__main__":
    test_url_loading() 