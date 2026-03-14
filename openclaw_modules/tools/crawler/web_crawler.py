"""
Web Crawler v2 - 工业级爬虫
增加功能：
1. 自动重试
2. 超时处理
3. Session 复用
4. 随机UA
5. 日志记录
6. 错误分类处理
7. 安全防护（Scraper Guard）
"""

import os
import sys

# 添加 security 模块路径（项目根目录的 security）
import pathlib
project_root = pathlib.Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / 'security'))

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import random
import time
import logging
from datetime import datetime
import urllib3

# 尝试导入安全守卫
try:
    from scraper_guard import ScraperGuard
    SCRAPER_GUARD = ScraperGuard()
    SECURITY_ENABLED = True
except ImportError:
    SECURITY_ENABLED = False
    SCRAPER_GUARD = None

# 禁用警告
urllib3.disable_warnings()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IndustrialCrawler:
    """工业级爬虫"""
    
    # 随机 User-Agent 池
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    ]
    
    def __init__(self, max_retries: int = 3, timeout: int = 10):
        """
        初始化
        
        Args:
            max_retries: 最大重试次数
            timeout: 超时时间(秒)
        """
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """创建带重试机制的 Session"""
        session = requests.Session()
        
        # 配置重试策略 - 指数退避
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,  # 重试间隔: 1s, 2s, 3s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        # 挂载适配器
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> dict:
        """获取随机请求头"""
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def crawl(self, url: str, max_paragraphs: int = 5) -> dict:
        """
        爬取网页
        """
        start_time = time.time()
        
        # ========== 安全检查 ==========
        if SECURITY_ENABLED and SCRAPER_GUARD:
            # 使用增强版安全守卫
            from scraper_guard import check_url
            url_safe, url_reason = check_url(url)
            if not url_safe:
                logger.warning(f"🚫 URL安全拦截: {url} - {url_reason}")
                return {"status": "error", "type": "security_blocked", "url": url, "error": url_reason}
        
        try:
            logger.info(f"🔄 正在请求: {url}")
            
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout,
                verify=False
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # ========== 响应安全检查 ==========
            if SECURITY_ENABLED and SCRAPER_GUARD:
                content_type = response.headers.get('Content-Type', 'text/html')
                
                # 2. 检查文件类型
                file_safe, file_reason = SCRAPER_GUARD.check_file_type(content_type, '')
                if not file_safe:
                    logger.warning(f"🚫 文件类型被拦截: {content_type} - {file_reason}")
                    return {"status": "error", "type": "security_blocked", "url": url, "error": f"不支持的文件类型: {content_type}"}
                
                # 3. 检查响应内容是否包含危险代码（简单检查）
                text_sample = response.text[:5000]
                if SCRAPER_GUARD:
                    code_safe, code_reason = SCRAPER_GUARD.check_code_execution(text_sample, url)
                    if not code_safe:
                        logger.warning(f"🚫 响应内容包含危险代码: {code_reason}")
                        # 只记录，不阻断（因为HTML本身可能包含script标签）
            
            title = self._extract_title(soup)
            paragraphs = self._extract_paragraphs(soup, max_paragraphs)
            links = self._extract_links(soup)
            description = self._extract_description(soup)
            
            elapsed = time.time() - start_time
            
            result = {
                "status": "success",
                "url": url,
                "title": title,
                "description": description,
                "paragraphs": paragraphs,
                "links": links,
                "fetched_at": datetime.now().isoformat(),
                "elapsed": f"{elapsed:.2f}s"
            }
            
            logger.info(f"✅ 成功: {url} ({elapsed:.2f}s)")
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ 超时: {url}")
            return {"status": "error", "type": "timeout", "url": url, "error": "连接超时"}
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ HTTP错误: {e.response.status_code}")
            return {"status": "error", "type": "http_error", "url": url, "error": f"HTTP {e.response.status_code}"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 请求异常: {e}")
            return {"status": "error", "type": "request_error", "url": url, "error": str(e)}
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        if soup.title:
            return soup.title.string.strip()
        h1 = soup.find('h1')
        return h1.get_text().strip() if h1 else ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """提取描述"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')
        return ""
    
    def _extract_paragraphs(self, soup: BeautifulSoup, max_count: int) -> list:
        """提取段落"""
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if len(text) > 20 and not text.startswith('['):
                paragraphs.append(text)
                if len(paragraphs) >= max_count:
                    break
        return paragraphs
    
    def _extract_links(self, soup: BeautifulSoup) -> list:
        """提取链接"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
                if len(links) >= 10:
                    break
        return links
    
    def crawl_multiple(self, urls: list, delay: float = 1.0) -> list:
        """
        批量爬取
        
        Args:
            urls: URL列表
            delay: 请求间隔(秒)
        """
        results = []
        for url in urls:
            result = self.crawl(url)
            results.append(result)
            time.sleep(delay)  # 礼貌延迟
        return results


# ===== 便捷函数 =====

def crawl(url: str, max_paragraphs: int = 5) -> dict:
    """简单接口"""
    crawler = IndustrialCrawler()
    return crawler.crawl(url, max_paragraphs)


# ===== 测试 =====

if __name__ == "__main__":
    print("="*50)
    print("Industrial Crawler v2 Test")
    print("="*50)
    
    test_urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://www.reddit.com/r/MachineLearning/",
    ]
    
    crawler = IndustrialCrawler(max_retries=2, timeout=5)
    
    for url in test_urls:
        print(f"\n🕷️ {url}")
        result = crawler.crawl(url, max_paragraphs=2)
        
        if result["status"] == "success":
            print(f"  ✅ {result.get('title', 'N/A')[:50]}")
            print(f"  📝 {len(result.get('paragraphs', []))} paragraphs")
            print(f"  ⏱️ {result.get('elapsed')}")
        else:
            print(f"  ❌ [{result.get('type')}] {result.get('error')}")
