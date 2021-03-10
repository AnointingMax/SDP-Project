import os
import secrets
import json
from datetime import datetime

from flask import jsonify, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from Backend import app, bcrypt, db, ma
from Backend.models import Person, User, Worker, Address, UserSchema, WorkerSchema, AddressSchema, WorkLog, TaskSchema


@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify(message= "asfwefwsdfc")

@app.route('/user/login', methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')
     
    user = User.query.filter(User.email == email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=remember)
        return jsonify(message = "logged in user")
    else:
        return jsonify(message = "wrong login credentials")
    

@app.route('/user/register', methods=["POST"])
def register():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    location = request.form.get('location')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    
    hashpw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(fname=fname, lname=lname, location=location,
                phone=phone, email=email, password=hashpw)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(message = "registered")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "integrity error")
    

@app.route('/user/updateuserprofile', methods=["POST"])
@login_required
def updateuserprofile():
    current_user.fname = request.form.get('fname')
    current_user.lname = request.form.get('lname')
    current_user.location = request.form.get('location')
    current_user.phone = request.form.get('phone')
    current_user.email = request.form.get('email')
    try:
        db.session.commit()
        return jsonify(message = "updated user info successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "integrity error update")
    

@app.route('/user/addnewaddress', methods=["POST"])
@login_required
def addnewaddress():
    address = request.form.get('address')
    city = request.form.get('city')
    landmark = request.form.get('landmark')
    add1 = Address(address=address, city=city, landmark=landmark, user_id=current_user.id)
    db.session.add(add1)
    try:
        db.session.commit()
        return jsonify(message = "added address successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "integrity error update")
    

@app.route('/user/getuseraddresses', methods=["GET"])
@login_required
def getuseraddresses():
    addresses = Address.query.filter_by(user=current_user).all()
    schema = AddressSchema(many=True)
    output = schema.dump(addresses)
    return jsonify(addresses = output)


@app.route('/user/getparticularaddress/<int:address_id>', methods=["GET"])
@login_required
def getparticularaddress(address_id):
    address = Address.query.get_or_404(address_id)
    if address.user != current_user:
        abort(403)
    schema = AddressSchema()
    output = schema.dump(address)
    return jsonify(address = output)


@app.route('/user/updateparticularaddress/<int:address_id>', methods=["POST"])
@login_required
def updateparticularaddress(address_id):
    address = request.form.get('address')
    city = request.form.get('city')
    landmark = request.form.get('landmark')

    add = Address.query.get_or_404(address_id)
    add.address = address
    add.city = city
    add.landmark = landmark
    
    try:
        db.session.commit()
        return jsonify(message = "updated address successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "integrity error update")


@app.route('/user/deleteparticularaddress/<int:address_id>', methods=["DELETE"])
@login_required
def deleteparticularaddress(address_id):
    address = Address.query.get_or_404(address_id)
    if address.user != current_user:
        abort(403)
    db.session.delete(address)
    db.session.commit()
    return jsonify(message = "deleted address successfully")


@app.route('/user/createtask', methods=["POST"])
@login_required
def createtask():
    address = request.form.get('address')
    duration = request.form.get('duration')
    description = request.form.get('description')
    date = datetime.fromtimestamp(int(request.form.get('date'))/1000)
    task = WorkLog(address_id=address, user_id=current_user.id, worker_id=1, duration=duration, description=description, date=date)
    db.session.add(task)
    try:
        db.session.commit()
        return jsonify(message = "added task successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "integrity error update")


@app.route('/user/getusertasks', methods=["GET"])
@login_required
def getusertasks():
    tasks = WorkLog.query.filter_by(taskee=current_user).all()
    schema = TaskSchema(many=True,)
    output = schema.dump(tasks)
    return jsonify(tasks = output)


@app.route('/user/gettaskinfo/<int:task_id>', methods=["GET"])
@login_required
def gettaskinfo(task_id):
    task = WorkLog.query.get_or_404(task_id)
    # check if the taskee is the current user else abort
    if task.taskee != current_user:
        abort(403)
    #instantiate schemas
    taskschema = TaskSchema()
    #dump them into schema
    output = taskschema.dump(task)
    return jsonify(task = output)


@app.route('/user/editparticulartask/<int:task_id>', methods=["POST"])
@login_required
def updateparticulartask(task_id):
    address = request.form.get('address')
    duration = request.form.get('duration')
    description = request.form.get('description')
    date = request.form.get('date')

    task = WorkLog.query.get_or_404(task_id)
    task.address = address
    task.duration = duration
    task.description = description
    task.date = date
    
    try:
        db.session.commit()
        return jsonify(message = "updated task successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "integrity error update")


@app.route('/user/accepttask/<int:task_id>', methods=["GET"])
@login_required
def accepttask(task_id):
    task = WorkLog.query.get_or_404(task_id)
    task.accepted = True
    
    try:
        db.session.commit()
        return jsonify(message = "updated address successfully")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "error")


@app.route('/user/getworkersbyjob/<string:job>/<int:page>', methods=["GET"])
@login_required
def getworkersbyjob(job,page):
    workers = Worker.query.filter_by(job=job, active=True, available=True).paginate(per_page=7,page=page)
    workerschema = WorkerSchema(many=True, exclude=['password', 'location', 'type', 'email', 'phone', 'active', 'available'])
    #dump them into schema
    output = workerschema.dump(workers.items)
    return jsonify(workers = output)


@app.route('/user/logout', methods=["GET"])
def logout():
    logout_user()
    return jsonify(message = "user logged out")


@app.route('/user/addworker', methods=["GET"])
def addworker():    
    passwd = bcrypt.generate_password_hash('password').decode('utf-8')

    work = Worker(fname='Daniel', lname='Iheonu', phone='08012345678', email='daniel@mail.com', location='Aba', password=passwd, job='Carpenter')
    work1 = Worker(fname='David', lname='Iheonu', phone='08098765432', email='david@mail.com', location='Aba', password=passwd, job='Carpenter')
    work2 = Worker(fname='Maxwell', lname='Ogalabu', phone='08126897683', email='maxwell@mail.com', location='Aba', password=passwd, job='Barber')
    work3 = Worker(fname='Temi', lname='Dimowo', phone='08078965412', email='temi@mail.com', location='Aba', password=passwd, job='Carpenter')
    work4 = Worker(fname='Ify', lname='Ogalabu', phone='08198765432', email='ify@mail.com', location='Aba', password=passwd, job='Gardener')
    work5 = Worker(fname='Carey', lname='Ifode', phone='08112345678', email='carey@mail.com', location='Aba', password=passwd, job='Gardener')

    try:
        db.session.add(work)
        db.session.add(work1)
        db.session.add(work2)
        db.session.add(work3)
        db.session.add(work4)
        db.session.add(work5)
        db.session.commit()
        return jsonify(message = "workers added")
    except IntegrityError:
        db.session.rollback()
        return jsonify(message = "integrity error")
