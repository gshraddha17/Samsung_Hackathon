from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

@app.route('/')
def home():
    # Retrieve all projects from the database
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/submit_idea', methods=['GET', 'POST'])
def submit_project():
    if request.method == 'POST':
        # Process the submitted project here and store it in the database
        project_name = request.form['name']
        project_description = request.form['description']
        new_project = Project(name=project_name, description=project_description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('submit_idea.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
