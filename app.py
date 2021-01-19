from flask import Flask, render_template, url_for,request, redirect, flash
from flask_mysqldb import MySQL


app= Flask(__name__)
app.secret_key= "Hello_Sajeeb"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todo'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tasks ORDER BY id DESC')
    all_data = cur.fetchall()
    mysql.connection.commit()
    return render_template('index.html', all_data=all_data)

@app.route('/submit_form', methods=['POST'])
def submitted_form():
    if request.method=='POST':
        task =request.form['task']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tasks (task) VALUES (%s)',[task])
        mysql.connection.commit()
        flash("Your task Successfully Saved.")
        return redirect('/')
    else:
        return 'Data is not Submitted.'

@app.route('/delete/<string:task_id>')
def delete(task_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s',[task_id])
    mysql.connection.commit()
    flash('Task Deleted Successfully.')
    return redirect('/')


@app.route('/edit/<string:task_id>')
def edit_view(task_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tasks WHERE id=%s',[task_id])
    data = cur.fetchone()
    mysql.connection.commit()
    return render_template('edit.html',data=data)

@app.route('/update_task', methods=['POST'])
def update():
    task_id = request.form['task_id']
    task_title = request.form['task_name']

    cur = mysql.connection.cursor()
    cur.execute('UPDATE tasks SET task=%s WHERE id=%s',[task_title,task_id])
    mysql.connection.commit()
    flash('Task Updated Successfully.')
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)
