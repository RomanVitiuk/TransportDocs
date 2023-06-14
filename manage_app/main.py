from fastapi import FastAPI

from routers import (
    company_router, user_router, docs_router
)


app = FastAPI(
    title="Business Transport Docs App"
)

app.include_router(user_router.router)
app.include_router(company_router.router)
app.include_router(docs_router.router)
