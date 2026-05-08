# -*- coding: utf-8 -*-
# File: database.py
# Created: 2026-05-08 22:28
# Author: zhuimeng
# Description: 数据库模块

import sqlite3
import os


class DataBase:
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path if file_path else "./BlankSlate.db"
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.isdir(self.file_path):
            os.makedirs(dir_path, exist_ok=True)

        if not os.path.exists(self.file_path):
            # 文件不存在，需要先初始化表结构
            try:
                self.init_db()
            except Exception as e:
                print(f"意外错误: {e}")
                raise

    def get_connect(self):
        conn = sqlite3.connect(self.file_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys =ON;")
        return conn

    def init_db(self):
        with self.get_connect() as conn:
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS knowledge(
                            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 知识库编号
                            title TEXT, -- 知识库标题
                            describe TEXT, -- 知识点概要
                            content TEXT -- 知识点内容
                            );

                        CREATE TABLE IF NOT EXISTS stu_info(
                            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 学生编号
                            name VARCHAR(10) NOT NULL,  -- 学生姓名
                            comment TEXT -- 备注
                            );

                        CREATE TABLE IF NOT EXISTS session(
                            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 会话编号
                            stu_id INTEGER NOT NULL, -- 学生编号
                            know_id INTEGER NOT NULL, -- 知识点编号
                            title TEXT NOT NULL, -- 会话标题
                            score INTEGER, -- 评分
                            FOREIGN KEY (stu_id) REFERENCES stu_info(id),
                            FOREIGN KEY (know_id) REFERENCES knowledge(id)
                            );

                        CREATE TABLE IF NOT EXISTS chat(
                            id VARCHAR(128) PRIMARY KEY, -- 对话编号
                            session_id INTEGER NOT NULL,  -- 会话编号
                            reasoning_content TEXT, -- 推理内容
                            content TEXT, -- 对话内容
                            tools TEXT, -- 工具调用(JSON 字符串)
                            FOREIGN KEY (session_id) REFERENCES session(id)
                            );
                       
                        CREATE TABLE IF NOT EXISTS model_knowledge(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 知识库编号
                            chat_id VARCHAR(128) NOT NULL,  -- 对话编号
                            title TEXT NOT NULL, -- 标题
                            describe TEXT NOT NULL, -- 概要
                            content TEXT NOT NULL, -- 正文
                            comment TEXT, -- 备注(主要用来记录错误)
                            FOREIGN KEY (chat_id) REFERENCES chat(id)
                            );

                        CREATE TABLE IF NOT EXISTS model_evaluation(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 评价编号
                            chat_id VARCHAR(128) NOT NULL, -- 对话编号
                            evaluation TEXT NOT NULL, --  模型评价
                            comment TEXT, -- 备注(可以存储评分)
                            FOREIGN KEY (chat_id) REFERENCES chat(id)
                            );
                        """)
            conn.commit()
