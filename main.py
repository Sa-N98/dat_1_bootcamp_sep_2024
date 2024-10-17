from flask import Flask, render_template as rt, request, redirect, url_for
from model import *
from sqlalchemy import and_ , or_
import os


current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ \
os.path.join(current_dir,"Database.sqlite3")

db.init_app(app)
app.app_context().push() # stack in pograming


@app.route('/', methods=['GET','POST']) #192.168.0.117:5000 = /
def home():
    if request.method == "POST":
        
        Email = request.form['email']
        Password = request.form['password']

        user = users.query.filter_by(email = Email).first()
        if user:
            if Password == user.password:




                if user.user_type == "Theater":
                    relation = User_theater_relation.query.filter_by(user_id =user.id).first()
                    theater = theaters.query.filter_by(id = relation.theater_id).first()

                    if theater.status == False:
                        return "You are not verified yet"
                    return redirect(url_for("Theater_dashbord" , id=user.id))
                


                elif user.user_type == "Customer":
                    return redirect(url_for("customer_dashbord"))
                elif user.user_type == "Admin":
                    return redirect(url_for("Admin_dashbord"))
                

                return "user exists"
            else:
                return "password is wrong"
        else:
            return rt('home.html' , message = 'user dos not exist')
    return rt('home.html')


@app.route('/CustomerSignUp', methods=['GET','POST']) 
def CustomerSignUp():
    if request.method == 'POST':
         Email = request.form['email']
         Password = request.form['password']
         Username = request.form['name']
         UserType = request.form['userType']

         newUser = users(name = Username , email =  Email , password = Password, user_type=UserType) 
         db.session.add(newUser)
         db.session.commit()
         return redirect(url_for("home", message = "New User Created"))
         
    return rt('CustomerSignUp.html')


@app.route('/TheaterSignUp', methods=['GET','POST']) 
def TheaterSignUp():
    if request.method == 'POST':
         Email = request.form['email']
         Password = request.form['password']
         Username = request.form['name']
         UserType = request.form['userType']
         theater_Name=request.form['theaterName']

         newUser = users(name = Username , email =  Email , password = Password, user_type=UserType) 
         db.session.add(newUser)
         db.session.commit()

         newTheater = theaters(name = theater_Name)
         db.session.add(newTheater)
         db.session.commit()
         


         new_relation =User_theater_relation(user_id = newUser.id , theater_id=newTheater.id)
         db.session.add(new_relation)
         db.session.commit()
         




         
         






         return redirect(url_for("home", message = "New User Created"))
         
    return rt('TheaterSignUp.html')









@app.route('/CustomerDashbord', methods=['GET','POST']) 
def customer_dashbord():
    return rt('customerDashbord.html')



@app.route('/TheaterDashbord/<id>', methods=['GET','POST']) 
def Theater_dashbord(id):

    theaterdata= theaters.query.filter_by(id = id ).first()
    print( theaterdata.hosted_movies)
    return rt('ServerDashbord.html', Tid=id , movie_data = theaterdata.hosted_movies)




@app.route('/AdminDashbord', methods=['GET','POST']) 
def Admin_dashbord():
    if request.method == "POST":
        TheaterID= request.form['ID']
        theaterStatus = request.form['Status']
        get_theater = theaters.query.filter_by(id =TheaterID).first()

        if theaterStatus == 'True':
            get_theater.status =True
            db.session.commit()
        return redirect(url_for('Admin_dashbord'))




    approvals = theaters.query.filter_by(status = False).all()

    return rt('AdminDashbord.html', apvals = approvals )


@app.route('/submit_movie', methods=['GET','POST'])
def submit_movie():

    if request.method == "POST":
        movie_name = request.form['name']
        genre = request.form['genre']
        poster_url = request.form['poster']
        ticket_price = int(request.form['price'])
        available_tickets = int(request.form['tickets'])
        event_date = request.form['date']
        event_time = request.form['time']
        theaterID = request.form['theater']

        new_movie = movies(
                            name=movie_name,
                            genre=genre,
                            poster=poster_url,
                            price=ticket_price,
                            tickets=available_tickets,
                            date=event_date,
                            time=event_time
                        )
        
        db.session.add(new_movie)
        db.session.commit()

        newRelation = Movies_theater_relation(movie_id =new_movie.id ,  theater_id = theaterID)
        db.session.add(newRelation)
        db.session.commit()


        return redirect(url_for("Theater_dashbord" , id=theaterID))













@app.route('/sql', methods=['GET','POST'])
def sql():

    #basic
    # data = users.query.all()
    # print('name', 'email')
    # for i in data:
    #     print(i.name, i.email)
    
    #filters
    # data = users.query.filter(users.user_type == 'Admin').all()
    # data = users.query.filter_by(user_type = 'Admin').all()
    # data = users.query.filter( and_(users.user_type == 'Customer' , users.id % 2 == 0 )).all()
    data = users.query.filter(users.name.like('a%') ).all()
    print('lenght:', len(data))
    print('name', 'type')
    for i in data:
        print(i.id, i.name, i.user_type)


    return rt('sql.html', var = data)


@app.route('/dataflow', methods=['GET','POST'])
def dataflow():
    if request.method == "POST":
        
        Email = request.form['email']
        Password = request.form['password']
    
        print(Email)
        print(Password)

        user = users.query.filter_by(email = Email).first()
        if user:
            if Password == user.password:
                return "user exists"
            else:
                return "password is wrong"
        else:
            return " user dos not exist"

       
    return rt('dataflow.html')

if __name__ == "__main__":

    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')