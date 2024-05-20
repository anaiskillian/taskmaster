from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   # Flask constructor
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
# A decorator used to tell the application 
# which URL is associated function 

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])       
def index():
    
    if request.method == 'POST':
        # we create a variable here to represent the form content (form is )
        # request here is just an object from which we call form, 
        # and then we just pass in the id of the input that we want to get the contents of
        # and that id was just called content since from our form action, we did input type name = "content"
        task_content = request.form['content']
        # next we create a todo object from the class Todo object we set up
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            # then we commit this to our database
            db.session.commit()
            # then we redirect to our index page
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        #this is how we display all of the current tasks in the table
        # so when we do for task in tasks in the html file, what we are doing
        # is going through each task in this Todo object
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    # what get_or_404 does is it tries to get that query with that id or it 404s 
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        # WHAT THIS LINE BELOW DOES is it grabs the request.form input (which is the content)
        # and updates the task.content part of the task variable
        task.content = request.form['content']

        try:
            db.session.commit()
            # what this does is after we commit our new changes, we redirect back to the home page
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task)

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)