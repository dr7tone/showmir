
from fastapi import FastAPI
from app.routes import users, setup_db, admins, tests, nfc_tags

app = FastAPI(
    title="showmir",
)

app.include_router(tests.router)
app.include_router(users.router)
app.include_router(setup_db.router)
app.include_router(admins.router)
app.include_router(nfc_tags.router)
@app.get("/")
async def root():
    return {"message": "Хз что тут написать, но это работает!"} # нужен ли нам вообще главный экран?


@app.get("/api/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {"status": "ok", "service": "showmir"}



