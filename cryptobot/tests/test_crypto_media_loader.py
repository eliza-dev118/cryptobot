from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptobot.src.kb.knowledge_base import KnowledgeBase
import trafilatura
import time

def test_crypto_media_loading():
    print("\n=== 测试加密媒体整合加载器 ===")
    
    kb = KnowledgeBase()
    
    # 测试URL列表
    test_urls = [
        "https://www.odaily.news/post/5198722",
        "https://foresightnews.pro/article/detail/77220",
        "https://www.theblockbeats.info/news/56667"
    ]
    
    # 初始化Chrome浏览器（仅用于需要的网站）
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    try:
        for test_url in test_urls:
            print(f"\n尝试加载URL: {test_url}")
            try:
                content = None
                
                # BlockBeats 使用 trafilatura
                if "theblockbeats.info" in test_url:
                    downloaded = trafilatura.fetch_url(test_url)
                    if downloaded:
                        content = trafilatura.extract(downloaded, include_comments=False, 
                                                    include_tables=False, 
                                                    no_fallback=True)
                    
                # 其他网站使用 Selenium
                else:
                    driver.get(test_url)
                    wait = WebDriverWait(driver, 10)
                    
                    if "odaily.news" in test_url:
                        article = wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, "_3739r7Mk"))
                        )
                    elif "foresightnews.pro" in test_url:
                        article = wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, "ql-editor"))
                        )
                    
                    # 获取所有段落和标题
                    paragraphs = article.find_elements(By.TAG_NAME, "p")
                    headings = article.find_elements(By.TAG_NAME, "h2")
                    
                    # 组合内容
                    content_elements = []
                    for element in paragraphs + headings:
                        text = element.text.strip()
                        if text:  # 只添加非空内容
                            content_elements.append(text)
                    
                    content = "\n".join(content_elements)
                
                if content:
                    print(f"成功提取内容，长度: {len(content)} 字符")
                    print("\n内容预览:")
                    print(content[:500] + "...\n")
                    
                    # 添加到知识库
                    print("添加到知识库...")
                    kb.add_texts([content])
                else:
                    print(f"无法从URL提取内容: {test_url}")
                    
            except Exception as e:
                print(f"处理URL时出错: {test_url}")
                print(f"错误信息: {str(e)}")
                continue
                
            # 等待一下，避免请求太频繁
            time.sleep(2)
        
        # 所有文章加载完成后进行测试查询
        test_queries = [
            "0xSun和CryptoD分别是谁？他们有什么成就？",
            "他们在TRUMP上的交易经历是什么？",
            "文章中提到了哪些链上监控工具？每个工具的特点是什么？",
            "对于新手来说，应该如何开始链上交易？",
            "Moonshot在TRUMP交易中起到了什么作用？"
        ]
        
        print("\n=== 开始综合查询测试 ===")
        for query in test_queries:
            print(f"\n问题: {query}")
            results = kb.search(query, k=2)  # 获取top 2相关结果
            for i, result in enumerate(results, 1):
                print(f"\n结果 {i}:")
                print(f"相关度: {result['score']:.4f}")
                print(f"内容: {result['content'][:800] + '...' if len(result['content']) > 800 else result['content']}")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    test_crypto_media_loading() 