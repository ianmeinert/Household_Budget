import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from householdbudget.auth.router import router as auth_router
from householdbudget.database.connection import create_tables
from householdbudget.utils.db_utils import validate_db_file

app = FastAPI()

# add the auth handler to the router
app.include_router(auth_router)


def main():
    load_dotenv()
    db_file = os.getenv("DBFILE")
    validate_db_file(db_file)
    create_tables(db_file)

    port = 5000
    host = "127.0.0.1"

    # start the ASGI service
    uvicorn.run(app=app, host=host, port=port)


if __name__ == "__main__":
    main()
