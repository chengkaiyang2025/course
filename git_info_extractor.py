#!/usr/bin/env python3
"""
Git信息提取脚本
提取git仓库的各种有用信息，包括提交历史、分支、文件状态等
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class GitInfoExtractor:
    def __init__(self, repo_path: str = "."):
        """
        初始化Git信息提取器
        
        Args:
            repo_path: git仓库路径，默认为当前目录
        """
        self.repo_path = os.path.abspath(repo_path)
        self.git_dir = os.path.join(self.repo_path, ".git")
        
        # 检查是否为git仓库
        if not os.path.exists(self.git_dir):
            raise ValueError(f"路径 {self.repo_path} 不是一个有效的git仓库")
    
    def run_git_command(self, command: List[str]) -> str:
        """
        执行git命令并返回结果
        
        Args:
            command: git命令列表
            
        Returns:
            命令输出结果
        """
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git命令执行失败: {' '.join(command)}")
            print(f"错误信息: {e.stderr}")
            return ""
    
    def get_basic_info(self) -> Dict[str, Any]:
        """获取基本git信息"""
        info = {}
        
        # 仓库名称
        info["repository_name"] = os.path.basename(self.repo_path)
        
        # 远程仓库URL
        remote_url = self.run_git_command(["config", "--get", "remote.origin.url"])
        info["remote_url"] = remote_url if remote_url else "无远程仓库"
        
        # 当前分支
        current_branch = self.run_git_command(["branch", "--show-current"])
        info["current_branch"] = current_branch
        
        # 最新提交信息
        latest_commit = self.run_git_command([
            "log", "-1", "--pretty=format:%H|%an|%ae|%ad|%s",
            "--date=iso"
        ])
        if latest_commit:
            parts = latest_commit.split("|")
            info["latest_commit"] = {
                "hash": parts[0],
                "author": parts[1],
                "email": parts[2],
                "date": parts[3],
                "message": parts[4]
            }
        
        return info
    
    def get_branch_info(self) -> Dict[str, Any]:
        """获取分支信息"""
        info = {}
        
        # 所有本地分支
        local_branches = self.run_git_command(["branch", "--format=%(refname:short)"])
        info["local_branches"] = [b.strip() for b in local_branches.split("\n") if b.strip()]
        
        # 所有远程分支
        remote_branches = self.run_git_command(["branch", "-r", "--format=%(refname:short)"])
        info["remote_branches"] = [b.strip() for b in remote_branches.split("\n") if b.strip()]
        
        # 分支统计
        info["branch_stats"] = {
            "local_count": len(info["local_branches"]),
            "remote_count": len(info["remote_branches"])
        }
        
        return info
    
    def get_commit_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取提交历史
        
        Args:
            limit: 获取的提交数量限制
            
        Returns:
            提交历史列表
        """
        commits = []
        
        # 获取提交历史
        commit_log = self.run_git_command([
            "log", f"-{limit}", 
            "--pretty=format:%H|%an|%ae|%ad|%s|%b",
            "--date=iso"
        ])
        
        if commit_log:
            for line in commit_log.split("\n"):
                if line.strip():
                    parts = line.split("|", 5)
                    if len(parts) >= 5:
                        commit_info = {
                            "hash": parts[0],
                            "author": parts[1],
                            "email": parts[2],
                            "date": parts[3],
                            "message": parts[4],
                            "body": parts[5] if len(parts) > 5 else ""
                        }
                        commits.append(commit_info)
        
        return commits
    
    def get_file_status(self) -> Dict[str, Any]:
        """获取文件状态信息"""
        status = {}
        
        # 获取工作区状态
        git_status = self.run_git_command(["status", "--porcelain"])
        
        if git_status:
            lines = git_status.split("\n")
            modified_files = []
            untracked_files = []
            staged_files = []
            
            for line in lines:
                if line.strip():
                    status_code = line[:2]
                    filename = line[3:]
                    
                    if status_code == "M ":
                        modified_files.append(filename)
                    elif status_code == " M":
                        modified_files.append(filename)
                    elif status_code == "??":
                        untracked_files.append(filename)
                    elif status_code in ["A ", "M ", "D "]:
                        staged_files.append(filename)
            
            status["modified_files"] = modified_files
            status["untracked_files"] = untracked_files
            status["staged_files"] = staged_files
            status["total_changes"] = len(modified_files) + len(untracked_files) + len(staged_files)
        else:
            status["modified_files"] = []
            status["untracked_files"] = []
            status["staged_files"] = []
            status["total_changes"] = 0
        
        return status
    
    def get_repo_stats(self) -> Dict[str, Any]:
        """获取仓库统计信息"""
        stats = {}
        
        # 总提交数
        total_commits = self.run_git_command(["rev-list", "--count", "HEAD"])
        stats["total_commits"] = int(total_commits) if total_commits else 0
        
        # 文件数量
        file_count = self.run_git_command(["ls-files"]).count("\n") + 1
        stats["total_files"] = file_count
        
        # 仓库大小（近似）
        repo_size = self.run_git_command(["count-objects", "-vH"])
        if repo_size:
            for line in repo_size.split("\n"):
                if "size-pack" in line:
                    stats["repo_size"] = line.split(":")[1].strip()
                    break
        
        # 活跃度统计（最近30天的提交数）
        recent_commits = self.run_git_command([
            "log", "--since=30 days ago", "--oneline"
        ])
        stats["recent_activity"] = len([c for c in recent_commits.split("\n") if c.strip()])
        
        return stats
    
    def get_contributors(self) -> List[Dict[str, Any]]:
        """获取贡献者信息"""
        contributors = []
        
        # 获取所有贡献者及其提交数
        contributor_stats = self.run_git_command([
            "shortlog", "-sn", "--no-merges"
        ])
        
        if contributor_stats:
            for line in contributor_stats.split("\n"):
                if line.strip():
                    parts = line.strip().split("\t")
                    if len(parts) == 2:
                        contributors.append({
                            "name": parts[1],
                            "commits": int(parts[0])
                        })
        
        return contributors
    
    def extract_all_info(self, commit_limit: int = 10) -> Dict[str, Any]:
        """
        提取所有git信息
        
        Args:
            commit_limit: 提交历史数量限制
            
        Returns:
            包含所有git信息的字典
        """
        print("正在提取git信息...")
        
        all_info = {
            "extraction_time": datetime.now().isoformat(),
            "repository_path": self.repo_path,
            "basic_info": self.get_basic_info(),
            "branch_info": self.get_branch_info(),
            "commit_history": self.get_commit_history(commit_limit),
            "file_status": self.get_file_status(),
            "repo_stats": self.get_repo_stats(),
            "contributors": self.get_contributors()
        }
        
        return all_info
    
    def save_to_json(self, info: Dict[str, Any], filename: str = "git_info.json"):
        """
        将git信息保存为JSON文件
        
        Args:
            info: git信息字典
            filename: 输出文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        print(f"Git信息已保存到 {filename}")
    
    def print_summary(self, info: Dict[str, Any]):
        """打印git信息摘要"""
        print("\n" + "="*50)
        print("GIT仓库信息摘要")
        print("="*50)
        
        basic = info["basic_info"]
        print(f"仓库名称: {basic['repository_name']}")
        print(f"当前分支: {basic['current_branch']}")
        print(f"远程仓库: {basic['remote_url']}")
        
        if "latest_commit" in basic:
            commit = basic["latest_commit"]
            print(f"最新提交: {commit['hash'][:8]} - {commit['message']}")
            print(f"提交者: {commit['author']} ({commit['email']})")
            print(f"提交时间: {commit['date']}")
        
        branch_info = info["branch_info"]
        print(f"\n分支统计:")
        print(f"  本地分支: {branch_info['branch_stats']['local_count']} 个")
        print(f"  远程分支: {branch_info['branch_stats']['remote_count']} 个")
        
        file_status = info["file_status"]
        print(f"\n文件状态:")
        print(f"  已修改: {len(file_status['modified_files'])} 个文件")
        print(f"  未跟踪: {len(file_status['untracked_files'])} 个文件")
        print(f"  已暂存: {len(file_status['staged_files'])} 个文件")
        
        repo_stats = info["repo_stats"]
        print(f"\n仓库统计:")
        print(f"  总提交数: {repo_stats['total_commits']}")
        print(f"  总文件数: {repo_stats['total_files']}")
        print(f"  最近30天活动: {repo_stats['recent_activity']} 次提交")
        if "repo_size" in repo_stats:
            print(f"  仓库大小: {repo_stats['repo_size']}")
        
        contributors = info["contributors"]
        if contributors:
            print(f"\n主要贡献者:")
            for i, contributor in enumerate(contributors[:5], 1):
                print(f"  {i}. {contributor['name']} ({contributor['commits']} 次提交)")
        
        print("="*50)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="提取git仓库信息")
    parser.add_argument("--path", "-p", default=".", help="git仓库路径 (默认: 当前目录)")
    parser.add_argument("--output", "-o", default="git_info.json", help="输出文件名 (默认: git_info.json)")
    parser.add_argument("--limit", "-l", type=int, default=10, help="提交历史数量限制 (默认: 10)")
    parser.add_argument("--no-save", action="store_true", help="不保存到文件，只打印摘要")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    try:
        # 创建提取器
        extractor = GitInfoExtractor(args.path)
        
        # 提取所有信息
        git_info = extractor.extract_all_info(args.limit)
        
        # 打印摘要
        extractor.print_summary(git_info)
        
        # 保存到文件
        if not args.no_save:
            extractor.save_to_json(git_info, args.output)
        
        # 详细模式显示完整信息
        if args.verbose:
            print("\n完整信息:")
            print(json.dumps(git_info, ensure_ascii=False, indent=2))
            
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"提取过程中发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 