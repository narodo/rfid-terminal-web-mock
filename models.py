from flask_sqlalchemy import SQLAlchemy
 
db =SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    balance = db.Column(db.Float())
    tag = db.Column(db.Integer()) 
 
    def __init__(self, id, name, balance, tag):
        self.id = id
        self.name = name
        self.balance = balance
        self.tag = tag
 
    def __repr__(self):
        return f"{self.id}:{self.name}:{self.balance}:{self.tag}"
 
class Transaction(db.Model):
    __tablename__ = "trans"
 
    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Float())
    tag = db.Column(db.Integer()) 
    terminal = db.Column(db.Integer()) 
 
    def __init__(self, id, amount, tag, terminal):
        self.id = id
        self.amount = amount
        self.tag = tag
        self.terminal = terminal
 
    def __repr__(self):
        return f"{self.id}:{self.amount}:{self.tag}:{self.terminal}"

class Terminal(db.Model):
    __tablename__ = "terminal"

    id = db.Column(db.Integer(), primary_key=True)
    location = db.Column(db.String())
    status = db.Column(db.String())
    name = db.Column(db.String())
    amount = db.Column(db.Float())

    def __init__(self, id, location, status, name,  amount):
        self.id = id
        self.location = location
        self.status = status
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f"{self.id}:{self.location}:{self.status}:{self.name}:{self.amount}"

    @property
    def serialize(self):
        return {
                'id' : self.id,
                'location' : self.location,
                'status' : self.status,
                'name' : self.name,
                'amount' : self.amount
        }
