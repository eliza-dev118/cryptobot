import sys
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from cryptobot.src.kb.knowledge_base import KnowledgeBase

def test_vitalik_knowledge():
    print("\n=== 测试 Vitalik 相关知识 ===")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    kb = KnowledgeBase()
    
    # 添加测试文档
    test_content = """
    Vitalik Buterin对区块链的主要观点：
    
    1. 扩容解决方案：
    - Layer 2是以太坊扩容的关键
    - ZK-Rollups将在未来发挥重要作用
    - 分片技术仍然是长期规划的一部分
    
    2. 隐私保护：
    - 区块链需要更好的隐私保护机制
    - 零知识证明技术是关键
    
    3. 去中心化：
    - 保持足够的去中心化程度很重要
    - 反对过度中心化的趋势
    
    4. 社会影响：
    - 区块链应该服务于社会价值
    - 反对纯投机行为
    """
    
    print("\n=== 添加文档到知识库 ===")
    kb.add_texts([test_content])
    
    # 测试不同类型的查询
    queries = [
        "Vitalik对区块链扩容的看法是什么？",
        "Vitalik如何看待隐私保护？",
        "以太坊的未来发展方向是什么？",
        "Vitalik对去中心化的观点是什么？"
    ]
    
    print("\n=== 开始测试查询 ===")
    for query in queries:
        print(f"\n查询问题: {query}")
        print("-" * 50)
        results = kb.search(query, k=2)
        
        if not results:
            print("没有找到相关结果")
            continue
            
        for i, result in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"相关度: {result['score']:.4f}")
            print(f"内容片段: {result['content'].strip()}")
            print("-" * 30)

if __name__ == "__main__":
    test_vitalik_knowledge()
