from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptobot.src.kb.knowledge_base import KnowledgeBase
import time

def test_odaily_loading():
    print("\n=== 测试 Odaily 加载器 ===")
    
    kb = KnowledgeBase()
    
    # 测试URL列表
    test_urls = [
        "https://www.odaily.news/post/5198722",
    ]
    
    # 初始化Chrome浏览器
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    try:
        for test_url in test_urls:
            print(f"\n尝试加载URL: {test_url}")
            try:
                # 加载页面
                driver.get(test_url)
                
                # 等待文章内容加载
                wait = WebDriverWait(driver, 10)
                article = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_3739r7Mk"))
                )
                
                # 获取所有段落和标题
                paragraphs = article.find_elements(By.TAG_NAME, "p")
                headings = article.find_elements(By.TAG_NAME, "h2")
                
                # 组合内容（包括段落和标题）
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
                    
                    # 测试查询
                    test_queries = [
                        "0xSun是谁？他的主要成就是什么？",
                        "0xSun如何看待当前的Meme市场？",
                        "0xSun给新手什么建议？",
                        "文章中提到了哪些具体的交易案例？"
                    ]
                    
                    print("\n测试查询:")
                    for query in test_queries:
                        print(f"\n问题: {query}")
                        results = kb.search(query, k=1)
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
                
            # 等待一下，避免请求太频繁
            time.sleep(2)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    test_odaily_loading() 