def paginate(query, page=1, limit=5):
    total_items = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    return {
        'page': page,
        'limit': limit,
        'total_items': total_items,
        'total_pages': (total_items + limit - 1) // limit,
        'items': items
    }
