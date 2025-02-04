import logging
from cryptobot.src.kb.knowledge_base import KnowledgeBase

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_content_deduplication():
    """测试内容去重功能"""
    kb = KnowledgeBase()
    
    # 测试完全相同的内容
    content1 = "这是一个测试内容"
    metadata1 = {"source": "test1.txt", "type": "text"}
    kb.add_texts([content1], [metadata1])
    
    # 应该被识别为重复
    assert kb.is_content_duplicate(content1)
    
    # 测试非常相似的内容
    content2 = "这是一个测试内容。"  # 只多了一个句号
    assert kb.is_content_duplicate(content2)
    
    # 测试不同的内容
    content3 = "这是完全不同的内容"
    assert not kb.is_content_duplicate(content3)

if __name__ == "__main__":
    test_content_deduplication() 