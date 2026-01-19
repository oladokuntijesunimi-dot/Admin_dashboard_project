from flask import Flask, render_template, request
import db

app = Flask(__name__)

posts = db.get_posts()
parties = db.get_parties()

@app.route('/contestant', methods = ['GET', 'POST'])
def contestant():
    if request.method == 'GET':
        return render_template('contestant.html', posts = posts, parties = parties)
    else:
        fullname = request.form.get('fullname')
        age= request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('address')
        email = request.form.get('email')
        party = request.form.get('party')
        post = request.form.get('post')

        message = db.register_contestants(fullname,age,gender,party,post,address,email)
        return render_template('contestant.html',posts = posts, parties = parties, message = message)

    
@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        fullname = request.form.get('Full_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('Address')
        email = request.form.get('Email')
        phonenumber = request.form.get('Phone_number')

        message = db.register_voter(fullname, age, gender, address, phonenumber, email)
        return render_template('register.html', message = message)
    
if __name__ == '__main__':
    app.run('0.0.0.0',debug = True)