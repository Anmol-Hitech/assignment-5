from pydantic import BaseModel, EmailStr
from typing import List, Optional


class AuthorCreate(BaseModel):
    name: str
    email: EmailStr


class ProfileCreate(BaseModel):
    bio: str


class BlogCreate(BaseModel):
    title: str
    content: Optional[str]=None


class CategoryCreate(BaseModel):
    name: str


class SeedResponse(BaseModel):
    author: AuthorCreate
    profile: ProfileCreate
    blogs: List[BlogCreate]
    categories: List[CategoryCreate]
class CustomEagerBlog(BaseModel):
    title:str
    categories:List[CategoryCreate]
class EagerResponse(BaseModel):
    name:str
    profile:str
    blogs:List[CustomEagerBlog]

class EagerBlogResponse(BaseModel):
    title:str
    author:str
    categories:List[CategoryCreate]


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str


class TotalBlogResponse(BaseModel):
    blogs: List[BlogResponse]