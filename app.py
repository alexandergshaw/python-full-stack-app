from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Item  # Import our database and Item model

# Initialize the Flask application
app = Flask(__name__)

# Basic configuration
app.config.update(
    SECRET_KEY='change-this-key',
    SQLALCHEMY_DATABASE_URI='sqlite:///data.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Initialize the SQLAlchemy database with our app
db.init_app(app)

# Define route for the home page
@app.route('/')
def index():
    """
    Route handler for the home page.
    Fetches all tasks from the database and passes them to the template.
    """
    # Query all tasks from the database
    items = Item.query.all()
    # Render the index.html template, passing tasks to the template
    return render_template('index.html', items=items)

# Define route for creating a new task
@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    Route handler for creating a new task.
    GET: Display the create task form.
    POST: Process the form data and create a new task.
    """
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create new item from form data
        new_item = Item(
            title=request.form['title'],
            description=request.form['description']
        )
        # Add the new task to the database session
        db.session.add(new_item)
        # Commit the changes to the database
        db.session.commit()
        
        # Flash a success message
        flash('Created successfully!', 'success')
        # Redirect to the home page
        return redirect(url_for('index'))
    
    # For GET requests, render the create task form
    return render_template('create.html')

# Define route for editing an existing task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """
    Route handler for editing a task.
    GET: Display the edit task form with current task data.
    POST: Process the form data and update the task.
    
    Args:
        id (int): The ID of the task to edit
    """
    # Query the task by ID, return 404 if not found
    item = Item.query.get_or_404(id)
    
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Update task with form data
        item.title = request.form['title']
        item.description = request.form['description']
        # Commit the changes to the database
        db.session.commit()
        
        # Flash a success message
        flash('Updated successfully!', 'success')
        # Redirect to the home page
        return redirect(url_for('index'))
    
    # For GET requests, render the edit form with the task data
    return render_template('edit.html', item=item)

# Define route for deleting a task
@app.route('/delete/<int:id>')
def delete(id):
    """
    Route handler for deleting a task.
    
    Args:
        id (int): The ID of the task to delete
    """
    # Query the task by ID, return 404 if not found
    item = Item.query.get_or_404(id)
    
    # Delete the task from the database session
    db.session.delete(item)
    # Commit the changes to the database
    db.session.commit()
    
    # Flash a success message
    flash('Deleted successfully!', 'success')
    # Redirect to the home page
    return redirect(url_for('index'))

# Run the application if this file is executed directly
if __name__ == '__main__':
    # Create all database tables within the application context
    with app.app_context():
        db.create_all()
    
    # Run the Flask development server with debug mode enabled
    app.run(debug=True)