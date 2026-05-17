#!/usr/bin/env python3
"""
AStock Info - A股资讯工具
基于 AKShare 的命令行A股资讯查询工具
"""
import argparse
import os
import sys
from datetime import datetime

from src.market import (
    index_spot, a_spot_top, index_history, stock_history,
    concept_board_spot, industry_board_spot,
)
from src.stocks import (
    stock_info, stock_financial, stock_profit,
    stock_balance, holders_top, new_a_stock,
)
from src.news import stock_notice, news_telegraph, research_report
from src.funds import (
    north_fund_flow, margin_trade, block_deal,
    fund_flow_industry, fund_flow_individual,
)
from src.collector import (
    collect_news_articles, collect_notice_articles, collect_report_articles,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def save_df(df, name_prefix, symbol=""):
    """保存 DataFrame 到 data/ 目录"""
    if df is None or df.empty:
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    if symbol:
        filename = f"{name_prefix}_{symbol}_{tag}.csv"
    else:
        filename = f"{name_prefix}_{tag}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"已保存: {filepath}")


def cmd_index(args):
    df = index_spot()
    if args.save:
        save_df(df, "index_spot")


def cmd_market(args):
    sort_by = args.sort or "涨跌幅"
    df = a_spot_top(n=args.n, sort_by=sort_by)
    if args.save:
        save_df(df, "market")


def cmd_concept(args):
    df = concept_board_spot()
    if args.save:
        save_df(df, "concept_board")


def cmd_industry(args):
    df = industry_board_spot()
    if args.save:
        save_df(df, "industry_board")


def cmd_stock_info(args):
    df = stock_info(args.symbol)
    if args.save:
        save_df(df, "stock_info", args.symbol)


def cmd_stock_financial(args):
    df = stock_financial(args.symbol)
    if args.save:
        save_df(df, "stock_finance", args.symbol)


def cmd_stock_profit(args):
    df = stock_profit(args.symbol)
    if args.save:
        save_df(df, "stock_profit", args.symbol)


def cmd_stock_balance(args):
    df = stock_balance(args.symbol)
    if args.save:
        save_df(df, "stock_balance", args.symbol)


def cmd_holders(args):
    df = holders_top(args.symbol)
    if args.save:
        save_df(df, "stock_holders", args.symbol)


def cmd_ipo(args):
    df = new_a_stock()
    if args.save:
        save_df(df, "ipo_calendar")


def cmd_history(args):
    if args.type == "index":
        df = index_history(symbol=args.symbol)
        if args.save:
            save_df(df, "index_hist", args.symbol)
    else:
        df = stock_history(symbol=args.symbol, adjust=args.adjust)
        if args.save:
            save_df(df, "stock_hist", args.symbol)


def cmd_news(args):
    df = news_telegraph()
    if args.save:
        save_df(df, "stock_news")


def cmd_notice(args):
    df = stock_notice(args.symbol)
    if args.save:
        save_df(df, "stock_notice", args.symbol)


def cmd_report(args):
    df = research_report()
    if args.save:
        save_df(df, "research_report")


def cmd_north(args):
    df = north_fund_flow()
    if args.save:
        save_df(df, "north_fund")


def cmd_margin(args):
    df = margin_trade()
    if args.save:
        save_df(df, "margin_trade")


def cmd_block(args):
    df = block_deal()
    if args.save:
        save_df(df, "block_deal")


def cmd_fund_industry(args):
    df = fund_flow_industry()
    if args.save:
        save_df(df, "fund_ind")


def cmd_fund_stock(args):
    df = fund_flow_individual(args.symbol)
    if args.save:
        save_df(df, "fund_stock", args.symbol)


def _add_save(subparser):
    subparser.add_argument("--save", action="store_true", help="保存结果CSV到data/目录")



def cmd_pull_news(args):
    """采集新闻文章保存为HTML"""
    collect_news_articles(max_articles=args.n)


def cmd_pull_notice(args):
    """采集公告保存为HTML"""
    collect_notice_articles(symbol=args.symbol, max_articles=args.n)


def cmd_pull_report(args):
    """采集研报保存为HTML"""
    collect_report_articles(max_articles=args.n)


def main():
    parser = argparse.ArgumentParser(
        description="AStock Info - A股资讯工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py index --save           查看指数行情并保存CSV
  python main.py market -n 10 --save    查看A股涨幅前10并保存
  python main.py info 000858 --save     查看五粮液基本信息并保存
  python main.py news --save            查看股票新闻并保存
  python main.py north --save           北向资金并保存
        """
    )

    sub = parser.add_subparsers(dest="command", help="可用命令")

    # 行情
    _add_save(sub.add_parser("index", help="主要指数实时行情"))

    p_market = sub.add_parser("market", help="A股实时行情")
    p_market.add_argument("-n", type=int, default=20, help="显示前N只 (默认20)")
    p_market.add_argument("--sort", type=str, default="涨跌幅", help="排序字段")
    _add_save(p_market)

    _add_save(sub.add_parser("concept", help="概念板块行情"))
    _add_save(sub.add_parser("industry", help="行业板块行情"))

    # 个股信息
    p_info = sub.add_parser("info", help="个股基本信息")
    p_info.add_argument("symbol", help="股票代码 (如 000858)")
    _add_save(p_info)

    p_fin = sub.add_parser("finance", help="个股财务指标")
    p_fin.add_argument("symbol", help="股票代码")
    _add_save(p_fin)

    p_profit = sub.add_parser("profit", help="个股利润表")
    p_profit.add_argument("symbol", help="股票代码")
    _add_save(p_profit)

    p_bal = sub.add_parser("balance", help="个股资产负债表")
    p_bal.add_argument("symbol", help="股票代码")
    _add_save(p_bal)

    p_holder = sub.add_parser("holders", help="前十大流通股东")
    p_holder.add_argument("symbol", help="股票代码")
    _add_save(p_holder)

    _add_save(sub.add_parser("ipo", help="新股日历"))

    # 历史行情
    p_hist = sub.add_parser("hist", help="历史行情")
    p_hist.add_argument("type", choices=["stock", "index"], help="类型")
    p_hist.add_argument("symbol", help="代码")
    p_hist.add_argument("--adjust", default="qfq", choices=["qfq", "hfq", ""], help="复权方式")
    _add_save(p_hist)

    # 新闻公告
    p_notice = sub.add_parser("notice", help="个股公告")
    p_notice.add_argument("--symbol", default="000002", help="股票代码")
    _add_save(p_notice)

    _add_save(sub.add_parser("news", help="股票新闻"))
    _add_save(sub.add_parser("report", help="研报"))

    # 资金流向
    _add_save(sub.add_parser("north", help="北向资金流向"))
    _add_save(sub.add_parser("margin", help="融资融券"))
    _add_save(sub.add_parser("block", help="大宗交易"))
    _add_save(sub.add_parser("fund-ind", help="行业资金流向"))

    p_fund = sub.add_parser("fund-stock", help="个股资金流向")
    p_fund.add_argument("symbol", nargs="?", default="all", help="股票代码")
    _add_save(p_fund)


    # 文章采集
    p_pull_news = sub.add_parser("pull-news", help="抓取新闻全文保存为HTML")
    p_pull_news.add_argument("-n", type=int, default=20, help="采集文章数 (默认20)")

    p_pull_notice = sub.add_parser("pull-notice", help="抓取公告全文保存为HTML")
    p_pull_notice.add_argument("symbol", help="股票代码")
    p_pull_notice.add_argument("-n", type=int, default=20, help="采集数量 (默认20)")

    p_pull_report = sub.add_parser("pull-report", help="保存研报为HTML")
    p_pull_report.add_argument("-n", type=int, default=10, help="采集数量 (默认10)")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    cmds = {
        "index": cmd_index,
        "market": cmd_market,
        "concept": cmd_concept,
        "industry": cmd_industry,
        "info": cmd_stock_info,
        "finance": cmd_stock_financial,
        "profit": cmd_stock_profit,
        "balance": cmd_stock_balance,
        "holders": cmd_holders,
        "ipo": cmd_ipo,
        "hist": cmd_history,
        "notice": cmd_notice,
        "news": cmd_news,
        "report": cmd_report,
        "north": cmd_north,
        "margin": cmd_margin,
        "block": cmd_block,
        "fund-ind": cmd_fund_industry,
        "fund-stock": cmd_fund_stock,
        "pull-news": cmd_pull_news,
        "pull-notice": cmd_pull_notice,
        "pull-report": cmd_pull_report,
    }

    cmds[args.command](args)


if __name__ == "__main__":
    main()
