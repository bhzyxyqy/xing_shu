# 星枢量化框架

初衷：刚开始是想单纯想写一个策略，对比多个框架后选择了vnpy，他的文档很详细，但我入门还是用了较长的时间去阅读文档和看他的源码，后来考虑到我不需要使用图形化界面和想以母语中文对我后续策略开发和策略维护更友好的想法，决定以vnpy中的`examples/no_ui/run.py`为基础，进行全面中文重构。

基于vnpy框架深度中文化的量化交易解决方案，专为中文开发者打造的友好开发体验基于`vnpy 3.9.4`深度汉化的量化交易开发框架，专为中文母语开发者打造的策略研发解决方案。

## 📖 项目背景

为满足中文开发者对策略代码可读性和可维护性的需求，本项目以vnpy-3.9.4为基础，全面重构：

- **全中文命名体系**：包/模块/类/变量100%中文标识
- **深度语义对应**：保留原框架设计理念，建立精确中英术语映射
- **无缝兼容升级**：在保持功能一致性的基础上提升中文开发体验

## 🚀 核心优势

### 中文友好性

- 完全消除英文术语障碍
- API设计符合中文编程思维习惯
- 文档字符串及注释全中文化

### 架构延续性

- 完整保留vnpy的优秀架构设计
- 事件驱动引擎、主引擎等核心机制保持不变
- 渐进式重构保证功能稳定性

### 开发便捷性

- 更直观的代码导航
- 降低新人学习成本
- 提升长期维护效率

## 📂 项目结构对比

### 核心模块对照表

| 原vnpy路径                       | 星枢路径                                 |
| -------------------------------- | ---------------------------------------- |
| `vnpy/event`                     | `星枢/包_事件引擎`                       |
| `vnpy/event/__init__.py`         | `星枢/包_事件引擎/__init__.py`           |
| `vnpy/event/engine.py`           | `星枢/包_事件引擎/模块_引擎.py`          |
| `vnpy/trader`                    | `星枢/包_交易核心`                       |
| `vnpy/trader/app.py`             | `星枢/包_交易核心/模块_应用.py`          |
| `vnpy/trader/constant.py`        | `星枢/包_交易核心/模块_常数.py`          |
| `vnpy/trader/converter.py`       | `星枢/包_交易核心/模块_转换器.py`        |
| `vnpy/trader/engine.py`          | `星枢/包_交易核心/模块_主引擎.py`        |
| `vnpy/trader/event.py`           | `星枢/包_交易核心/模块_事件类型.py`      |
| `vnpy/trader/gateway.py`         | `星枢/包_交易核心/模块_网关.py`          |
| `vnpy/trader/object.py`          | `星枢/包_交易核心/模块_对象.py`          |
| `vnpy/trader/setting.py`         | `星枢/包_交易核心/模块_设置.py`          |
| `vnpy/trader/utility.py`         | `星枢/包_交易核心/模块_工具.py`          |
| `vnpy/trader/locale/__init__.py` | `星枢/包_交易核心/包_国际化/__init__.py` |

### 开发进度看板

| 模块                      | 重写进度 | 预计完成时间 |
| :------------------------ | :------- | :----------- |
| 事件引擎（原EventEngine） | ✅ 100%   | 已发布       |
| 主引擎（原MainEngine）    | ✅ 100%   | 已发布       |
| CTA自动交易模块           |          |              |
| CTP接口                   |          |              |

## 🤝 贡献指南

欢迎提交中文命名的：

- 📝 文档翻译
- 🐛 Bug修复
- 🎯 功能增强
