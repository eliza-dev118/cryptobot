import logging
from cryptobot.src.kb.knowledge_manager import KnowledgeManager
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_knowledge_manager():
    """测试知识管理器"""
    # 1. 初始化管理器
    manager = KnowledgeManager()
    
    # 2. 准备测试数据
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_pdf_dir = os.path.join(current_dir, "loaders", "test_data")
    
    test_urls = [
        "https://www.theblockbeats.info/news/56667",
        "https://www.odaily.news/post/5198722",
        "https://foresightnews.pro/article/detail/77220"
    ]
    
    logger.info("\n=== 测试知识管理器 ===")
    
    try:
        # 3. 测试加载
        results = manager.load_all(pdf_dir=test_pdf_dir, urls=test_urls)
        
        logger.info("\n=== 加载结果 ===")
        logger.info(f"成功加载 PDF: {results['pdfs_loaded']} 个")
        logger.info(f"成功加载 URL: {results['urls_loaded']} 个")
        
        # 4. 测试重复加载
        logger.info("\n=== 测试重复加载 ===")
        results = manager.load_all(pdf_dir=test_pdf_dir, urls=test_urls)
        logger.info(f"重复加载 PDF: {results['pdfs_loaded']} 个")
        logger.info(f"重复加载 URL: {results['urls_loaded']} 个")
        
    except Exception as e:
        logger.error(f"测试出错: {str(e)}")
        logger.error(f"错误类型: {type(e)}")

if __name__ == "__main__":
    test_knowledge_manager() 