from fastapi import FastAPI, status

from app.api.product import product_router
from app.api.review import review_router
from app.api.user import user_router

app = FastAPI()
app.include_router(product_router)
app.include_router(review_router)
app.include_router(user_router)


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
def perform_healthcheck():
    """
    Performs a health check on the application.

    Returns:
        dict: A dictionary with a success message.

    Response:
        - 200: The health check was successful.
    """
    return {"message": "OK"}
