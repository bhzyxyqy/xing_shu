import json
import sys
from pathlib import Path
from typing import Tuple


def _获取交易目录(文件夹名称: str) -> Tuple[Path, Path]:
    """获取交易平台运行时目录"""
    # 获取当前工作目录
    当前路径: Path = Path.cwd()

    # 拼接临时目录路径
    临时路径: Path = 当前路径.joinpath(文件夹名称)

    # 检查是否存在.vntrader目录
    if 临时路径.exists():
        return 当前路径, 临时路径

    # 获取用户主目录
    用户目录: Path = Path.home()
    临时路径 = 用户目录.joinpath(文件夹名称)

    # 创建不存在的目录
    if not 临时路径.exists():
        临时路径.mkdir()

    return 用户目录, 临时路径


# 初始化目录配置
交易目录, 临时目录 = _获取交易目录(".vntrader")
sys.path.append(str(交易目录))  # 添加至Python路径


def 获取文件路径(文件名称: str) -> Path:
    """获取临时目录下的文件完整路径"""
    return 临时目录.joinpath(文件名称)


def 加载json文件(文件名称: str) -> dict:
    """从临时目录加载JSON文件数据"""
    文件路径: Path = 获取文件路径(文件名称)

    if 文件路径.exists():
        with open(文件路径, mode="r", encoding="UTF-8") as 文件对象:
            数据字典: dict = json.load(文件对象)
        return 数据字典
    else:
        # 文件不存在时创建空文件
        保存json文件(文件名称, {})
        return {}


def 保存json文件(文件名称: str, 数据字典: dict) -> None:
    """保存数据到临时目录的JSON文件"""
    文件路径: Path = 获取文件路径(文件名称)
    with open(文件路径, mode="w+", encoding="UTF-8") as 文件对象:
        json.dump(
            数据字典,
            文件对象,
            indent=4,           # 4空格缩进
            ensure_ascii=False  # 支持非ASCII字符
        )


def 获取目录路径(目录名称: str) -> Path:
    """获取临时目录下的指定子目录路径"""
    目录路径: Path = 临时目录.joinpath(目录名称)

    if not 目录路径.exists():
        目录路径.mkdir()

    return 目录路径