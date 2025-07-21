#!/usr/bin/env python3
"""
简化版Git信息提取脚本
快速提取git仓库的基本信息
"""

import subprocess
import json
import os
from datetime import datetime

def run_git_command(command):
    """执行git命令"""
    try:
        result = subprocess.run(
            ["git"] + command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def get_git_info():
    """获取git仓库信息"""
    info = {
        "提取时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "仓库信息": {},
        "当前状态": {},
        "统计信息": {}
    }
    
    # 基本仓库信息
    info["仓库信息"]["仓库名称"] = os.path.basename(os.getcwd())
    info["仓库信息"]["当前分支"] = run_git_command(["branch", "--show-current"])
    info["仓库信息"]["远程仓库"] = run_git_command(["config", "--get", "remote.origin.url"]) or "无"
    
    # 最新提交
    latest_commit = run_git_command(["log", "-1", "--pretty=format:%H|%an|%ad|%s", "--date=short"])
    if latest_commit:
        parts = latest_commit.split("|")
        info["仓库信息"]["最新提交"] = {
            "哈希": parts[0][:8],
            "作者": parts[1],
            "日期": parts[2],
            "消息": parts[3]
        }
    
    # 当前状态
    status = run_git_command(["status", "--porcelain"])
    if status:
        modified = len([line for line in status.split("\n") if line.startswith(" M") or line.startswith("M ")])
        untracked = len([line for line in status.split("\n") if line.startswith("??")])
        staged = len([line for line in status.split("\n") if line.startswith("A ") or line.startswith("M ") or line.startswith("D ")])
        
        info["当前状态"]["已修改文件"] = modified
        info["当前状态"]["未跟踪文件"] = untracked
        info["当前状态"]["已暂存文件"] = staged
    else:
        info["当前状态"]["工作区状态"] = "干净"
    
    # 统计信息
    total_commits = run_git_command(["rev-list", "--count", "HEAD"])
    info["统计信息"]["总提交数"] = int(total_commits) if total_commits else 0
    
    file_count = len(run_git_command(["ls-files"]).split("\n")) if run_git_command(["ls-files"]) else 0
    info["统计信息"]["总文件数"] = file_count
    
    # 分支信息
    branches = run_git_command(["branch", "--format=%(refname:short)"])
    if branches:
        local_branches = [b.strip() for b in branches.split("\n") if b.strip()]
        info["统计信息"]["本地分支数"] = len(local_branches)
        info["统计信息"]["本地分支"] = local_branches
    
    return info

def print_info(info):
    """打印信息"""
    print("=" * 60)
    print("GIT仓库信息")
    print("=" * 60)
    print(f"提取时间: {info['提取时间']}")
    print()
    
    print("仓库信息:")
    for key, value in info["仓库信息"].items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    print()
    
    print("当前状态:")
    for key, value in info["当前状态"].items():
        print(f"  {key}: {value}")
    print()
    
    print("统计信息:")
    for key, value in info["统计信息"].items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} 个")
            if len(value) <= 5:
                for item in value:
                    print(f"    - {item}")
        else:
            print(f"  {key}: {value}")
    
    print("=" * 60)

def main():
    """主函数"""
    try:
        # 检查是否为git仓库
        if not os.path.exists(".git"):
            print("错误: 当前目录不是一个git仓库")
            return
        
        # 获取信息
        info = get_git_info()
        
        # 打印信息
        print_info(info)
        
        # 保存到文件
        with open("git_info_simple.json", "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        print("\n信息已保存到 git_info_simple.json")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main() 