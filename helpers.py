from models import BlogCategory,Category
def paginate(query, page: int=1, limit: int=10):
    page = max(page, 1)
    limit = max(min(limit, 100), 1)
    return query.offset((page - 1) * limit).limit(limit).all()
def filter_by_category(query,category):
    category_blogs=query.join(BlogCategory).join(Category).filter(Category.name==category).all()
    return category_blogs