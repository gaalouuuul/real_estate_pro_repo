from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import User, Property, Room

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(first_name="Admin", last_name="User", email="admin@example.com", password_hash=generate_password_hash("admin123"), role="admin")
    owner = User(first_name="Ahmed", last_name="Owner", email="owner@example.com", password_hash=generate_password_hash("owner123"), role="owner")
    viewer = User(first_name="Sara", last_name="Viewer", email="viewer@example.com", password_hash=generate_password_hash("viewer123"), role="user")
    db.session.add_all([admin, owner, viewer])
    db.session.commit()

    prop = Property(name="Appartement central", description="Bel appartement lumineux", city="Paris", property_type="apartment", owner_id=owner.id, status="published", price=320000, surface=72)
    db.session.add(prop)
    db.session.commit()

    db.session.add_all([
        Room(name="Salon", size=22, features="balcon, lumineux", property_id=prop.id),
        Room(name="Cuisine", size=10, features="équipée", property_id=prop.id),
    ])
    db.session.commit()

print("Seed completed.")
