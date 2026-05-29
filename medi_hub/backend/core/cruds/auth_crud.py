from core import logger
from core.cruds.base import CRUDBase
from core.models.user_model import User
from core.apis.schemas.requests.auth_request import UserCreateRequest, UserUpdateRequest
from odmantic import ObjectId
from datetime import datetime, timezone
from typing import Optional

logging = logger(__name__)


class CRUDAuth(CRUDBase[User, UserCreateRequest, UserUpdateRequest]):
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

    async def update(self, id: ObjectId, obj_in: dict) -> Optional[User]:
        """Update an existing user document by its ID.

        Args:
            id: The ObjectId of the user to update.
            obj_in: A dictionary containing the fields to update.

        Returns:
            The updated User document if the update was successful, otherwise None.
        """
        try:
            logging.info(f"Executing CRUDAuth.update function for user ID {id}")
            update_data = dict(obj_in)
            update_data["updated_at"] = datetime.now(timezone.utc)

            update_result = await self.engine.get_collection(self.model).update_one(
                {"_id": id},
                {"$set": update_data},
            )

            if update_result.matched_count == 0:
                logging.warning(f"User with ID {id} not found for update")
                return None

            return await self.engine.find_one(self.model, self.model.id == id)
        except Exception as error:
            logging.error(
                f"Error in CRUDAuth.update function for user ID {id}: {error}"
            )
            raise

    async def delete(self, id: ObjectId) -> bool:
        """Delete a user document by its ID.

        Args:
            id: The ObjectId of the user to delete.

        Returns:
            True if the deletion was successful, False if the user was not found.
        """
        try:
            logging.info(f"Executing CRUDAuth.delete function for user ID {id}")
            delete_result = await self.engine.get_collection(self.model).delete_one(
                {"_id": id}
            )
            if delete_result.deleted_count == 0:
                logging.warning(f"User with ID {id} not found for deletion")
                return False
            return True
        except Exception as error:
            logging.error(
                f"Error in CRUDAuth.delete function for user ID {id}: {error}"
            )
            raise

    async def list_all(self):
        """Fetch all user documents from the database.

        Returns:
            A list of all User documents.
        """
        try:
            logging.info(f"Executing CRUDAuth.list_all function")
            return await self.engine.find(self.model)
        except Exception as error:
            logging.error(f"Error in CRUDAuth.list_all function: {error}")
            raise

    async def get_by_id(self, id: str) -> Optional[User]:
        """Fetch a user document by its ID.

        Args:
            id: The ObjectId of the user to fetch.

        Returns:
            The User document if found, otherwise None.
        """
        try:
            if isinstance(id, str) and len(id) == 24:
                id = ObjectId(id)
            logging.info(f"Executing CRUDAuth.get_by_id function for user ID {id}")
            return await self.engine.find_one(self.model, self.model.id == id)
        except Exception as error:
            logging.error(
                f"Error in CRUDAuth.get_by_id function for user ID {id}: {error}"
            )
            raise
