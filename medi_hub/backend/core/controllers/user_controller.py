from fastapi import HTTPException, status
from core import logger
from core.cruds.auth_crud import CRUDAuth

logging = logger(__name__)


class UserController:
    """
    Controller for user-related operations, such as fetching user details, updating user information, etc.
    """

    def __init__(self):
        self.crud_auth = CRUDAuth()

    async def list_users(self):
        """
        Fetch a list of all users.

        Returns:
            A list of user details.

        Raises:
            HTTPException with status code 500 for any unexpected errors.
        """
        try:
            logging.info(f"Executing UserController.list_users function")
            result = await self.crud_auth.get_all()
            return result
        except Exception as error:
            logging.error(f"Error in UserController.list_users function: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(error),
            )
