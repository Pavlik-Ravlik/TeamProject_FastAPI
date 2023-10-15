import uvicorn
import fastapi

from fastapi import FastAPI, Request, status

from src.routes import auth, users, shares, public, admin


app = FastAPI()

app.include_router(auth.router, prefix='/app')
app.include_router(users.router, prefix='/app')
app.include_router(shares.router, prefix='/app')
app.include_router(public.router, prefix='/app')
app.include_router(admin.router, prefix='/app')

@app.get('/')
def read_root():
    '''main page'''
    return {'message': 'Main page'}



if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)