from pydantic import BaseModel, Field


class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    country: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class AddressUpdate(BaseModel):
    name: str | None = None
    street: str | None = None
    city: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class AddressResponse(AddressCreate):
    id: int

    class Config:
        from_attributes = True