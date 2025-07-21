#!/usr/bin/env python3
"""
简单的git信息提取脚本
"""

import subprocess
import os

def run_git(cmd):
    """执行git命令"""
    try:
        result = subprocess.run(["git"] + cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return ""

def main():
    print("=" * 50)
    print("GIT信息")
    print("=" * 50)
    
    # 仓库名称
    repo_name = os.path.basename(os.getcwd())
    print(f"仓库: {repo_name}")
    
    # 当前分支
    branch = run_git(["branch", "--show-current"])
    print(f"分支: {branch}")
    
    # 最新提交
    commit = run_git(["log", "-1", "--oneline"])
    print(f"最新提交: {commit}")
    
    # 远程仓库
    remote = run_git(["config", "--get", "remote.origin.url"])
    print(f"远程: {remote}")
    
    # 文件状态
    status = run_git(["status", "--porcelain"])
    if status:
        modified = len([line for line in status.split("\n") if line.startswith(" M") or line.startswith("M ")])
        untracked = len([line for line in status.split("\n") if line.startswith("??")])
        print(f"已修改: {modified} 个文件")
        print(f"未跟踪: {untracked} 个文件")
    else:
        print("工作区: 干净")
    
    # 提交数
    commits = run_git(["rev-list", "--count", "HEAD"])
    print(f"总提交: {commits}")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 