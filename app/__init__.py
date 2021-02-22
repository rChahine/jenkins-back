import sys

from fastapi import Body, Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session

from .database import get_session
from .models import Choice, User, UserChoice  # noqa F401
from .schemas import newUserSchema
from .security import decode_auth_token, encrypt_password
from .settings import TESTING


app = FastAPI(
    title="CI api",
    docs_url=None,
    redoc_url="/doc"
)


if TESTING:
    sys.exit(0)


def retrieve_user(
    session: Session = Depends(get_session),
    authorization: str = Header(...)
) -> User:

    """ Retrieve user from encoded token """

    decoded = decode_auth_token(authorization)

    user = session.query(User).filter(User.id == decoded['id']).one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@app.post('/authentication/login')
async def login(
    login: str = Body(...),
    password: str = Body(...),
    session: Session = Depends(get_session)
):

    """ Connexion à l'application """
    user = User.get_by_credentials(session, login, password)

    if user is not None:
        return {'token': user.get_auth_token()}
    else:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


@app.get('/user/me')
async def get_user(user: User = Depends(retrieve_user)):
    return user


@app.post('/user')
async def add_user(
    new_user: newUserSchema,
    user: User = Depends(retrieve_user),
    session: Session = Depends(get_session)
):
    """ add a new user in database """

    username_exist = session.query(User).filter_by(
        username=new_user.username
    ).one_or_none()

    if username_exist is None:

        user_to_add = User(
            username=new_user.username,
            password=encrypt_password(new_user.password),
            role=new_user.role
        )

        session.add(user_to_add)
        session.commit()

        return {'detail': "User added"}
    else:
        raise HTTPException(status_code=409, detail="Username already exist")


@app.post('/choices')
async def add_choice(
    wording: str = Body(..., embed=True),
    user: User = Depends(retrieve_user),
    session: Session = Depends(get_session)
):
    """ Add a choice in database """
    print(user)
    if user.role == "A":
        choice = Choice(wording=wording)

        session.add(choice)
        session.commit()

        return {'detail': "Choice added"}
    else:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized request"
        )


@app.get('/choices')
async def retrieve_choice(
    user: User = Depends(retrieve_user),
    session: Session = Depends(get_session)
):
    """ Return list of choices in database """

    choices = session.query(Choice).all()
    beautified = []

    for choice in choices:
        nbVote = session.query(UserChoice)\
            .filter(UserChoice.idChoice == choice.id)\
            .count()

        beautified.append({
            'choice': choice,
            'nb_vote': nbVote
        })

    return beautified


@app.put("/vote/{choice_id}")
async def add_vote(
    choice_id: int,
    user: User = Depends(retrieve_user),
    session: Session = Depends(get_session)
):
    """ add a vote for a user """
    if user.role == "U":

        choice = session.query(Choice).filter_by(
            id=choice_id
        ).one_or_none()

        if choice is not None:

            vote = UserChoice(
                idUser=user.id,
                idChoice=choice_id
            )

            session.add(vote)
            session.commit()

            return {'detail': "Vote added"}

        else:
            raise HTTPException(
                status_code=404,
                detail="Choice not found"
            )

    else:
        raise HTTPException(
            status_code=401,
            detail="Only users are allowed to vote"
        )


@app.delete("/vote/{choice_id}")
async def unvote(
    choice_id: int,
    user: User = Depends(retrieve_user),
    session: Session = Depends(get_session)
):
    """ add a vote for a user """
    if user.role == "U":

        choice = session.query(Choice).filter_by().one_or_none()

        if choice is not None:

            session.query(UserChoice).filter_by(
                idUser=user.id,
                idChoice=choice_id
            ).delete()

            session.commit()

            return {'detail': "Vote deleted"}

        else:
            raise HTTPException(
                status_code=404,
                detail="Choice not found"
            )

    else:
        raise HTTPException(
            status_code=401,
            detail="Only users are allowed to vote"
        )
