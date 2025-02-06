from typing import Dict, List, Set, TYPE_CHECKING

from .模块_对象 import 类_合约数据, 类_订单数据, 类_成交数据, 类_持仓数据, 类_订单请求
from .模块_常数 import 方向, 开平, 交易所

if TYPE_CHECKING:
    from .模块_主引擎 import 类_主引擎


class 类_仓位转换器:
    """仓位转换管理器"""

    def __init__(self, 主引擎: "类_主引擎") -> None:
        self.持仓记录字典: Dict[str, "类_持仓记录"] = {}
        self.获取合约 = 主引擎.获取合约详情

    def 更新持仓(self, 持仓实例: 类_持仓数据) -> None:
        """更新持仓数据"""
        if not self.需要转换(持仓实例.唯一标识):
            return

        持仓记录 = self.获取持仓记录(持仓实例.唯一标识)
        持仓记录.更新持仓(持仓实例)

    def 更新成交(self, 成交实例: 类_成交数据) -> None:
        """更新成交数据"""
        if not self.需要转换(成交实例.唯一标识):
            return

        持仓记录 = self.获取持仓记录(成交实例.唯一标识)
        持仓记录.更新成交(成交实例)

    def 更新订单(self, 订单实例: 类_订单数据) -> None:
        """更新订单状态"""
        if not self.需要转换(订单实例.唯一标识):
            return

        持仓记录 = self.获取持仓记录(订单实例.唯一标识)
        持仓记录.更新订单(订单实例)

    def 更新订单请求(self, 请求: 类_订单请求, 订单标识: str) -> None:
        """关联订单请求与实际成交"""
        if not self.需要转换(请求.唯一标识):
            return

        持仓记录 = self.获取持仓记录(请求.唯一标识)
        持仓记录.关联订单请求(请求, 订单标识)

    def 获取持仓记录(self, 合约标识: str) -> "类_持仓记录":
        """获取或创建指定合约的持仓记录"""
        持仓记录 = self.持仓记录字典.get(合约标识, None)
        if not 持仓记录:
            合约实例 = self.获取合约(合约标识)
            持仓记录 = 类_持仓记录(合约实例)
            self.持仓记录字典[合约标识] = 持仓记录
        return 持仓记录

    def 转换订单请求(
            self,
            请求: 类_订单请求,
            锁定模式: bool,
            净仓模式: bool = False
    ) -> List[类_订单请求]:
        """根据持仓转换订单请求"""
        if not self.需要转换(请求.唯一标识):
            return [请求]

        持仓记录 = self.获取持仓记录(请求.唯一标识)

        if 锁定模式:
            return 持仓记录.转换为锁定单(请求)
        elif 净仓模式:
            return 持仓记录.转换为净仓单(请求)
        elif 请求.交易所 in {交易所.上期所, 交易所.能源中心}:
            return 持仓记录.转换为上期所模式(请求)
        else:
            return [请求]

    def 需要转换(self, 合约标识: str) -> bool:
        """检查是否需要仓位转换"""
        合约实例 = self.获取合约(合约标识)

        # 仅非净仓模式合约需要转换
        if not 合约实例:
            return False
        elif 合约实例.净持仓模式:
            return False
        else:
            return True


class 类_持仓记录:
    """单个合约的持仓记录管理"""

    def __init__(self, 合约实例: 类_合约数据) -> None:
        self.合约 = 合约实例
        self.交易所 = 合约实例.交易所

        # 多仓持仓
        self.多仓: int = 0
        self.多今: int = 0
        self.多昨: int = 0
        self.多冻结: int = 0

        # 空仓持仓
        self.空仓: int = 0
        self.空今: int = 0
        self.空昨: int = 0
        self.空冻结: int = 0

        # 订单跟踪
        self.待成交订单: Dict[str, 类_订单数据] = {}
        self.待成交请求: Dict[str, 类_订单请求] = {}

    def 更新持仓(self, 持仓实例: 类_持仓数据) -> None:
        """更新持仓数据"""
        if 持仓实例.方向 == 方向.做多:
            self.多仓 = 持仓实例.数量
            self.多昨 = 持仓实例.昨仓量
            self.多今 = self.多仓 - self.多昨
        else:
            self.空仓 = 持仓实例.数量
            self.空昨 = 持仓实例.昨仓量
            self.空今 = self.空仓 - self.空昨

    def 更新成交(self, 成交实例: 类_成交数据) -> None:
        """处理成交数据"""
        # 撤销关联订单的冻结持仓
        if 成交实例.订单编号 in self.待成交订单:
            订单 = self.待成交订单.pop(成交实例.订单编号)
            self.减少冻结(订单.方向, 订单.开平, 成交实例.数量)

    def 更新订单(self, 订单实例: 类_订单数据) -> None:
        """跟踪订单状态"""
        if not 订单实例.是否活跃():
            if 订单实例.订单编号 in self.待成交订单:
                self.待成交订单.pop(订单实例.订单编号)
        else:
            self.待成交订单[订单实例.订单编号] = 订单实例

    def 关联订单请求(self, 请求: 类_订单请求, 订单标识: str) -> None:
        """记录原始订单请求"""
        self.待成交请求[订单标识] = 请求

    def 转换为锁定单(self, 请求: 类_订单请求) -> List[类_订单请求]:
        """生成锁定单转换逻辑"""
        return self._拆分平仓请求(请求)

    def 转换为净仓单(self, 请求: 类_订单请求) -> List[类_订单请求]:
        """生成净仓单转换逻辑"""
        return self._拆分平仓请求(请求)

    def 转换为上期所模式(self, 请求: 类_订单请求) -> List[类_订单请求]:
        """上期所平今优先转换逻辑"""
        return self._拆分平仓请求(请求)

    def _拆分平仓请求(self, 请求: 类_订单请求) -> List[类_订单请求]:
        """平仓请求拆分核心逻辑"""
        拆分请求列表 = []
        剩余数量 = 请求.数量

        if 请求.方向 == 方向.做多:
            # 平空仓逻辑
            pass
        else:
            # 平多仓逻辑
            pass

        return 拆分请求列表

    def 减少冻结(self, 方向: 方向, 开平: 开平, 数量: float) -> None:
        """减少冻结持仓"""
        if 方向 == 方向.做多:
            if 开平 == 开平.平今:
                self.空今 -= 数量
            elif 开平 == 开平.平昨:
                self.空昨 -= 数量
            else:
                self.空仓 -= 数量
        else:
            if 开平 == 开平.平今:
                self.多今 -= 数量
            elif 开平 == 开平.平昨:
                self.多昨 -= 数量
            else:
                self.多仓 -= 数量