from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging

from app.db import get_db
from app.models import schema
from app.models.address import Address
from app import crud
from app.utils.distance import calculate_distance

router = APIRouter(prefix="/addresses", tags=["Addresses"])

logger = logging.getLogger(__name__)


# CREATE ADDRESS
@router.post("/")
def create_address(address: schema.AddressCreate, db: Session = Depends(get_db)):

    logger.info("Creating address")

    new_address = crud.create_address(db, address)

    if not new_address:
        raise HTTPException(
            status_code=400,
            detail="Address already exists"
        )

    return {
        "message": "Address created successfully",
        "data": schema.AddressResponse.model_validate(new_address)
    }


# UPDATE ADDRESS
@router.put("/{address_id}")
def update_address(address_id: int, update: schema.AddressUpdate, db: Session = Depends(get_db)):

    address = crud.get_address(db, address_id)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    duplicate = db.query(Address).filter(
        Address.name == update.name,
        Address.latitude == update.latitude,
        Address.longitude == update.longitude,
        Address.id != address_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Another address with same details already exists"
        )

    updated_address = crud.update_address(db, address_id, update)

    return {
        "message": "Address updated successfully",
        "data": schema.AddressResponse.model_validate(updated_address)
    }


# DELETE ADDRESS
@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):

    address = crud.get_address(db, address_id)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    crud.delete_address(db, address_id)

    return {
        "message": "Address deleted successfully"
    }


# FIND ADDRESSES WITHIN DISTANCE
@router.get("/nearby")
def get_addresses_within_distance(
    latitude: float = Query(...),
    longitude: float = Query(...),
    distance_km: float = Query(...),
    db: Session = Depends(get_db)
):

    addresses = db.query(Address).all()

    result = []

    for addr in addresses:

        dist = calculate_distance(
            latitude,
            longitude,
            addr.latitude,
            addr.longitude
        )

        if dist <= distance_km:
            result.append({
                "id": addr.id,
                "name": addr.name,
                "distance_km": round(dist, 2)
            })

    return result