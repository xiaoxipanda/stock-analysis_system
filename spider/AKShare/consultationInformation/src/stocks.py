"""
个股信息模块
提供个股基本面、财务数据、估值等信息
"""
import akshare as ak
import pandas as pd
from tabulate import tabulate


def stock_info(symbol):
    """个股基本信息"""
    try:
        df = ak.stock_individual_info_em(symbol=symbol)
        print(f"\n个股 {symbol} 基本信息:")
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取 {symbol} 基本信息失败: {e}")
        return None


def stock_financial(symbol):
    """个股财务指标"""
    try:
        df = ak.stock_financial_analysis_indicator(symbol=symbol, start_year="2023")
        print(f"\n个股 {symbol} 财务指标:")
        cols = ["日期", "营业总收入", "净利润", "净利润同比增长率",
                "净资产收益率", "资产负债率", "每股收益", "每股净资产"]
        available_cols = [c for c in cols if c in df.columns]
        result = df[available_cols].head(10)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取 {symbol} 财务指标失败: {e}")
        return None


def stock_profit(symbol):
    """个股利润表"""
    try:
        df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        print(f"\n个股 {symbol} 利润表:")
        result = df.head(8)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取 {symbol} 利润表失败: {e}")
        return None


def stock_balance(symbol):
    """个股资产负债表"""
    try:
        df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        print(f"\n个股 {symbol} 资产负债表:")
        result = df.head(8)
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取 {symbol} 资产负债表失败: {e}")
        return None


def holders_top(symbol):
    """前十大流通股东"""
    try:
        df = ak.stock_gdfx_free_top_10_em(date="2025-03-31")
        df = df[df["代码"] == symbol]
        if df.empty:
            df = ak.stock_gdfx_free_top_10_em()
            df = df[df["代码"] == symbol]
        print(f"\n个股 {symbol} 前十大流通股东:")
        print(tabulate(df.head(10), headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取 {symbol} 股东信息失败: {e}")
        return None


def new_a_stock():
    """新股日历"""
    try:
        df = ak.stock_new_ipo_cninfo()
        print("\n新股日历:")
        print(tabulate(df.head(15), headers="keys", tablefmt="grid", showindex=False))
        return df
    except Exception as e:
        print(f"获取新股日历失败: {e}")
        return None
