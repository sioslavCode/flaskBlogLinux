from flaskblog import create_app  # ovo radi jer u ta varijabla app je definirana u __init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # ovo je alternativa za terminalno pokretanje sa FLASK_DEBUG=1
