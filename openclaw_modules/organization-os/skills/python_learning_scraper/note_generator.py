"""
Note Generator - 学习笔记生成
"""

import os
from datetime import datetime
from pathlib import Path


class NoteGenerator:
    """学习笔记生成器"""
    
    def __init__(self, output_dir: str = None):
        """
        初始化
        
        Args:
            output_dir: 输出目录
        """
        if output_dir is None:
            output_dir = os.path.expanduser("~/ai-learning-notes")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_youtube_notes(self, videos: list, topic: str) -> str:
        """
        生成 YouTube 视频笔记
        
        Args:
            videos: 视频列表
            topic: 主题
            
        Returns:
            笔记文件路径
        """
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date}_{topic}_youtube.md"
        filepath = self.output_dir / filename
        
        content = f"""# {topic} - YouTube 教程

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 视频列表

| 序号 | 标题 | 时长 | 频道 | 链接 |
|------|------|------|------|------|

"""
        
        for i, video in enumerate(videos, 1):
            title = video.get('title', '')
            duration = video.get('duration', '')
            channel = video.get('channel', '')
            url = video.get('url', '')
            
            content += f"| {i} | {title} | {duration} | {channel} | [观看]({url}) |\n"
        
        content += f"""

## 学习建议

- [ ] 观看所有视频
- [ ] 记录重点
- [ ] 动手实践

---
*由 AI Agent 自动生成*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_wechat_notes(self, articles: list, topic: str) -> str:
        """
        生成微信公众号文章笔记
        
        Args:
            articles: 文章列表
            topic: 主题
            
        Returns:
            笔记文件路径
        """
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date}_{topic}_wechat.md"
        filepath = self.output_dir / filename
        
        content = f"""# {topic} - 微信公众号文章

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 文章列表

"""
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', '')
            author = article.get('author', '')
            date = article.get('date', '')
            url = article.get('url', '')
            content_preview = article.get('content', '')[:500]
            
            content += f"""### {i}. {title}

- 作者: {author}
- 日期: {date}
- 链接: {url}

**内容摘要:**

{content_preview}...

---

"""
        
        content += """
## 学习建议

- [ ] 阅读所有文章
- [ ] 提取关键知识点
- [ ] 整理思维导图

---
*由 AI Agent 自动生成*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def list_notes(self) -> list:
        """列出所有笔记"""
        return sorted([f.name for f in self.output_dir.glob("*.md")])


if __name__ == "__main__":
    generator = NoteGenerator()
    
    # 测试
    videos = [
        {'title': 'Python Tutorial 1', 'duration': '10:00', 'channel': 'ABC', 'url': 'https://youtube.com/1'},
        {'title': 'Python Tutorial 2', 'duration': '15:00', 'channel': 'XYZ', 'url': 'https://youtube.com/2'},
    ]
    
    path = generator.generate_youtube_notes(videos, "Python")
    print(f"Generated: {path}")
    print(f"Notes: {generator.list_notes()}")
