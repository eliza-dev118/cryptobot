from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import trafilatura
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

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