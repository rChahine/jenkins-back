from pydantic import BaseModel, validator


class newUserSchema(BaseModel):
    """ Schema for add a new user """
    role: str
    username: str
    password: str

    @validator('role')
    def check_role(cls, v):
        if v == "A" or v == "U":
            return v
        else:
            raise ValueError("role must be A or U")
