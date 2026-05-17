"""
市场行情与指数模块
提供大盘指数、板块、个股实时行情及历史数据
"""
import akshare as ak
import pandas as pd
from tabulate import tabulate


def index_spot():
    """获取主要指数实时行情（上证、深证、创业板、科创50等）"""
    df = ak.stock_zh_index_spot_em()
    df = df.rename(columns={
        "名称": "名称", "最新价": "最新价", "涨跌幅": "涨跌幅",
        "涨跌额": "涨跌额", "成交量": "成交量", "成交额": "成交额",
        "今开": "今开", "最高": "最高", "最低": "最低",
        "昨收": "昨收",
    })
    cols = ["名称", "最新价", "涨跌幅", "涨跌额", "成交量", "成交额"]
    result = df[cols].head(20)
    print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
    return df


def a_spot_top(n=20, sort_by="涨跌幅"):
    """A股实时行情，按涨跌幅/成交额排序"""
    df = ak.stock_zh_a_spot_em()
    col_map = {
        "代码": "代码", "名称": "名称", "最新价": "最新价",
        "涨跌幅": "涨跌幅", "涨跌额": "涨跌额", "成交量": "成交量",
        "成交额": "成交额", "换手率": "换手率", "市盈率-动态": "市盈率",
        "量比": "量比",
    }
    df = df.rename(columns=col_map)
    if sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=False)
    cols = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "成交额", "换手率"]
    result = df[cols].head(n)
    print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
    return df


def index_history(symbol="000300", period="daily"):
    """获取指数历史行情，symbol 如: 000300(沪深300) 000001(上证) 399001(深证)"""
    df = ak.stock_zh_index_daily_em(symbol=symbol)
    print(f"\n指数 {symbol} 最近交易数据:")
    cols = ["date", "open", "close", "high", "low", "volume"]
    print(tabulate(df[cols].tail(10), headers="keys", tablefmt="grid", showindex=False))
    return df


def stock_history(symbol, period="daily", adjust="qfq"):
    """获取个股历史行情，默认前复权"""
    df = ak.stock_zh_a_hist(symbol=symbol, period=period, adjust=adjust)
    cols = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "涨跌幅"]
    result = df[cols].tail(15)
    print(f"\n个股 {symbol} 最近交易数据:")
    print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
    return df


def concept_board_spot():
    """概念板块行情"""
    df = ak.stock_board_concept_spot_em()
    cols = ["板块名称", "最新价", "涨跌幅", "总市值", "换手率", "上涨家数", "下跌家数"]
    result = df[cols].head(20)
    print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
    return df


def industry_board_spot():
    """行业板块行情"""
    df = ak.stock_board_industry_spot_em()
    cols = ["板块名称", "最新价", "涨跌幅", "总市值", "换手率", "上涨家数", "下跌家数"]
    result = df[cols].head(20)
    print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
    return df
