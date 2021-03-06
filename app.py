from flask import Flask, redirect, url_for

import config

app = Flask(__name__, template_folder='./src/templates')
app.secret_key = config.Settings().SCR_KEY


def getVersion():
    return config.Settings().VERSION


app.jinja_env.globals.update(getVersion=getVersion)


with app.app_context():

    from src.auth.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from src.aluno.aluno import aluno_bp
    app.register_blueprint(aluno_bp, url_prefix='/alunos')

    from src.admin.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')


@app.route('/')
def main():
    return redirect('/alunos')


if __name__ == "__main__":
    app.run(port=config.Settings().PORT, debug=True)
