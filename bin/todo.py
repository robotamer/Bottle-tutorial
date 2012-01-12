import sqlite3
from bottle import route, run, debug, template, request, validate, static_file, error

dblink = 'data/todo.db'

def todolist(title, html=''):

    conn = sqlite3.connect(dblink)
    c = conn.cursor()
    c.execute("SELECT oid, task FROM todo WHERE status LIKE '1';")
    result = c.fetchall()
    c.close()
    return template('gui/todo/view', rows=result, title=title, html=html)


@route('/todo')
def todo_list():

    title='ToDo List'
    return todolist(title)

@route('/todo/new', method='GET')
def new_item():

    if request.GET.get('save','').strip():

        new = request.GET.get('task', '').strip()
        conn = sqlite3.connect(dblink)
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
        new_id = c.lastrowid

        conn.commit()
        c.close()
        body='The new task was inserted into the database, the ID is %s' % new_id
        return todolist('ToDo List Saved',body)
    else:
        return todolist('ToDo List')

@route('/todo/edit/:no', method='GET')
@validate(no=int)
def edit_item(no):

    if request.GET.get('save','').strip():
        edit = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect(dblink)
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE oid LIKE ?", (edit,status,no))
        conn.commit()
        body = 'The item number %s was successfully updated' %no
        return todolist('ToDo List Updated',body)

    else:
        conn = sqlite3.connect(dblink)
        c = conn.cursor()
        sql = 'SELECT task FROM todo WHERE oid LIKE %s' %no
        c.execute(sql)
        cur_data = c.fetchone()
        body = template('gui/todo/edit', old = cur_data, no = no)
        return todolist('ToDo List Edit',body)



@route('/todo/json:json#[1-9]+#')
def show_json(json):

    conn = sqlite3.connect(blink)
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE oid LIKE ?", (json))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task':'This item number does not exist!'}
    else:
        return {'Task': result[0]}
