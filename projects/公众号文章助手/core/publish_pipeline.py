#!/usr/bin/env python3
"""
AI公众号内容生产系统 - 终极自动化
一键生成完整公众号文章
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 添加项目路径
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

class AutoPublisher:
    """自动发布器"""
    
    def __init__(self):
        self.project_dir = PROJECT_DIR
        self.output_dir = self.project_dir / 'output' / 'published_articles'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print("="*60)
        print("🤖 AI公众号内容生产系统 - 终极自动化")
        print("="*60)
    
    def step1_topic(self, topic: str = None) -> str:
        """步骤1: 选题"""
        print("\n📌 步骤1: 智能选题")
        print("-"*40)
        
        if topic:
            print(f"   使用指定主题: {topic}")
            return topic
        
        # 自动选题
        try:
            from crawler.选题系统 import TopicSelectorV2
            selector = TopicSelectorV2()
            daily = selector.get_daily_topics()
            
            if daily['recommendations']:
                topic = daily['recommendations'][0]['topic']
                print(f"   智能推荐: {topic}")
                return topic
        except:
            pass
        
        # 默认主题
        return "AI学习路线规划"
    
    def step2_crawl(self, topic: str) -> str:
        """步骤2: 采集参考"""
        print("\n📥 步骤2: 采集参考文章")
        print("-"*40)
        
        # 尝试抓取（可选）
        print(f"   主题: {topic}")
        print(f"   [可选] 如有参考链接可添加")
        
        return None
    
    def step3_parse(self, html_file: str = None) -> dict:
        """步骤3: 解析结构"""
        print("\n🔍 步骤3: 解析文章结构")
        print("-"*40)
        
        if html_file and os.path.exists(html_file):
            try:
                from tools.文章结构解析 import parse_article
                result = parse_article(html_file)
                print(f"   解析完成: {result.get('title', 'N/A')}")
                return result
            except:
                pass
        
        print("   使用默认结构模板")
        return {
            'title': '',
            'sections_count': 5,
            'template_type': '教程类'
        }
    
    def step4_style(self, style_name: str = '余豪风格') -> dict:
        """步骤4: 分析风格"""
        print("\n🎨 步骤4: 风格学习")
        print("-"*40)
        
        try:
            from tools.风格分析 import load_style
            style = load_style(style_name)
            if style:
                print(f"   加载风格: {style_name}")
                print(f"   语气: {style.get('tone', '轻松')}")
                return style
        except:
            pass
        
        # 默认风格
        default_style = {
            'tone': '轻松',
            'sentence_length': '短句',
            'emoji': True,
            'opening': '大家好，我是余豪',
            'closing': '有问题评论区见！'
        }
        print(f"   使用默认风格")
        return default_style
    
    def step5_write(self, topic: str, style: dict, article_type: str = '安全科普') -> dict:
        """步骤5: AI写作"""
        print("\n✍️ 步骤5: AI写作")
        print("-"*40)
        
        # 生成文章结构
        try:
            from tools.风格生成 import AIWriter
            writer = AIWriter()
            article = writer.generate_article(topic, '余豪风格', article_type)
            
            print(f"   标题: {article.get('title', topic)}")
            print(f"   结构: {len(article.get('structure', []))}个章节")
            
            return article
        except Exception as e:
            print(f"   ⚠️ AI生成需要配置LLM")
            # 返回基础结构
            return {
                'title': topic,
                'topic': topic,
                'structure': [
                    {'title': '背景', 'type': 'intro'},
                    {'title': '内容', 'type': 'content'},
                    {'title': '总结', 'type': 'summary'}
                ]
            }
    
    def step6_seo(self, title: str, content: str = '') -> dict:
        """步骤6: SEO优化"""
        print("\n🔍 步骤6: SEO优化")
        print("-"*40)
        
        try:
            from tools.文章优化 import optimize_title
            result = optimize_title(title)
            
            print(f"   原标题: {title}")
            print(f"   评分: {result.get('score', 0)}/100")
            
            # 生成变体
            variants = result.get('suggestions', [])
            if variants:
                print(f"   优化建议: {variants[0]}")
            
            return result
        except:
            pass
        
        return {'title': title, 'score': 50}
    
    def step7_cover(self, title: str) -> str:
        """步骤7: 生成封面"""
        print("\n🖼️ 步骤7: 生成封面")
        print("-"*40)
        
        try:
            from tools.生成封面 import generate_cover
            
            cover_file = self.output_dir / 'covers' / f'{datetime.now().strftime("%Y%m%d")}_cover.html'
            cover_file.parent.mkdir(exist_ok=True)
            
            generate_cover(
                title=title,
                subtitle='AI公众号内容生产系统',
                tags=['AI', '学习', '教程'],
                template='tech',
                output=str(cover_file)
            )
            
            print(f"   封面: {cover_file.name}")
            return str(cover_file)
        except Exception as e:
            print(f"   生成失败: {e}")
            return None
    
    def step8_format(self, content: str, title: str) -> str:
        """步骤8: 排版"""
        print("\n📝 步骤8: 公众号排版")
        print("-"*40)
        
        try:
            # 保存内容到临时文件
            temp_md = self.output_dir / 'temp_format.md'
            with open(temp_md, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 调用排版
            from formatter.markdown_to_wechat import format_wechat
            format_wechat(str(temp_md), str(self.output_dir / 'temp_wechat.html'))
            
            # 重命名
            output_file = self.output_dir / f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_wechat.html'
            (self.output_dir / 'temp_wechat.html').rename(output_file)
            
            # 删除临时文件
            temp_md.unlink()
            
            print(f"   排版文件: {output_file.name}")
            return str(output_file)
        except Exception as e:
            print(f"   排版失败: {e}")
            return None
    
    def step9_save(self, article: dict, title: str) -> str:
        """步骤9: 保存"""
        print("\n💾 步骤9: 保存文章")
        print("-"*40)
        
        # 保存Markdown
        md_file = self.output_dir / f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        content = f"""# {title}

