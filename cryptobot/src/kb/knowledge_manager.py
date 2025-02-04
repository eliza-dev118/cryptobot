from cryptobot.src.kb.knowledge_base import KnowledgeBase
from cryptobot.src.kb.loaders.pdf_loader import PDFLoader
from cryptobot.src.kb.loaders.url_loader import URLLoader
from typing import List, Dict
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import trafilatura
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

"""
KnowledgeLoader 类设计说明：

当前职责：
1. 抓取不同来源的网页内容（BlockBeats、Odaily等）
2. 处理和清洗文本数据
3. 调用 KnowledgeBase 存储数据

待优化点：
1. 网页抓取逻辑应该分离到专门的 Scraper 类
2. 需要更好的错误处理机制
3. 需要更完善的数据验证

未来重构方向：
1. 创建专门的 WebScraper 类处理网页抓取
2. 创建数据处理管道（Pipeline）标准化数据处理流程
3. 添加重试机制和并发支持
4. 改进日志记录系统

重构后的理想结构：
Scraper（抓取） -> Loader（处理） -> KnowledgeBase（存储）
"""

class KnowledgeManager:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.pdf_loader = PDFLoader()
        self.url_loader = URLLoader()
    
    def load_pdfs(self, pdf_dir: str) -> int:
        """加载目录下的所有PDF文件，跳过已存在的"""
        logger.info(f"\n=== 开始加载PDF文件 ===")
        
        # 获取已存在的PDF文件记录
        existing_pdfs = self.kb.get_existing_pdfs()
        logger.info(f"已存在 {len(existing_pdfs)} 个PDF文件")
        
        # 获取目录下所有PDF文件
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        
        # 筛选新文件
        new_pdfs = [f for f in pdf_files if f not in existing_pdfs]
        skipped_pdfs = [f for f in pdf_files if f in existing_pdfs]
        
        if skipped_pdfs:
            logger.info("\n跳过已存在的PDF文件:")
            for pdf in skipped_pdfs:
                logger.info(f"- {pdf}")
        
        if not new_pdfs:
            logger.info("\n没有新的PDF文件需要加载")
            return 0
        
        # 加载新文件
        logger.info(f"\n开始加载 {len(new_pdfs)} 个新PDF文件:")
        success_count = 0
        for pdf_file in new_pdfs:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            content, metadata = self.pdf_loader.load_pdf(pdf_path)
            if content and metadata:
                self.kb.add_texts([content], [metadata])
                success_count += 1
                logger.info(f"成功加载: {pdf_file}")
        
        return success_count
    
    def load_urls(self, urls: List[str]) -> int:
        """加载URL列表，跳过已存在的"""
        logger.info("\n=== 开始加载URL ===")
        
        # 获取已存在的URL
        existing_urls = self.kb.get_existing_urls()
        logger.info(f"已存在 {len(existing_urls)} 个URL")
        
        # 筛选新URL
        new_urls = [url for url in urls if url not in existing_urls]
        skipped_urls = [url for url in urls if url in existing_urls]
        
        if skipped_urls:
            logger.info("\n跳过已存在的URL:")
            for url in skipped_urls:
                logger.info(f"- {url}")
        
        if not new_urls:
            logger.info("\n没有新的URL需要加载")
            return 0
        
        # 加载新URL
        logger.info(f"\n开始加载 {len(new_urls)} 个新URL:")
        success_count = 0
        for url in new_urls:
            content = self.url_loader.load_url(url)
            if content:
                try:
                    self.kb.add_texts([content], [{"source": url, "type": "url"}])
                    success_count += 1
                    logger.info(f"成功加载: {url}")
                except Exception as e:
                    logger.error(f"添加URL内容时出错 {url}: {str(e)}")
        
        return success_count
    
    def load_texts(self, texts: List[str]) -> int:
        """加载纯文本列表，返回成功加载的数量"""
        logger.info("\n=== 开始加载纯文本 ===")
        
        success_count = 0
        for i, text in enumerate(texts):
            try:
                logger.info(f"\n处理第 {i+1} 个文本:")
                logger.info(f"文本长度: {len(text)} 字符")
                logger.info(f"文本预览: {text[:100]}...")
                
                metadata = {"source": f"text_{i+1}", "type": "text"}
                self.kb.add_texts([text], [metadata])
                success_count += 1
                logger.info("成功添加文本")
                
            except Exception as e:
                logger.error(f"添加文本时出错: {str(e)}")
        
        return success_count
    
    def load_all(self, pdf_dir: str = None, urls: List[str] = None, texts: List[str] = None) -> Dict[str, int]:
        """加载所有资源"""
        results = {
            "pdfs_loaded": 0,
            "urls_loaded": 0,
            "texts_loaded": 0
        }
        
        if pdf_dir and os.path.exists(pdf_dir):
            results["pdfs_loaded"] = self.load_pdfs(pdf_dir)
            
        if urls:
            results["urls_loaded"] = self.load_urls(urls)
        
        if texts:
            results["texts_loaded"] = self.load_texts(texts)
        
        return results

