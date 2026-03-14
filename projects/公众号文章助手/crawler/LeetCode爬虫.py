#!/usr/bin/env python3
"""
LeetCode爬虫 - 完整版
功能：
1. 获取题目列表
2. 获取题目详情
3. 获取代码示例
4. 分类整理
5. 难度筛选
"""
import requests
import os
import json

class LeetCodeCrawler:
    def __init__(self):
        self.api_url = "https://leetcode.com/graphql"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.output_dir = os.path.expanduser("~/项目/Ai学习系统/projects/公众号文章助手/content_library/LeetCode")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_problems(self, limit=50):
        """获取题目列表"""
        url = "https://leetcode.com/api/problems/algorithms/"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            return data.get('stat_status_pairs', [])[:limit]
        except Exception as e:
            print(f"获取失败: {e}")
            return []
    
    def get_problem_detail(self, title_slug):
        """获取题目详情"""
        query = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                difficulty
                content
                topicTags { name }
                codeSnippets { langSlug code }
            }
        }
        """
        
        variables = {"titleSlug": title_slug}
        data = {"query": query, "variables": variables}
        
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers=self.headers,
                timeout=10
            )
            return response.json().get('data', {}).get('question')
        except:
            return None
    
    def categorize(self, problems):
        """按分类整理"""
        categories = {
            '简单': [],
            '中等': [],
            '困难': []
        }
        
        level_map = {1: '简单', 2: '中等', 3: '困难'}
        
        for p in problems:
            stat = p.get('stat', {})
            difficulty = p.get('difficulty', {})
            level = difficulty.get('level', 0)
            
            categories[level_map.get(level, '中等')].append({
                'title': stat.get('question__title', ''),
                'slug': stat.get('question__title_slug', '')
            })
        
        return categories
    
    def save_all(self, problems):
        """保存所有内容"""
        print("\n" + "="*50)
        print("📚 正在保存到知识库...")
        print("="*50)
        
        # 1. 保存完整列表
        self.save_full_list(problems)
        
        # 2. 按难度分类保存
        self.save_by_difficulty(problems)
        
        # 3. 保存统计
        self.save_stats(problems)
        
        print(f"\n✅ 全部保存完成!")
        print(f"📁 位置: {self.output_dir}")
    
    def save_full_list(self, problems):
        """保存完整列表"""
        content = "# LeetCode算法题库 - 完整版\n\n"
        content += f"总共: {len(problems)} 题\n\n"
        content += "## 全部题目\n\n"
        
        level_map = {1: '简单', 2: '中等', 3: '困难'}
        
        for i, p in enumerate(problems, 1):
            stat = p.get('stat', {})
            difficulty = p.get('difficulty', {})
            level = difficulty.get('level', 0)
            
            title = stat.get('question__title', '')
            slug = stat.get('question__title_slug', '')
            
            content += f"{i:3}. [{title}](https://leetcode.com/problems/{slug}/) - {level_map.get(level, '未知')}\n"
        
        with open(f"{self.output_dir}/完整题库.md", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 完整题库.md")
    
    def save_by_difficulty(self, problems):
        """按难度分类保存"""
        level_map = {1: '简单', 2: '中等', 3: '困难'}
        
        for level in ['简单', '中等', '困难']:
            content = f"# LeetCode - {level}题\n\n"
            content += f"## {level}题目列表\n\n"
            
            count = 0
            for p in problems:
                stat = p.get('stat', {})
                difficulty = p.get('difficulty', {})
                l = difficulty.get('level', 0)
                
                if level_map.get(l) == level:
                    count += 1
                    title = stat.get('question__title', '')
                    slug = stat.get('question__title_slug', '')
                    content += f"{count}. [{title}](https://leetcode.com/problems/{slug}/)\n"
            
            filename = f"{level}题.md"
            with open(f"{self.output_dir}/{filename}", 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filename} ({count}题)")
    
    def save_stats(self, problems):
        """保存统计"""
        level_map = {1: '简单', 2: '中等', 3: '困难'}
        stats = {'简单': 0, '中等': 0, '困难': 0}
        
        for p in problems:
            difficulty = p.get('difficulty', {})
            level = difficulty.get('level', 0)
            stats[level_map.get(level, '中等')] += 1
        
        content = "# LeetCode学习统计\n\n"
        content += "## 难度分布\n\n"
        content += f"| 难度 | 数量 | 进度 |\n"
        content += f"|------|------|------|\n"
        
        for level in ['简单', '中等', '困难']:
            count = stats[level]
            bar = '█' * count
            content += f"| {level} | {count} | {bar} |\n"
        
        content += "\n## 学习建议\n\n"
        content += "1. 入门: 从简单题开始\n"
        content += "2. 进阶: 掌握中等难度\n"
        content += "3. 冲刺: 挑战困难题\n\n"
        content += "## 目标\n\n"
        content += f"- [ ] 简单题: {stats['简单']} / {stats['简单']}\n"
        content += f"- [ ] 中等题: 0 / {stats['中等']}\n"
        content += f"- [ ] 困难题: 0 / {stats['困难']}\n"
        
        with open(f"{self.output_dir}/学习统计.md", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 学习统计.md")
    
    def demo_detail(self):
        """演示获取详情"""
        print("\n" + "="*50)
        print("🔍 演示: 获取题目详情")
        print("="*50)
        
        # 获取第一题的详情
        problems = self.get_problems(1)
        
        if problems:
            stat = problems[0].get('stat', {})
            slug = stat.get('question__title_slug', '')
            
            print(f"\n📝 题目: {stat.get('question__title')}")
            print(f"🔗 链接: https://leetcode.com/problems/{slug}/\n")
            
            # 获取详情
            detail = self.get_problem_detail(slug)
            
            if detail:
                print(f"📊 难度: {detail.get('difficulty')}")
                print(f"🏷️ 标签: {', '.join([t['name'] for t in detail.get('topicTags', [])])}")
                print(f"\n📄 描述 (前200字):")
                print(detail.get('content', '')[:200])
                
                # 代码示例
                snippets = detail.get('codeSnippets', [])
                for s in snippets:
                    if s['langSlug'] == 'python3':
                        print(f"\n💻 Python代码:")
                        print(f"```python\n{s['code'][:300]}...\n```")
                        break
        
        return detail

def main():
    crawler = LeetCodeCrawler()
    
    print("="*50)
    print("🚀 LeetCode爬虫 - 完整版")
    print("="*50)
    
    # 1. 获取题目
    print("\n📥 获取题目列表...")
    problems = crawler.get_problems(20)
    print(f"✅ 获取到 {len(problems)} 道题目")
    
    # 2. 显示列表
    print("\n📋 题目列表:")
    print("-"*40)
    
    level_map = {1: '简单', 2: '中等', 3: '困难'}
    for i, p in enumerate(problems[:10], 1):
        stat = p.get('stat', {})
        difficulty = p.get('difficulty', {})
        level = difficulty.get('level', 0)
        
        print(f"{i:2}. {stat.get('question__title'):40} [{level_map.get(level, '未知')}]")
    
    # 3. 保存
    crawler.save_all(problems)
    
    # 4. 演示详情
    crawler.demo_detail()

if __name__ == '__main__':
    main()
