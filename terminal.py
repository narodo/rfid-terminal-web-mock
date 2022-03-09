from flask import Flask, request, jsonify, json, render_template
from flask_restful import Resource, Api
from models import db,Transaction,Terminal,User
from flask_sqlalchemy import SQLAlchemy
import re
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)


trans_id = 0 

class TransactionAPI(Resource):

    def put(self, terminal):

        global trans_id

        if trans_id == 0:
            trans_id = (Transaction.query.all())[-1].id + 1
        
        new_trans = Transaction( trans_id, request.form['amount'], 
                request.form['tag'], terminal)

        user = User.query.filter_by(tag=new_trans.tag).first()
        user.balance = user.balance - float(new_trans.amount)
        print("New Transaction for user ", user.name, " - new balance", user.balance)
        
        db.session.add(new_trans)
        db.session.commit()

        trans_id = trans_id + 1


def parse_command(command_str):
    loc=re.search(r"\d", command_str).start()
    print("command_str: ", command_str, "loc: ", loc)
    return command_str[:loc], command_str[loc:]
    # return "OK", "1"
 

@app.before_first_request
def create_table():
    global trans_id
    db.create_all()

@app.route('/', methods=['GET'])
def showHome():
    if request.method == 'GET':
        return render_template('base.html')

@app.route('/users', methods=['GET'])
def showallUsers():
    users = User.query.all();
    if request.method == 'GET':
        return render_template('users.html', userlist=users)

@app.route('/transactions', methods=['GET'])
def showallTransactions():
    trans = Transaction.query.all();
    if request.method == 'GET':
        return render_template('transactions.html', translist=trans)

@app.route('/showterminal', methods=['GET', 'POST'])
def showallTerminals():
    terms = Terminal.query.all();
    if request.method == 'GET':
        return render_template('all_terminals.html', terminals=terms)

    if request.method == 'POST':
        action = list(request.form)[0] #get button name
        command, index = parse_command(action)
        print("Action: ", command, "index: ", index)

        update_term = Terminal.query.filter_by(id=index).first()
        update_term.status=command
        db.session.commit()
        return render_template('all_terminals.html', terminals=terms)

def change_status_ok():
    print("Changed status to ok")

@app.route('/showterminal/<int:term_id>')
def showTerminal(term_id):
    term =  Terminal.query.filter_by(id=term_id).first()
    return render_template('terminal.html', id=term.id, name=term.name,
            location=term.location, status=term.status, amount=term.amount )


@app.route('/terminal/<int:term_id>',methods = ['GET'])
def getTerminal(term_id):
    cur_term =  jsonify(json_list = Terminal.query.filter_by(id=term_id).first().serialize)
    return cur_term

api.add_resource(TransactionAPI, '/transaction/<int:terminal>')


app.run(host='0.0.0.0', port=8080)
