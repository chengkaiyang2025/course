# Git信息提取脚本使用说明

这个项目包含两个Python脚本，用于提取git仓库的各种信息。

## 脚本说明

### 1. `git_info_extractor.py` - 完整版脚本

功能最全面的git信息提取脚本，提供以下功能：

- **基本仓库信息**: 仓库名称、当前分支、远程仓库URL
- **提交历史**: 详细的提交信息（作者、时间、消息等）
- **分支信息**: 本地和远程分支列表及统计
- **文件状态**: 已修改、未跟踪、已暂存的文件
- **仓库统计**: 总提交数、文件数、仓库大小等
- **贡献者信息**: 所有贡献者及其提交数
- **活跃度分析**: 最近30天的提交活动

### 2. `simple_git_info.py` - 简化版脚本

轻量级的git信息提取脚本，适合快速查看：

- **基本仓库信息**: 仓库名称、当前分支、远程仓库
- **当前状态**: 工作区文件状态
- **统计信息**: 总提交数、文件数、分支数

## 使用方法

### 完整版脚本使用

```bash
# 基本使用（提取当前目录的git信息）
python git_info_extractor.py

# 指定仓库路径
python git_info_extractor.py --path /path/to/repo

# 指定输出文件
python git_info_extractor.py --output my_git_info.json

# 限制提交历史数量
python git_info_extractor.py --limit 20

# 只打印摘要，不保存文件
python git_info_extractor.py --no-save

# 显示详细信息
python git_info_extractor.py --verbose

# 查看帮助
python git_info_extractor.py --help
```

### 简化版脚本使用

```bash
# 直接运行（必须在git仓库目录内）
python simple_git_info.py
```

## 输出示例

### 完整版输出摘要
```
==================================================
GIT仓库信息摘要
==================================================
仓库名称: course
当前分支: main
远程仓库: https://github.com/username/course.git

最新提交: a1b2c3d4 - 更新课程内容
提交者: 张三 (zhangsan@example.com)
提交时间: 2024-01-15T10:30:00+08:00

分支统计:
  本地分支: 3 个
  远程分支: 2 个

文件状态:
  已修改: 2 个文件
  未跟踪: 1 个文件
  已暂存: 0 个文件

仓库统计:
  总提交数: 45
  总文件数: 156
  最近30天活动: 12 次提交
  仓库大小: 2.5 MB

主要贡献者:
  1. 张三 (25 次提交)
  2. 李四 (15 次提交)
  3. 王五 (5 次提交)
==================================================
```

### 简化版输出
```
============================================================
GIT仓库信息
============================================================
提取时间: 2024-01-15 10:30:00

仓库信息:
  仓库名称: course
  当前分支: main
  远程仓库: https://github.com/username/course.git
  最新提交:
    哈希: a1b2c3d4
    作者: 张三
    日期: 2024-01-15
    消息: 更新课程内容

当前状态:
  已修改文件: 2
  未跟踪文件: 1
  已暂存文件: 0

统计信息:
  总提交数: 45
  总文件数: 156
  本地分支数: 3 个
  本地分支:
    - main
    - develop
    - feature/new-module
============================================================
```

## 输出文件格式

两个脚本都会生成JSON格式的输出文件：

- 完整版: `git_info.json` (默认) 或自定义文件名
- 简化版: `git_info_simple.json`

JSON文件包含结构化的git信息，便于程序化处理和分析。

## 系统要求

- Python 3.6+
- Git已安装并配置
- 在git仓库目录内运行（或指定正确的仓库路径）

## 错误处理

脚本包含完善的错误处理机制：

- 检查是否为有效的git仓库
- 处理git命令执行失败的情况
- 提供清晰的错误信息

## 扩展功能

完整版脚本的`GitInfoExtractor`类可以轻松扩展：

```python
from git_info_extractor import GitInfoExtractor

# 创建提取器实例
extractor = GitInfoExtractor("/path/to/repo")

# 获取特定信息
basic_info = extractor.get_basic_info()
commit_history = extractor.get_commit_history(limit=5)
file_status = extractor.get_file_status()

# 自定义处理
# ... 你的代码 ...
```

## 注意事项

1. 确保在git仓库目录内运行脚本
2. 某些git命令可能需要网络连接（如获取远程分支信息）
3. 大型仓库的统计信息提取可能需要较长时间
4. 建议定期运行脚本以跟踪项目发展情况 