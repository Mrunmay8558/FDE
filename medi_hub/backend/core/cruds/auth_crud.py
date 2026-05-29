from core import logger
from core.cruds.base import CRUDBase
from core.models.user_model import User
from core.apis.schemas.requests.auth_request import UserCreateRequest
from odmantic import ObjectId
from datetime import datetime, timezone
from typing import Optional

logging = logger(__name__)


class CRUDAuth(CRUDBase[User, UserCreateRequest, None]):
    def __init__(self):
        super().__init__(model=User)

    async def create(self, obj_in: dict) -> User:
        """Create a new user document in the database.

        Args:
            obj_in: UserCreateRequest containing email, password, mobile number, and optional address.

        Returns:
            The created User document.
        """
        try:
            logging.info(f"Executing CRUDAuth.create function")
            if isinstance(obj_in, dict):
                data = obj_in
            else:
                data = obj_in.model_dump()

            user = User(**data)
            return await self.engine.save(user)
        except Exception as error:
            logging.error(f"Error in CRUDAuth.create function: {error}")
            raise

    async def get_by_email(self, email: str):
        """Fetch a user document by email.

        Args:
            email: The email address to search for.

        Returns:
            The User document if found, otherwise None.
        """
        try:
            logging.info(f"Executing CRUDAuth.get_by_email function")
            return await self.engine.find_one(self.model, self.model.email == email)
        except Exception as error:
            logging.error(f"Error in CRUDAuth.get_by_email function: {error}")
            raise
