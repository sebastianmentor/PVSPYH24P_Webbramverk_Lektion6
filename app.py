from flask import Flask, render_template, request
from flask_migrate import Migrate, upgrade

from models import db, seed_users, User, UserType


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/FunUsers'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)



@app.route("/")
def startpage():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/users")
def users():
    sort_order = request.args.get('sort_order', 'asc')
    sort_column = request.args.get('sort_column', 'id')
    search_word = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    user_type = request.args.get('user_type', 0, type=int)

    search_users = User.query.filter(
        User.name.like("%"+ search_word + "%") |
        User.address.like("%"+ search_word + "%") |
        User.email.like("%"+ search_word + "%")
    )

    if user_type != 0:
        search_users = search_users.filter_by(user_type=user_type)

    order_by = User.id
    if sort_column == "name":
        order_by = User.name
    elif sort_column == "address":
        order_by = User.address
    elif sort_column == "email":
        order_by = User.email
    elif sort_column == 'type':
        order_by = User.user_type

    order_by = order_by.asc() if sort_order=='asc' else order_by.desc()

    all_users = search_users.order_by(order_by)


    pagination_object = all_users.paginate(page=page, per_page=20, max_per_page=20, error_out=True)
    
    return render_template(
        "users.html", 
        all_users=pagination_object.items, 
        has_prev = pagination_object.has_prev,
        has_next = pagination_object.has_next,
        pages = pagination_object.pages,
        iter_pages = pagination_object.iter_pages,
        sort_column=sort_column,
        sort_order=sort_order,
        page=page,
        q=search_word,
        user_type_list=list(UserType),
        user_type=user_type)


@app.route('/user/<int:user_id>')
def user(user_id):
    a_user = User.query.filter_by(id=user_id).first()
    return render_template('user.html', a_user=a_user)

if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seed_users(db)
    app.run(debug=True)