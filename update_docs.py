import os

content = """# AI 智能知识库系统

## 1. 项目结构 

ai_kb/
├── data/
│   ├── knowledge_base/  # Chroma 向量数据库
│   └── pdfs/           # PDF 文件存储
├── src/
│   └── kb/
│       ├── loaders/    # 加载器
│       │   ├── pdf_loader.py
│       │   └── url_loader.py
│       ├── knowledge_base.py    # 核心知识库类
│       ├── knowledge_manager.py # 知识库管理器
│       └── clear_kb.py         # 清空知识库工具
└── docs/
    └── 项目文档.md      # 本文档

## 2. 核心功能

### 2.1 知识库管理
- 支持加载 PDF、URL 和纯文本
- 基于向量相似度的内容去重
- 支持内容搜索和相似度匹配

### 2.2 去重机制
- 使用 OpenAI Embeddings 生成文本向量
- 相似度阈值设置为 0.95
- 对所有类型内容（PDF、URL、纯文本）都有效

## 3. 关键代码

### 3.1 知识库核心 (knowledge_base.py)

class KnowledgeBase:
    def __init__(self):
        \"\"\"初始化知识库\"\"\"
        self.persist_dir = "ai_kb/data/knowledge_base"
        os.makedirs(self.persist_dir, exist_ok=True)
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=OpenAIEmbeddings()
        )
    
    def is_content_duplicate(self, content: str, threshold: float = 0.95) -> bool:
        \"\"\"检查内容是否重复\"\"\"
        try:
            collection = self.vectorstore.get()
            if len(collection['ids']) == 0:
                return False
            
            results = self.vectorstore.similarity_search_with_score(content, k=1)
            
            if results:
                doc, score = results[0]
                similarity = 1 - score
                logger.info(f"内容相似度: {similarity:.4f}")
                
                is_duplicate = similarity >= threshold
                if is_duplicate:
                    logger.info(f"内容重复 (相似度 {similarity:.4f} >= 阈值 {threshold})")
                else:
                    logger.info(f"内容不重复 (相似度 {similarity:.4f} < 阈值 {threshold})")
                
                return is_duplicate
            
            return False
            
        except Exception as e:
            logger.error(f"检查内容重复时出错: {str(e)}")
            return False

### 3.2 知识库管理器 (knowledge_manager.py)

class KnowledgeManager:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.pdf_loader = PDFLoader()
        self.url_loader = URLLoader()
    
    def load_all(self, pdf_dir: str = None, urls: List[str] = None, texts: List[str] = None) -> Dict[str, int]:
        \"\"\"加载所有资源\"\"\"
        results = {
            "pdfs_loaded": 0,
            "urls_loaded": 0,
            "texts_loaded": 0
        }
        
        if pdf_dir and os.path.exists(pdf_dir):
            results["pdfs_loaded"] = self.load_pdfs(pdf_dir)
                
        if urls:
            results["urls_loaded"] = self.load_urls(urls)
        
        if texts:
            results["texts_loaded"] = self.load_texts(texts)
        
        return results

## 4. 使用说明

### 4.1 清空知识库
重要：清空知识库时，建议使用独立命令而不是在代码中调用：

python -m ai_kb.src.kb.clear_kb

### 4.2 加载内容

from ai_kb.src.kb.knowledge_manager import KnowledgeManager

manager = KnowledgeManager()

# 加载 PDF
manager.load_all(pdf_dir="ai_kb/data/pdfs")

# 加载 URL
manager.load_all(urls=["https://example.com"])

# 加载纯文本
manager.load_all(texts=["这是一段测试文本"])

### 4.3 内容去重
- 系统自动对所有新添加的内容进行去重检查
- 相似度阈值为 0.95（可配置）
- 支持跨类型去重（PDF、URL、纯文本之间互相去重）

## 5. 注意事项

1. 数据库操作
   - 清空数据库时使用独立命令
   - 避免在代码中直接调用 clear_knowledge_base()

2. 去重功能
   - 对所有类型内容都有效
   - 即使文件名不同，内容相同也会被去重
   - 可以通过调整阈值控制去重严格程度

3. 错误处理
   - 系统包含完整的错误处理和日志记录
   - 加载失败不会影响其他内容的处理

## 6. 未来优化方向

1. 性能优化
   - 批量处理大量文档
   - 并行处理多个来源

2. 功能扩展
   - 支持更多文档类型
   - 自定义去重规则
   - 内容更新机制

3. 监控和管理
   - 添加管理界面
   - 统计和分析功能
"""

# 确保目录存在
os.makedirs("cryptobot/docs", exist_ok=True)

# 写入文档
with open("cryptobot/docs/项目文档.md", "w", encoding="utf-8") as f:
    f.write(content)
