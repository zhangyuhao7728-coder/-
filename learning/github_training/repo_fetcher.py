#!/usr/bin/env python3
"""
Repo Fetcher - GitHub项目获取
"""
import requests
from typing import Dict, List


class RepoFetcher:
    """GitHub仓库获取"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.cache = {}
    
    def fetch_repo(self, repo: str) -> Dict:
        """获取仓库信息"""
        
        # 检查缓存
        if repo in self.cache:
            return self.cache[repo]
        
        try:
            url = f"{self.base_url}/repos/{repo}"
            resp = requests.get(url, timeout=30)
            
            if resp.status_code == 200:
                data = resp.json()
                self.cache[repo] = data
                return data
            else:
                return {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_readme(self, repo: str) -> str:
        """获取README"""
        
        try:
            url = f"{self.base_url}/repos/{repo}/readme"
            resp = requests.get(url, timeout=30)
            
            if resp.status_code == 200:
                import base64
                data = resp.json()
                content = data.get("content", "")
                return base64.b64decode(content).decode("utf-8")
        except:
            pass
        
        return "无法获取README"
    
    def get_files(self, repo: str, path: str = "") -> List:
        """获取文件列表"""
        
        try:
            url = f"{self.base_url}/repos/{repo}/contents/{path}"
            resp = requests.get(url, timeout=30)
            
            if resp.status_code == 200:
                return resp.json()
        except:
            pass
        
        return []
    
    def get_python_files(self, repo: str) -> List:
        """获取Python文件"""
        
        files = []
        
        def explore(path=""):
            contents = self.get_files(repo, path)
            
            for item in contents:
                if isinstance(item, dict):
                    if item.get("type") == "file" and item["name"].endswith(".py"):
                        files.append(item["path"])
                    elif item.get("type") == "dir" and path.count("/") < 2:
                        explore(item["path"])
        
        explore()
        return files
    
    def search_code(self, repo: str, keyword: str) -> List:
        """搜索代码"""
        
        try:
            url = f"{self.base_url}/search/code"
            params = {"q": f"repo:{repo} {keyword}"}
            resp = requests.get(url, params=params, timeout=30)
            
            if resp.status_code == 200:
                data = resp.json()
                return data.get("items", [])[:10]
        except:
            pass
        
        return []


_fetcher = None

def get_repo_fetcher() -> RepoFetcher:
    global _fetcher
    if _fetcher is None:
        _fetcher = RepoFetcher()
    return _fetcher


def fetch_repo(repo: str) -> Dict:
    return get_repo_fetcher().fetch_repo(repo)


# 测试
if __name__ == "__main__":
    fetcher = get_repo_fetcher()
    
    print("=== GitHub仓库获取测试 ===\n")
    
    # 测试获取
    repo = "psf/requests"
    info = fetcher.fetch_repo(repo)
    
    if "error" not in info:
        print(f"仓库: {info.get('full_name')}")
        print(f"描述: {info.get('description')}")
        print(f"⭐ Stars: {info.get('stargazers_count')}")
    else:
        print(f"错误: {info['error']}")
