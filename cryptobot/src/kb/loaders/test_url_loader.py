import logging
from cryptobot.src.kb.loaders.url_loader import URLLoader
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_url_loader():
    """测试URL加载器的基本功能"""
    # 1. 初始化加载器
    loader = URLLoader()
    
    # 2. 测试不同网站的URL
    test_urls = [
        "https://www.theblockbeats.info/news/56667",
        "https://www.odaily.news/post/5198722",
        "https://foresightnews.pro/article/detail/77220"
    ]
    
    logger.info(f"\n=== 测试URL加载器 ===")
    
    for url in test_urls:
        logger.info(f"\n测试URL: {url}")
        try:
            content = loader.load_url(url)
            if content:
                logger.info(f"成功加载URL")
                logger.info(f"内容长度: {len(content)}")
                logger.info("\n内容预览:")
                logger.info(f"{content[:500]}...")
                logger.info("\n" + "="*50 + "\n")  # 分隔线
            else:
                logger.error("URL加载失败：返回内容为空")
                
        except Exception as e:
            logger.error(f"URL加载出错: {str(e)}")
            logger.error(f"错误类型: {type(e)}")
            logger.error("\n" + "="*50 + "\n")  # 分隔线

if __name__ == "__main__":
    test_url_loader() 