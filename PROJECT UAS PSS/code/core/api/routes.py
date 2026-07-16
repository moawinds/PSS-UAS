from ninja import Router, Query
from ninja.pagination import paginate

from core.models import Course

from .schemas import CourseSchema
from .filters import CourseFilter
from .auth import jwt_auth
from .throttling import SimpleRateThrottle

router = Router()


@router.get("/hello")
def hello(request):
    return {
        "message": "Hello Simple LMS"
    }


@router.get(
    "/courses",
    response=list[CourseSchema],
    auth=jwt_auth,
    throttle=SimpleRateThrottle()
)
@paginate
def get_courses(
    request,
    filters: Query[CourseFilter]
):
    qs = Course.objects.all()

    if filters.name:
        qs = qs.filter(name__icontains=filters.name)

    if filters.price_min is not None:
        qs = qs.filter(price__gte=filters.price_min)

    if filters.price_max is not None:
        qs = qs.filter(price__lte=filters.price_max)

    if filters.teacher:
        qs = qs.filter(teacher__username__icontains=filters.teacher)

    return qs