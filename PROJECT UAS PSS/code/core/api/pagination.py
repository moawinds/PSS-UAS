from ninja.pagination import PaginationBase


class CustomPagination(PaginationBase):

    class Input:
        page: int = 1
        size: int = 5

    class Output:
        items: list
        total: int

    def paginate_queryset(self, queryset, pagination, **params):

        start = (pagination.page - 1) * pagination.size
        end = start + pagination.size

        return {
            "items": list(queryset[start:end]),
            "total": queryset.count()
        }