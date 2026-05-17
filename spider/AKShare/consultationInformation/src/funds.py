"""
资金流向模块
提供北向资金、融资融券、大宗交易等信息
"""
import akshare as ak
import pandas as pd
from tabulate import tabulate


def north_fund_flow():
    """北向资金流向（沪股通+深股通）"""
    try:
        df = ak.stock_hsgt_fund_flow_summary_em()
        north = df[df["资金方向"] == "北向"]
        print("\n北向资金流向:")
        print(tabulate(north.tail(15), headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取北向资金失败: {e}")
        return None


def margin_trade():
    """融资融券数据 - 沪市"""
    try:
        df = ak.stock_margin_sse(start_date="20250501")
        print(f"\n融资融券 (沪市):")
        print(tabulate(df.tail(15), headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取融资融券失败: {e}")
        return None


def block_deal(symbol=""):
    """大宗交易"""
    try:
        df = ak.stock_dzjy_mrmx(symbol="000858", start_date="2025-01-01", end_date="2025-12-31")
        print(f"\n大宗交易:")
        cols = ["交易日期", "证券代码", "成交价", "成交量", "成交额", "买方营业部", "卖方营业部"]
        available = [c for c in cols if c in df.columns]
        result = df[available].head(15)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取大宗交易失败: {e}")
        return None


def fund_flow_industry():
    """行业资金流向"""
    try:
        df = ak.stock_sector_fund_flow_rank(indicator="今日")
        print(f"\n行业资金流向排名:")
        cols = ["名称", "主力净流入-净额", "主力净流入-净占比",
                "超大单净流入-净额", "大单净流入-净额", "涨跌幅"]
        available = [c for c in cols if c in df.columns]
        result = df[available].head(20)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取行业资金流向失败: {e}")
        return None


def fund_flow_individual(symbol):
    """个股资金流向"""
    try:
        df = ak.stock_individual_fund_flow_rank(indicator="今日")
        if symbol and symbol != "all":
            df = df[df["代码"] == symbol]
        df = df.sort_values("主力净流入-净额", ascending=False).head(20)
        print(f"\n个股资金流向排名:")
        cols = ["代码", "名称", "最新价", "涨跌幅",
                "主力净流入-净额", "主力净流入-净占比"]
        available = [c for c in cols if c in df.columns]
        result = df[available].head(15)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取个股资金流向失败: {e}")
        return None
