import os

from flask import Flask, render_template, g



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mech-site.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import get_db
    # a simple page that says hello
    @app.route('/')
    def home():
        if g.user is None:
            db = get_db()
            mechanics = db.execute('''
                SELECT
                    m.mechanic_id, 
                    m.name, 
                    AVG(a.review_score) AS avg_rating, 
                    m.zipcode 
                FROM 
                    mechanics m 
                LEFT JOIN 
                    appointments a ON m.mechanic_id = a.mechanic_id 
                GROUP BY 
                    m.name, m.zipcode
            ''').fetchall()
            return render_template("landing_page.html", nearby_mechanics=mechanics)
        if g.user_type == "customer":
            return render_template("customer/dash.html")
        return mechanic.mechanic_dashboard()
    
    from . import db
    db.init_app(app)
    from . import populate
    populate.init_app(app)

    from . import customer
    from . import mechanic
    from . import auth
    from . import maintence_page

    app.register_blueprint(mechanic.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(maintence_page.bp)
    

    

    for rule in app.url_map.iter_rules():
        print(rule.endpoint)


    return app

def get_bp_urls(blueprint):
    from flask import Flask
    temp_app = Flask(__name__) 
    temp_app.register_blueprint(blueprint)
    return [str(p) for p in temp_app.url_map.iter_rules()]