from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import errors as psycopg2_errors
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_current_user, get_db

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    """現在のユーザー情報を取得"""
    return current_user


@router.get("/", response_model=list[schemas.UserResponse])
async def get_users(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """全ユーザー一覧を取得"""
    users = crud.user.get_multi(db_session=db)
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """ユーザー情報を取得"""
    user = crud.user.get(db_session=db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ユーザーを作成"""
    try:
        db_user = crud.user.create(db_session=db, obj_in=user)
        return db_user
    except psycopg2_errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )


@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """ユーザー情報を更新"""
    try:
        db_user = crud.user.update(db_session=db, id=user_id, obj_in=user)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user
    except psycopg2_errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    """ユーザーを削除"""
    db_user = crud.user.remove(db_session=db, id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": "User deleted successfully"}
