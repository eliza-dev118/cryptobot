from cryptobot.src.kb.knowledge_base import KnowledgeBase
import shutil
import os
import logging
import time
import gc

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def clear_knowledge_base():
    """完全清空知识库"""
    try:
        # 1. 先获取数据库路径
        kb = KnowledgeBase()
        chroma_dir = kb.persist_dir
        logger.info(f"\n=== 开始清空知识库 ===")
        logger.info(f"知识库路径: {chroma_dir}")
        
        # 2. 清理连接
        kb.vectorstore = None
        del kb
        gc.collect()  # 强制垃圾回收
        time.sleep(2)  # 给系统时间清理
        
        # 3. 删除数据库目录
        if os.path.exists(chroma_dir):
            shutil.rmtree(chroma_dir)
            logger.info(f"已删除知识库目录")
            time.sleep(1)  # 确保文件系统操作完成
        else:
            logger.info(f"知识库目录不存在")
        
        # 4. 创建新的空知识库
        logger.info("\n=== 初始化新知识库 ===")
        kb = KnowledgeBase()
        
        # 5. 验证是否为空
        results = kb.vectorstore.get()
        count = len(results['ids'])
        if count == 0:
            logger.info("验证成功：知识库为空")
        else:
            logger.error(f"警告：知识库仍包含 {count} 条记录")
            
    except Exception as e:
        logger.error(f"清空知识库时出错: {str(e)}")
        logger.error(f"错误类型: {type(e)}")
        logger.error(f"错误详情: {str(e)}")

if __name__ == "__main__":
    clear_knowledge_base() 