class URLLoader:
    def __init__(self):
        # 初始化 Selenium
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = None

    def load_url(self, url: str) -> str:
        content = None
        try:
            logger.info(f"\n=== 开始加载URL: {url} ===")
            
            # BlockBeats 使用 trafilatura
            if "theblockbeats.info" in url:
                logger.info("使用 trafilatura 加载 BlockBeats")
                downloaded = trafilatura.fetch_url(url)
                if downloaded:
                    content = trafilatura.extract(downloaded, 
                                               include_comments=False,
                                               include_tables=False,
                                               no_fallback=True)
                
            # 其他网站使用 Selenium
            else:
                if not self.driver:
                    self.driver = webdriver.Chrome(options=self.options)
                
                self.driver.get(url)
                wait = WebDriverWait(self.driver, 10)
                
                if "odaily.news" in url:
                    logger.info("使用 Selenium 加载 Odaily")
                    article = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "_3739r7Mk"))
                    )
                elif "foresightnews.pro" in url:
                    logger.info("使用 Selenium 加载 Foresight")
                    article = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ql-editor"))
                    )
                else:
                    logger.error(f"不支持的网站: {url}")
                    return None
                
                # 获取内容
                paragraphs = article.find_elements(By.TAG_NAME, "p")
                headings = article.find_elements(By.TAG_NAME, "h2")
                content_elements = []
                for element in paragraphs + headings:
                    text = element.text.strip()
                    if text:
                        content_elements.append(text)
                content = "\n".join(content_elements)
            
            if content:
                logger.info(f"成功获取内容，长度: {len(content)} 字符")
                logger.info("内容预览:")
                logger.info(f"{content[:200]}...\n")
            else:
                logger.error("未能获取内容")
            
            time.sleep(2)  # 避免请求过于频繁
            
        except Exception as e:
            logger.error(f"加载URL时出错: {str(e)}")
            return None
            
        return content

    def __del__(self):
        if self.driver:
            self.driver.quit()

def main():
    manager = KnowledgeManager()
    
    # 配置资源
    pdf_dir = os.path.join(os.path.dirname(__file__), "../../../cryptobot/data/pdfs")
    print(f"\n=== PDF目录路径: {os.path.abspath(pdf_dir)} ===")
    print(f"PDF文件列表: {os.listdir(pdf_dir)}")
    
    urls = [
        "https://www.theblockbeats.info/news/56667",
        "https://www.odaily.news/post/5198722",
        "https://foresightnews.pro/article/detail/77220"
    ]
    
    # 测试纯文本加载
    texts = [
        "MEME币（模因币）是一类基于社交媒体热点、网络文化或者梗而创建的加密货币。它们通常具有较强的社区属性和病毒式传播特征，但也往往伴随着高风险。",
        "PEPE是2023年最成功的MEME币之一，它基于'青蛙Pepe'这个互联网表情包，在没有预售、预挖的情况下，依靠社区力量实现了病毒式传播。这开创了'公平发射'的新模式。"
    ]
    
    # 测试 load_all
    logger.info("\n=== 测试 load_all 函数 ===")
    results = manager.load_all(pdf_dir=pdf_dir, urls=urls, texts=texts)
    
    logger.info("\n=== 加载结果 ===")
    logger.info(f"成功加载 {results['pdfs_loaded']} 个PDF文件")
    logger.info(f"成功加载 {results['urls_loaded']} 个URL")
    logger.info(f"成功加载 {results['texts_loaded']} 个纯文本")
    
    # 测试搜索
    kb = KnowledgeBase()
    test_queries = [
        "什么是内盘和外盘？",
        "GMGN 链上打法有哪些？",
        "外盘⼀段是什么",
        "外盘二段是什么",
        "CryptoD的故事是什么？",
        "0xSun是谁？"

    ]
    
    logger.info("\n=== 测试搜索 ===")
    for query in test_queries:
        logger.info(f"\n查询: {query}")
        results = kb.search(query, k=2)
        for i, result in enumerate(results, 1):
            logger.info(f"\n结果 {i}:")
            logger.info(f"相关度: {result['score']}")
            logger.info(f"内容: {result['content'][:200]}...")

if __name__ == "__main__":
    main() 