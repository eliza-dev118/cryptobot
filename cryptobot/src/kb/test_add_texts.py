import logging
from cryptobot.src.kb.knowledge_manager import KnowledgeManager
from cryptobot.src.kb.clear_kb import clear_knowledge_base

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_add_texts():
    """测试添加文本功能"""
    # 1. 清空知识库
    # clear_knowledge_base()
    manager = KnowledgeManager()  # 使用 KnowledgeManager 而不是直接使用 KnowledgeBase
    
    logger.info("\n=== 测试添加文本 ===")
    
    # 2. 添加一段文本
    content1 = "这是第一段测试内容"
    
    try:
        logger.info("\n添加第一段内容:")
        # 使用 manager 的 load_all 方法
        result = manager.load_all(texts=[content1])
        logger.info(f"添加结果: {result}")
        
    except Exception as e:
        logger.error(f"测试出错: {str(e)}")
        logger.error(f"错误类型: {type(e)}")

if __name__ == "__main__":
    test_add_texts() 