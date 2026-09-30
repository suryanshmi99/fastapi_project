# # Pydantic (Client data)
# class X(BaseModel):
#     field: type

# # SQLAlchemy (Database table)
# class X(Base):
#     __tablename__ = "..."
#     field = Column(type)

# # CREATE
# db.add(obj)
# db.commit()
# db.refresh(obj)

# # UPDATE
# existing = db.query(Model).filter(Model.id == id).first()
# existing.field = naya_value
# db.commit()
# db.refresh(existing)