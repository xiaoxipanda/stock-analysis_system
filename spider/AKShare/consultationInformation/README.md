# AStock Info - A股资讯工具

基于 [AKShare](https://github.com/akfamily/akshare) 的命令行A股资讯查询工具。

## 快速开始

```bash
pip install -r requirements.txt
python main.py            # 查看帮助
```

## 功能模块

### 行情
| 命令 | 说明 |
|------|------|
| `python main.py index` | 主要指数实时行情 |
| `python main.py market -n 10` | A股实时行情（按涨跌幅排序） |
| `python main.py concept` | 概念板块行情 |
| `python main.py industry` | 行业板块行情 |

### 个股信息
| 命令 | 说明 |
|------|------|
| `python main.py info 000858` | 个股基本信息 |
| `python main.py finance 000858` | 财务指标 |
| `python main.py profit 000858` | 利润表 |
| `python main.py balance 000858` | 资产负债表 |
| `python main.py holders 000858` | 前十大流通股东 |
| `python main.py ipo` | 新股日历 |

### 历史K线
| 命令 | 说明 |
|------|------|
| `python main.py hist stock 000858` | 个股历史K线 |
| `python main.py hist index 000300` | 指数历史K线 |

### 资讯
| 命令 | 说明 |
|------|------|
| `python main.py news` | 财联社电报 |
| `python main.py notice` | 个股公告 |
| `python main.py report` | 个股研报 |

### 资金
| 命令 | 说明 |
|------|------|
| `python main.py north` | 北向资金流向 |
| `python main.py margin` | 融资融券 |
| `python main.py block` | 大宗交易 |
| `python main.py fund-ind` | 行业资金流向 |
| `python main.py fund-stock` | 个股资金流向 |

## 依赖

- Python >= 3.10
- akshare, pandas, tabulate
