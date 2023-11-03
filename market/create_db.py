from market import app, db
from market.models import items  # Import your model

# # Create a new item
new_item = items(
    name='Phoag',
    price=100,
    barcode='1234523565',
    description='This is a new ikjhgtesfnm,mgf'
)

# Add the new item to the session
with app.app_context():
    db.session.add(new_item)

    # Commit the changes to the database
    db.session.commit()
# from app import app, db
#
# # Import the models (make sure your models are properly defined in a module)
# #from app import items
#
# with app.app_context():
#     db.create_all()