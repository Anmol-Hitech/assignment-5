from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, datetime

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    profile = relationship("Profile", back_populates="author", uselist=False, cascade="all, delete-orphan")
    blogs = relationship("Blog", back_populates="author", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    bio = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), unique=True)

    author = relationship("Author", back_populates="profile")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True)
    published_at=Column(DateTime,default=datetime.now,nullable=False)
    author = relationship("Author", back_populates="blogs")
    categories = relationship("BlogCategory", back_populates="blog", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False, unique=True)

    blogs = relationship("BlogCategory", back_populates="category", cascade="all, delete-orphan")


class BlogCategory(Base):
    __tablename__ = "blog_categories"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))

    blog = relationship("Blog", back_populates="categories")
    category = relationship("Category", back_populates="blogs")
