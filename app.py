from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HealthEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    health_note = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<HealthEntry {self.date}>'

@app.route('/')
def index():
    entries = HealthEntry.query.all()
    entries_data = [{'date': entry.date.isoformat(), 'title': entry.health_note} for entry in entries]
    return render_template('index.html', entries=entries_data)

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    date_str = request.args.get('date') if request.method == 'GET' else request.form['date']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    entry = HealthEntry.query.filter_by(date=date).first()

    if request.method == 'POST':
        health_note = request.form['health_note']
        if entry:
            entry.health_note = health_note  # 既存の記録を更新
        else:
            entry = HealthEntry(date=date, health_note=health_note)  # 新規記録を作成
            db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('entry.html', entry=entry, date=date_str)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # データベースとテーブルを作成する
    app.run(debug=True)
