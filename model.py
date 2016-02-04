# -*- coding: utf-8 -*-
import web
import datetime

# dbn用于指定数据库类型
db = web.database(dbn='mysql', db='SummerRC', user='root', pw='SummerRC')


# DESC降序
def get_posts():
    return db.select('entries', order='id DESC')


# 查询
def get_post(_id):
    try:
        return db.select('entries', where='id=$_id', vars=locals())[0]
    except IndexError:
        return None


# 插入
def new_post(title, text):
    db.insert('entries', title=title, content=text, posted_on=datetime.datetime.utcnow())


# 删除
def del_post(_id):
    db.delete('entries', where="id=$_id", vars=locals())


# 更新
def update_post(_id, title, text):
    db.update('entries', where="id=$_id", vars=locals(), title=title, content=text)