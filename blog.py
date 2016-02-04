# -*- coding: utf-8 -*-
""" 使用 web.py 0.3 制作的一个简易Blog, 主要是为了练手熟悉python语法
"""
import web
import model


# 指定Url结构, 每个路径又相应的类处理
urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
)


# 创建模版对象, base参数可实现模版复用
t_global = {
    'dateStr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_global)


# 首页
class Index(object):
    def GET(self):
        posts = model.get_posts()
        return render.index(posts)


# 查看
class View(object):
    def GET(self, _id):
        post = model.get_post(int(_id))
        return render.view(post)


# 新增
class New(object):
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, size=30, description="Post title:"),
        web.form.Textarea('content', web.form.notnull, rows=30, cols=80, description="Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')


# 删除
class Delete(object):

    def POST(self, _id):
        model.del_post(int(_id))
        raise web.seeother('/')


# 编辑
class Edit(object):

    def GET(self, _id):
        post = model.get_post(int(_id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, _id):
        form = New.form()
        post = model.get_post(int(_id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(_id), form.d.title, form.d.content)
        raise web.seeother('/')


app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()