> 由AI公众号内容生产系统自动生成
> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 文章信息

- 主题: {article.get('topic', 'N/A')}
- 类型: {article.get('type', '经验分享')}
- 风格: {article.get('style', '余豪风格')}

---

## 文章结构

"""
        
        # 添加结构
        for i, s in enumerate(article.get('structure', []), 1):
            content += f"\n### {i}. {s.get('title', '章节')}\n\n"
            content += f"（内容）\n"
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   Markdown: {md_file.name}")
        
        # 更新CMS
        try:
            from cms import ContentManager
            cms = ContentManager(str(self.output_dir))
            cms.add_article(
                title=title,
                content=str(md_file),
                category='AI学习',
                status='draft'
            )
            print(f"   已添加到CMS")
        except:
            pass
        
        return str(md_file)
    
    def run(self, topic: str = None, style: str = '余豪风格', 
            article_type: str = '安全科普') -> dict:
        """运行完整流程"""
        print(f"\n🚀 开始自动生成...")
        print(f"📌 主题: {topic or '自动选择'}")
        print(f"🎨 风格: {style}")
        print(f"📄 类型: {article_type}")
        
        # 1. 选题
        topic = self.step1_topic(topic)
        
        # 2. 采集（可选）
        self.step2_crawl(topic)
        
        # 3. 解析
        parsed = self.step3_parse()
        
        # 4. 风格
        style_data = self.step4_style(style)
        
        # 5. 写作
        article = self.step5_write(topic, style_data, article_type)
        
        # 获取标题
        title = article.get('title', topic)
        
        # 6. SEO
        seo = self.step6_seo(title)
        
        # 7. 封面
        cover = self.step7_cover(title)
        
        # 8. 排版（如果有内容）
        content_md = f"# {title}\n\n（AI生成的内容）"
        formatted = self.step8_format(content_md, title)
        
        # 9. 保存
        saved = self.step9_save(article, title)
        
        # 完成
        print("\n" + "="*60)
        print("✅ 自动生成完成！")
        print("="*60)
        
        return {
            'topic': topic,
            'title': title,
            'status': 'success',
            'files': {
                'markdown': saved,
                'cover': cover,
                'formatted': formatted,
            }
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI公众号内容生产系统 - 终极自动化')
    parser.add_argument('--topic', '-t', help='文章主题')
    parser.add_argument('--style', '-s', default='余豪风格', help='风格')
    parser.add_argument('--type', '-y', default='安全科普', help='文章类型')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    
    args = parser.parse_args()
    
    if args.interactive:
        print("\n🎯 欢迎使用AI公众号内容生产系统")
        topic = input("请输入文章主题（直接回车使用智能推荐）: ").strip()
        if not topic:
            topic = None
    else:
        topic = args.topic
    
    # 运行
    publisher = AutoPublisher()
    result = publisher.run(topic, args.style, args.type)
    
    print(f"\n📁 输出目录: {publisher.output_dir}")

if __name__ == '__main__':
    main()
