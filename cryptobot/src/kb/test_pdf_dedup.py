import logging
import os
import shutil
from cryptobot.src.kb.knowledge_manager import KnowledgeManager
from cryptobot.src.kb.clear_kb import clear_knowledge_base

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_pdf_deduplication():
    """测试 PDF 去重功能"""
    # 1. 清空知识库
    # clear_knowledge_base()
    manager = KnowledgeManager()
    
    # 2. 准备测试 PDF 目录
    pdf_dir = "cryptobot/data/pdfs"
    os.makedirs(pdf_dir, exist_ok=True)
    
    # 3. 复制同一个 PDF 文件，但用不同的名字
    original_pdf = "cryptobot/data/pdfs/test.pdf"
    duplicate_pdf = "cryptobot/data/pdfs/test2.pdf"
    shutil.copy2(original_pdf, duplicate_pdf)
    
    logger.info("\n=== 测试 PDF 去重 ===")
    
    # 4. 加载所有 PDF
    results = manager.load_all(pdf_dir=pdf_dir)
    logger.info(f"\n加载结果: {results}")
    
    # 5. 清理测试文件
    os.remove(duplicate_pdf)

if __name__ == "__main__":
    test_pdf_deduplication() 