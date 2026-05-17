"""
新闻公告模块
提供A股新闻、公告、研报等信息
"""
import akshare as ak
import pandas as pd
from tabulate import tabulate


def stock_notice(symbol="000002"):
    """个股公告"""
    try:
        df = ak.stock_notice_report(symbol=symbol)
        print(f"\n个股 {symbol} 公告:")
        print(tabulate(df.head(15), headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取公告失败: {e}")
        return None


def news_telegraph():
    """股票新闻电报"""
    try:
        df = ak.stock_news_em()
        print("\n股票新闻 (最新):")
        cols = ["新闻标题", "发布时间"]
        available = [c for c in cols if c in df.columns]
        result = df[available].head(20)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取新闻失败: {e}")
        return None


def research_report(symbol=""):
    """个股研报"""
    try:
        df = ak.stock_research_report_em(symbol="000858")
        print(f"\n研报:")
        cols = ["股票简称", "机构名称", "最新评级", "评级日期", "目标价"]
        available = [c for c in cols if c in df.columns]
        result = df[available].head(15)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取研报失败: {e}")
        return None
