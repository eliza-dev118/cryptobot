import logging
from cryptobot.src.kb.knowledge_manager import KnowledgeManager
from cryptobot.src.kb.clear_kb import clear_knowledge_base

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_content_deduplication():
    """测试内容去重功能"""
    # 1. 清空知识库
    # clear_knowledge_base()
    manager = KnowledgeManager()
    
    logger.info("\n=== 测试内容去重 ===")
    
    # 2. 测试完全相同的内容
    content1 = """
    比特币（Bitcoin）是一种基于去中心化、采用点对点网络与共识主动性，
    开放源代码，以区块链作为底层技术的加密货币。
    """
    
    logger.info("\n添加第一段内容:")
    manager.load_all(urls=[], texts=[content1])
    
    # 3. 测试完全相同的内容
    logger.info("\n测试完全相同内容:")
    duplicate = content1
    manager.load_all(urls=[], texts=[duplicate])
    
    # 4. 测试非常相似的内容（只改了几个字）
    logger.info("\n测试相似内容:")
    similar = """
    比特币（Bitcoin）是一种基于去中心化技术、采用点对点网络与共识主动性，
    开放源代码，以区块链作为底层技术的数字货币。
    """
    manager.load_all(urls=[], texts=[similar])
    
    # 5. 测试完全不同的内容
    logger.info("\n测试不同内容:")
    different = """
    以太坊（Ethereum）是一个开源的有智能合约功能的公共区块链平台，
    通过其专用加密货币以太币提供去中心化的以太虚拟机来处理点对点合约。
    """
    manager.load_all(urls=[], texts=[different])

if __name__ == "__main__":
    test_content_deduplication() 