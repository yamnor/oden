from pydantic import BaseModel

class HashBase(BaseModel):
  hash: str

class HashCreate(HashBase):
  pass

class HashResponse(HashBase):
  key: str

  class Config:
    orm_mode = True
