from fastapi import FastAPI
from database import engine, BaseModel
from authentication.routes import router as authentication_router
from tweet.routes import router as tweet_router
from user.routes import router as user_router


app = FastAPI()
app.include_router(user_router)
app.include_router(authentication_router)
app.include_router(tweet_router)


@app.on_event("startup")
async def setup_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(BaseModel.metadata.create_all)
        except:
            pass
