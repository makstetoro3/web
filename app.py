from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.bread import Bread
from data.cake import Cake
from data.comment import Comment
from data.cake_type import Ctype
from data.bread_type import Btype
from data.users import User
from forms.user import RegisterForm
from forms.loginform import LoginForm
from forms.comments import CommentsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/comments')
def comment():
    db_sess = db_session.create_session()
    comments = db_sess.query(Comment).all()
    add_btn = False
    if current_user.is_authenticated:
        try:
            a = db_sess.query(Comment).filter(Comment.user_id == current_user.id)[0]
        except IndexError:
            add_btn = True
    return render_template("comments.html", comments=comments, add_btn=add_btn)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/cat_cake')
def cake():
    db_sess = db_session.create_session()
    types = db_sess.query(Ctype).all()
    cata = dict()
    for j in types:
        cata[j.id] = db_sess.query(Cake).filter(Cake.type_id == j.id)
    return render_template("catalog.html", types=types, dictionary=cata)


@app.route('/cat_bread')
def bread():
    db_sess = db_session.create_session()
    types = db_sess.query(Btype).all()
    cata = dict()
    for j in types:
        cata[j.id] = db_sess.query(Bread).filter(Bread.type_id == j.id)
    return render_template("catalog.html", types=types, dictionary=cata)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = CommentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Comment()
        news.title = form.title.data
        news.content = form.content.data
        current_user.comment.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/comments')
    return render_template('repcomment.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = CommentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Comment).filter(Comment.id == id,
                                             Comment.user == current_user
                                             ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Comment).filter(Comment.id == id,
                                             Comment.user == current_user
                                             ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            db_sess.commit()
            return redirect('/comments')
        else:
            abort(404)
    return render_template('repcomment.html',
                           title='Редактирование отзова',
                           form=form
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Comment).filter(Comment.id == id,
                                         Comment.user == current_user
                                         ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/comments')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
