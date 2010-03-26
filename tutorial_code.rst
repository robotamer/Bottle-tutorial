Complete Example Listing
=========================

As the ToDo list example was developed piece by piece, here is the complete listing:

Main code for the application ``todo.py``:

::

    #!Python
    import sqlite3
    from bottle import route, run, debug, template, request, validate, send_file, error

    # only needed when you run Bottle on mod_wsgi
    from bottle import default_app
        
    @route('/todo')
    def todo_list():
        
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT id, task FROM todo WHERE status LIKE '1';")
        result = c.fetchall()
        c.close()
            
        output = template('make_table', rows=result)
        return output

    @route('/new', method='GET')
    def new_item():

        if request.GET.get('save','').strip():
            
            new = request.GET.get('task', '').strip()
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            
            query = "INSERT INTO todo (task,status) VALUES ('%s',1)" %new
            c.execute(query)
            conn.commit()
            
            c.execute("SELECT last_insert_rowid()")
            new_id = c.fetchone()[0]
            c.close 
      
            return '<p>The new task was inserted into the database, the ID is %s</p>' %new_id
        
        else:
            return template('new_task.tpl')
            
    @route('/edit/:no', method='GET')
    @validate(no=int)
    def edit_item(no):

        if request.GET.get('save','').strip():
            edit = request.GET.get('task','').strip()
            status = request.GET.get('status','').strip()
            
            if status == 'open':
                status = 1
            else:
                status = 0
                
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            query = "UPDATE todo SET task = '%s', status = '%s' WHERE id LIKE '%s'" % (edit,status,no)
            c.execute(query)
            conn.commit()
            
            return '<p>The item number %s was successfully updated</p>' %no
            
        else:
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            query = "SELECT task FROM todo WHERE id LIKE '%s'" %no
            c.execute(query)
            cur_data = c.fetchone()
            print cur_data
            
            return template('edit_task', old = cur_data, no = no)
            
    @route('/item:item#[1-9]+#')
    def show_item(item):
    
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE '%s'" %item)
        result = c.fetchall()
        c.close()
            
        if not result:
            return 'This item number does not exist!'
        else:
            return 'Task: %s' %result[0]
            
    @route('/help')
    def help():

        send_file('help.html')

    @route('/json:json#[1-9]+#')
    def show_json(json):
    
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE '%s'" %item)
        result = c.fetchall()
        c.close()
            
        if not result:
            return {'task':'This item number does not exist!'}
        else:
            return {'Task': result[0]}

    @error(403)
    def mistake403(code):
        return 'There is a mistake in your url!'

    @error(404)
    def mistake404(code):
        return 'Sorry, this page does not exist!'


    debug(True)      
    run(reloader=True)
    #remember to remove reloader=True and debug(True) when you move your application from development to a productive environment.
    
Template ``make_table.tpl``:

::

    #!html
    %#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
    <p>The open items are as follows:</p>
    <table border="1">
    %for row in rows:
      <tr>
      %for r in row:
        <td>{{r}}</td>
      %end
      </tr>
    %end
    </table>

Template ``edit_task.tpl``:

::

    #!html
    %#template for editing a task
    %#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
    <p>Edit the task with ID = {{no}}</p>
    <form action="/edit/{{no}}" method="get">
    <input type="text" name="task" value="{{old[0]}}" size="100" maxlength="100">
    <select name="status">
    <option>open</option>
    <option>closed</option>
    </select>
    <br/>
    <input type="submit" name="save" value="save">
    </form>
    
Template ``new_task.tpl``:

::

    #!html
    %#template for the form for a new task
    <p>Add a new task to the ToDo list:</p>
    <form action="/new" method="GET">
    <input type="text" size="100" maxlenght="100" name="task">
    <input type="submit" name="save" value="save">
    </form>

