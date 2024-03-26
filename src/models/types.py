from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import text, String, DateTime
from sqlalchemy.orm import mapped_column

# ID
uuid_pk = Annotated[
    UUID, mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
]

# Strings
str_100 = Annotated[str, mapped_column(String(100), nullable=False)]
str_255 = Annotated[str, mapped_column(String(255), nullable=False)]

# Date, time
created_at = Annotated[
    datetime, mapped_column(
        DateTime(timezone=False),
        server_default=text("TIMEZONE('utc', now())")
    )
]
updated_at = Annotated[
    datetime, mapped_column(
        DateTime(timezone=False),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    ),
]
