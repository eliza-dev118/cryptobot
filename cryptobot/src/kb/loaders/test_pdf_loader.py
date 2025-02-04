import logging
from cryptobot.src.kb.loaders.pdf_loader import PDFLoader
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_pdf_loader():
    """测试PDF加载器的基本功能"""
    # 1. 初始化加载器
    loader = PDFLoader()
    
    # 2. 选择一个小的测试PDF文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_pdf = os.path.join(current_dir, "test_data", "test.pdf")
    
    if not os.path.exists(test_pdf):
        logger.error(f"测试文件不存在: {test_pdf}")
        return
        
    # 3. 测试加载功能
    logger.info(f"\n=== 测试PDF加载 ===")
    logger.info(f"测试文件: {test_pdf}")
    
    try:
        # 加载内容和元数据
        content, metadata = loader.load_pdf(test_pdf)  # 修改返回值
        if content:
            logger.info(f"成功加载PDF")
            logger.info(f"内容长度: {len(content)}")
            logger.info("\n内容预览:")
            logger.info(f"{content[:500]}...")
            
            # 检查页面分隔
            pages = content.split('\n\n页面分隔符\n\n')
            logger.info(f"\n总页数: {len(pages)}")
            logger.info(f"第一页预览: {pages[0][:200]}...")
            
            # 检查元数据
            logger.info("\n元数据:")
            logger.info(metadata)
        else:
            logger.error("PDF加载失败：返回内容为空")
            
    except Exception as e:
        logger.error(f"PDF加载出错: {str(e)}")
        logger.error(f"错误类型: {type(e)}")

if __name__ == "__main__":
    test_pdf_loader() 