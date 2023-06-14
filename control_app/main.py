from fastapi import FastAPI

from routers import (
    auth_router, check_docs_router,
    control_router, org_router
)


app = FastAPI(
    title="Control Transport Docs App"
)

app.include_router(auth_router.router)
app.include_router(control_router.router)
app.include_router(org_router.router)
app.include_router(check_docs_router.router)
