from sqlalchemy.orm import Session
from app.models.address import Address


def check_duplicate_address(db: Session, data):

    return db.query(Address).filter(
        Address.name == data.name,
        Address.latitude == data.latitude,
        Address.longitude == data.longitude
    ).first()


def create_address(db: Session, data):

    existing = check_duplicate_address(db, data)

    if existing:
        return None

    address = Address(**data.dict())

    db.add(address)
    db.commit()
    db.refresh(address)

    return address


def get_address(db: Session, address_id: int):

    return db.query(Address).filter(Address.id == address_id).first()


def update_address(db: Session, address_id: int, update_data):

    address = get_address(db, address_id)

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)

    return address


def delete_address(db: Session, address_id: int):

    address = get_address(db, address_id)

    db.delete(address)
    db.commit()

    return address