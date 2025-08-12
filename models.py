from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Item(db.Model):
    """
    Generic item model that can be customized for different applications
    
    This class represents a database table with columns defined below.
    It can be used as a foundation for various types of items in different applications.
    Examples: Blog posts, products, tasks, etc.
    """
    # Primary key column - unique identifier for each item
    id = db.Column(db.Integer, primary_key=True)
    
    # Title column - required field (nullable=False)
    # Limited to 100 characters to prevent overly long titles
    title = db.Column(db.String(100), nullable=False)
    
    # Description column - optional field (nullable=True by default)
    # Text type has no character limit, suitable for longer content
    description = db.Column(db.Text, nullable=True)
    
    # Timestamp for when the item was created
    # Automatically set to current UTC time when item is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        Define string representation of Item objects
        
        This helps with debugging by providing a readable format when
        printing Item objects or viewing them in interactive sessions
        """
        return f'<Item {self.id}: {self.title}>'