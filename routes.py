from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session,joinedload
from database import Sessionlocal
from models import Author, Profile, Blog, Category, BlogCategory
from schemas import SeedResponse, AuthorCreate, ProfileCreate, BlogCreate, CategoryCreate,EagerResponse,CustomEagerBlog,EagerBlogResponse

router = APIRouter()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/seed", response_model=SeedResponse)
def seed(db: Session = Depends(get_db)):

    author = Author(
        name="Anmol",
        email="anmol@gmail.com"
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    profile = Profile(
        bio="Python Developer",
        author_id=author.id
    )
    db.add(profile)

    blog1 = Blog(title="FastAPI Basics", content="FastAPI", author_id=author.id)
    blog2 = Blog(title="ORM", content="ORM", author_id=author.id)
    blog3 = Blog(title="Pydantic Guide", content="Pydantic", author_id=author.id)

    db.add_all([blog1, blog2, blog3])
    db.commit()
    db.refresh(blog1)
    db.refresh(blog2)
    db.refresh(blog3)

    category1 = Category(name="Backend")
    category2 = Category(name="Python")

    db.add_all([category1, category2])
    db.commit()
    db.refresh(category1)
    db.refresh(category2)

    blog_category_data = [
        BlogCategory(blog_id=blog1.id, category_id=category1.id),
        BlogCategory(blog_id=blog1.id, category_id=category2.id),
        BlogCategory(blog_id=blog2.id, category_id=category1.id),
        BlogCategory(blog_id=blog3.id, category_id=category2.id),
    ]

    db.add_all(blog_category_data)
    db.commit()

    return {
        "author": AuthorCreate(name=author.name, email=author.email),
        "profile": ProfileCreate(bio=profile.bio),
        "blogs": [
            BlogCreate(title=blog1.title, content=blog1.content),
            BlogCreate(title=blog2.title, content=blog2.content),
            BlogCreate(title=blog3.title, content=blog3.content),
        ],
        "categories": [
            CategoryCreate(name=category1.name),
            CategoryCreate(name=category2.name),
        ]
    }


@router.get("/eager/author/{id}", response_model=EagerResponse)
def eager(id: int, db: Session = Depends(get_db)):

    author_db = (
        db.query(Author)
        .options(
            joinedload(Author.profile),
            joinedload(Author.blogs)
                .joinedload(Blog.categories)
                .joinedload(BlogCategory.category)
        )
        .filter(Author.id == id)
        .first()
    )

    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")

    return {
        "name": author_db.name,
        "profile": author_db.profile.bio,
        "blogs": [
            {
                "title": blog.title,
                "categories": [
                    {"name": bc.category.name}
                    for bc in blog.categories
                ],
            }
            for blog in author_db.blogs
        ],
    }

@router.get("/eager/blog/{id}",response_model=EagerBlogResponse)
def eager_blog(id:int , db:Session=Depends(get_db)):
    db_blog=db.query(Blog).options(
        joinedload(Blog.author),
        joinedload(Blog.categories).joinedload(BlogCategory.category)
    ).filter(Blog.id==id).first()
    return{
        "title":db_blog.title,
        "author":db_blog.author.name,
        "categories": [
            {"name": bc.category.name}
            for bc in db_blog.categories
        ],
    }