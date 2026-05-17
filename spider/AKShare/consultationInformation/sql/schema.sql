-- ============================================================
-- AStock Info - A股资讯数据库表结构
-- 数据库: MySQL 8.0+
-- ============================================================

CREATE DATABASE IF NOT EXISTS astock_info
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE astock_info;

-- ============================================================
-- 1. 新闻电报表 (stock_news_em)
-- 来源: ak.stock_news_em()
-- ============================================================
CREATE TABLE IF NOT EXISTS stock_news (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT  COMMENT '主键',
    keyword     VARCHAR(32)     NOT NULL DEFAULT ''       COMMENT '关联关键词/股票代码',
    title       VARCHAR(512)    NOT NULL                  COMMENT '新闻标题',
    content     TEXT                                     COMMENT '新闻摘要/内容',
    pub_time    DATETIME        NOT NULL                  COMMENT '发布时间',
    source      VARCHAR(128)    NOT NULL DEFAULT ''       COMMENT '文章来源',
    url         VARCHAR(1024)   NOT NULL DEFAULT ''       COMMENT '新闻链接',
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间',
    PRIMARY KEY (id),
    INDEX idx_pub_time (pub_time),
    INDEX idx_keyword  (keyword),
    INDEX idx_source   (source),
    UNIQUE INDEX uk_url (url(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='A股新闻电报';

-- ============================================================
-- 2. 个股公告表 (stock_notice_report)
-- 来源: ak.stock_notice_report(symbol)
-- ============================================================
CREATE TABLE IF NOT EXISTS stock_notice (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT  COMMENT '主键',
    symbol      VARCHAR(16)     NOT NULL                  COMMENT '股票代码',
    title       VARCHAR(512)    NOT NULL                  COMMENT '公告标题',
    pub_time    DATETIME        NOT NULL                  COMMENT '公告时间',
    notice_type VARCHAR(64)     NOT NULL DEFAULT ''       COMMENT '公告类型',
    url         VARCHAR(1024)   NOT NULL DEFAULT ''       COMMENT '公告链接',
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间',
    PRIMARY KEY (id),
    INDEX idx_symbol   (symbol),
    INDEX idx_pub_time (pub_time),
    UNIQUE INDEX uk_symbol_url (symbol, url(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='个股公告';

-- ============================================================
-- 3. 研报表 (stock_research_report_em)
-- 来源: ak.stock_research_report_em(symbol)
-- ============================================================
CREATE TABLE IF NOT EXISTS stock_report (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT  COMMENT '主键',
    stock_name      VARCHAR(64)     NOT NULL                  COMMENT '股票简称',
    symbol          VARCHAR(16)     NOT NULL DEFAULT ''       COMMENT '股票代码',
    org_name        VARCHAR(128)    NOT NULL                  COMMENT '机构名称',
    rating          VARCHAR(64)     NOT NULL DEFAULT ''       COMMENT '最新评级',
    rating_change   VARCHAR(64)     NOT NULL DEFAULT ''       COMMENT '评级变动',
    rating_date     DATE            NOT NULL                  COMMENT '评级日期',
    target_price    DECIMAL(12,3)            DEFAULT NULL     COMMENT '目标价(元)',
    analyst         VARCHAR(64)     NOT NULL DEFAULT ''       COMMENT '分析师',
    title           VARCHAR(512)    NOT NULL DEFAULT ''       COMMENT '研报标题',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间',
    PRIMARY KEY (id),
    INDEX idx_symbol       (symbol),
    INDEX idx_org_name     (org_name),
    INDEX idx_rating_date  (rating_date),
    UNIQUE INDEX uk_report (stock_name, org_name, rating_date, title(100))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='个股研报';
