from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import string, random
import uvicorn

from models import Hash
from schemas import HashCreate, HashResponse
from database import get_db

app = FastAPI()

origins = [
  "https://*.yamnor.me",
  "http://localhost",
  "http://0.0.0.0"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

from database import engine
import models
models.Base.metadata.create_all(bind=engine)

def generate_key(length=6):
  characters = string.ascii_letters + string.digits
  return ''.join(random.choices(characters, k=length))

@app.post("/add", response_model=HashResponse)
def create_key(hash: HashCreate, db: Session = Depends(get_db)):
  key = generate_key()
  db_hash = Hash(hash=hash.hash, key=key)
  db.add(db_hash)
  db.commit()
  db.refresh(db_hash)
  return db_hash

@app.get("/{key}")
def return_hash(key: str, db: Session = Depends(get_db)):
  db_hash = db.query(Hash).filter(Hash.key == key).first()
  if db_hash is None:
    raise HTTPException(status_code=404, detail="Not found")
  return {"hash": db_hash.hash}

if __name__ == "__main__":
  uvicorn.run(app, host='localhost', port=8000)