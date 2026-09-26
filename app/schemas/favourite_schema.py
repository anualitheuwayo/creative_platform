from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavouriteResponse(BaseModel):
    favourite_id: int
    client_id: int
    artwork_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )