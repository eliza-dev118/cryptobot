from PyPDF2 import PdfReader
import logging
import os
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PDFLoader:
    def __init__(self):
        pass
    
    def load_pdf(self, pdf_path: str) -> tuple:
        """加载PDF文件内容和元数据"""
        try:
            logger.info(f"\n正在处理PDF: {pdf_path}")
            reader = PdfReader(pdf_path)
            
            # 提取所有页面的文本
            pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text.strip():  # 确保页面内容不为空
                    pages.append(text.strip())
            
            # 使用分隔符连接所有页面
            content = "\n\n页面分隔符\n\n".join(pages)
            
            # 准备元数据
            metadata = {
                "source": os.path.basename(pdf_path),
                "type": "pdf",
                "pages": len(pages),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"成功提取 {len(pages)} 页内容")
            return content, metadata
            
        except Exception as e:
            logger.error(f"处理PDF时出错: {str(e)}")
            return None, None
    
    def load_directory(self, directory: str) -> int:
        """加载目录下的所有PDF文件"""
        success_count = 0
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    if self.load_pdf(pdf_path):
                        success_count += 1
        
        return success_count