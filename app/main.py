from fastapi import FastAPI 
from app.api.routes import router 
 
app = FastAPI(title="Language Translator API") 
app.include_router(router) 
