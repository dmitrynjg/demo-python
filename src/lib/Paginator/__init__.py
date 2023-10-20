from math import ceil

class Paginator:
    total = 0

    def __init__(self, query, page=1, per_page=10):
        self.per_page = per_page
        if per_page > 100:
            self.page = 100
        self.query = query
        self.page = page
       

    def apply_pagination(self):
        offset = (self.page - 1) * self.per_page
        self.total = self.query.count()
        self.query = self.query.offset(offset).limit(self.per_page)
        

    def get_results(self):
        return {
            'result': self.query.all(),
            "page": self.page,
            "total": self.total,
            "totalPage": self.per_page,
            "totalPages": ceil(self.total / self.per_page)
        }
