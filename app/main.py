from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routes.documents import router as document_router
from app.routes.selections import router as selection_router
from app.routes import generations

app = FastAPI(
    title="CT200 AI Backend",
)

app.include_router(document_router)
app.include_router(selection_router)
app.include_router(generations.router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")