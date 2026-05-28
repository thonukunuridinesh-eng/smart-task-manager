from app import create_app, db

app = create_app()

# Add this block to create tables in the cloud database automatically
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
