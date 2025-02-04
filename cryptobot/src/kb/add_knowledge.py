import argparse
import yaml
import logging
from cryptobot.src.kb.knowledge_manager import KnowledgeManager
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path: str = None) -> dict:
    """加载配置文件"""
    default_config = {
        "pdf_dir": "cryptobot/data/pdfs",
        "urls": [
            "https://www.theblockbeats.info/news/56667",
            "https://www.odaily.news/post/5198722",
            "https://foresightnews.pro/article/detail/77220"
        ]
    }
    
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logger.info(f"从 {config_path} 加载配置")
            return config
    
    logger.info("使用默认配置")
    return default_config

def main():
    parser = argparse.ArgumentParser(description='加载知识到知识库')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--pdf-dir', type=str, help='PDF文件目录')
    parser.add_argument('--urls', nargs='+', help='URL列表')
    parser.add_argument('--clear', action='store_true', help='是否先清空知识库')
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 命令行参数优先级高于配置文件
    pdf_dir = args.pdf_dir or config.get('pdf_dir')
    urls = args.urls or config.get('urls', [])
    
    # 显示将要处理的内容
    logger.info("\n=== 知识库加载任务 ===")
    if pdf_dir:
        logger.info(f"PDF目录: {pdf_dir}")
        if os.path.exists(pdf_dir):
            pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            logger.info(f"发现 {len(pdfs)} 个PDF文件:")
            for pdf in pdfs:
                logger.info(f"- {pdf}")
        else:
            logger.warning(f"PDF目录不存在: {pdf_dir}")
    
    if urls:
        logger.info(f"\n待加载URL: {len(urls)} 个")
        for url in urls:
            logger.info(f"- {url}")
    
    # 确认是否继续
    if not args.config:  # 只有在没有使用配置文件时才询问
        confirm = input("\n是否继续? [y/N] ")
        if confirm.lower() != 'y':
            logger.info("已取消")
            return
    
    # 执行加载
    try:
        manager = KnowledgeManager()
        if args.clear:
            from cryptobot.src.kb.clear_kb import clear_knowledge_base
            clear_knowledge_base()
            logger.info("已清空知识库")
        
        results = manager.load_all(pdf_dir=pdf_dir, urls=urls)
        
        # 显示结果
        logger.info("\n=== 加载完成 ===")
        logger.info(f"成功加载 {results['pdfs_loaded']} 个PDF文件")
        logger.info(f"成功加载 {results['urls_loaded']} 个URL")
        
    except Exception as e:
        logger.error(f"加载过程出错: {str(e)}")
        logger.error(f"错误类型: {type(e)}")

if __name__ == "__main__":
    main()