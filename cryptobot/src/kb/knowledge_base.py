import os
from typing import List, Dict
from dotenv import load_dotenv
import sys
import sqlite3
try:
    import pysqlite3
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import warnings
import logging

# 加载环境变量
load_dotenv()

# 确保有API密钥
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("请在.env文件中设置OPENAI_API_KEY")

# 过滤 LangChain 废弃警告
warnings.filterwarnings('ignore', category=DeprecationWarning, module='langchain.*')

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

"""
KnowledgeBase 类设计说明：

当前职责：
1. 管理向量数据库（Chroma）
2. 提供添加和搜索文本的基础功能
3. 维护已存在URL的记录

待优化点：
1. 元数据管理可以更完善（添加时间戳、标题、作者等）
2. 可以添加版本控制机制
3. 可以添加数据清理和更新机制

未来重构方向：
1. 分离元数据管理到独立的类
2. 添加数据验证层
3. 实现更细粒度的CRUD操作
4. 添加批量操作的支持
"""


class KnowledgeBase:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            print("=== 创建新的 KnowledgeBase 实例 ===")
            cls._instance = super(KnowledgeBase, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.persist_dir = "cryptobot/data/knowledge_base"
        
        # 检查知识库是否已存在
        if os.path.exists(self.persist_dir) and os.listdir(self.persist_dir):
            logger.info("=== 加载已存在的知识库 ===")
        else:
            logger.info("=== 首次初始化知识库 ===")
            os.makedirs(self.persist_dir, exist_ok=True)
            
        # 初始化向量存储
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=OpenAIEmbeddings()
        )

    def search(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """搜索相关文本"""
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return [{"content": doc.page_content, "score": score} 
                   for doc, score in results]
        except Exception as e:
            print(f"搜索时出错: {str(e)}")
            return []
    
    def is_content_duplicate(self, content: str, threshold: float = 0.95) -> bool:
        """检查内容是否重复（基于向量相似度）
        
        Args:
            content: 要检查的内容
            threshold: 相似度阈值，默认0.95，大于等于此值视为重复
        
        Returns:
            bool: True 表示内容重复，False 表示内容不重复
        """
        try:
            # 1. 如果知识库为空，直接返回 False
            collection = self.vectorstore.get()
            if len(collection['ids']) == 0:
                return False
            
            # 2. 搜索最相似的内容
            results = self.vectorstore.similarity_search_with_score(content, k=1)
            
            # 3. 如果找到结果，检查相似度
            if results:
                doc, score = results[0]
                similarity = 1 - score  # 转换距离为相似度
                logger.info(f"内容相似度: {similarity:.4f}")  # 显示更精确的相似度
                
                # 4. 判断是否重复
                is_duplicate = similarity >= threshold  # 修改为大于等于
                if is_duplicate:
                    logger.info(f"内容重复 (相似度 {similarity:.4f} >= 阈值 {threshold})")
                else:
                    logger.info(f"内容不重复 (相似度 {similarity:.4f} < 阈值 {threshold})")
                
                return is_duplicate
            
            return False
            
        except Exception as e:
            logger.error(f"检查内容重复时出错: {str(e)}")
            logger.error(f"错误类型: {type(e)}")
            return False

    def add_texts(self, texts: List[str], metadatas: List[dict] = None):
        """添加文本到知识库（带内容去重）"""
        try:
            # 过滤重复内容
            new_texts = []
            new_metadatas = []
            for i, text in enumerate(texts):
                if not self.is_content_duplicate(text):
                    new_texts.append(text)
                    if metadatas:
                        new_metadatas.append(metadatas[i])
                    logger.info(f"添加新内容: {text[:100]}...")
                else:
                    logger.info(f"跳过重复内容: {metadatas[i]['source'] if metadatas else '未知来源'}")
            
            if new_texts:
                self.vectorstore.add_texts(new_texts, metadatas=new_metadatas)
                self.vectorstore.persist()
                logger.info(f"成功添加 {len(new_texts)} 条新内容到知识库")
            else:
                logger.info("没有新的内容需要添加")
            
        except Exception as e:
            logger.error(f"添加文本时出错: {str(e)}")
            raise

    def clear(self) -> None:
        """清空知识库"""
        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=OpenAIEmbeddings()
            )
            logger.info("知识库已清空")
        except Exception as e:
            logger.error(f"清空知识库时出错: {str(e)}")

    def get_existing_urls(self) -> set:
        """获取知识库中已存在的URL"""
        try:
            # 直接从 Chroma 获取所有数据
            results = self.vectorstore.get()
            
            # 调试日志
            logger.info(f"从数据库获取到 {len(results['ids'])} 条记录")
            logger.info(f"元数据列表: {results['metadatas']}")
            
            # 提取所有URL
            urls = set()
            for metadata in results['metadatas']:
                if metadata and 'source' in metadata:
                    source = metadata['source']
                    if source.startswith('http'):
                        urls.add(source)
            
            logger.info(f"从知识库中找到 {len(urls)} 个已存在的URL")
            for url in urls:
                logger.info(f"- {url}")
            
            return urls
            
        except Exception as e:
            logger.error(f"获取已存在URL时出错: {str(e)}")
            logger.error(f"错误详情: {str(e.__class__.__name__)}")
            return set()

    def get_existing_pdfs(self) -> set:
        """获取知识库中已存在的PDF文件名"""
        try:
            # 直接从 Chroma 获取所有数据
            results = self.vectorstore.get()
            
            # 调试日志
            logger.info(f"从数据库获取到 {len(results['ids'])} 条记录")
            logger.info(f"元数据列表: {results['metadatas']}")
            
            # 提取所有PDF
            pdfs = set()
            for metadata in results['metadatas']:
                if metadata and 'source' in metadata and metadata.get('type') == 'pdf':
                    pdfs.add(metadata['source'])
            
            logger.info(f"从知识库中找到 {len(pdfs)} 个已存在的PDF")
            for pdf in pdfs:
                logger.info(f"- {pdf}")
            
            return pdfs
            
        except Exception as e:
            logger.error(f"获取已存在PDF时出错: {str(e)}")
            logger.error(f"错误详情: {str(e.__class__.__name__)}")
            return set()
