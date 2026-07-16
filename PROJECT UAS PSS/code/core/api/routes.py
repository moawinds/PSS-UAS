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


from pydantic import BaseModel
from django.contrib.auth.models import User
from ninja.errors import HttpError
from ninja_simple_jwt.jwt.token_operations import get_access_token_for_user, get_refresh_token_for_user

class GoogleLoginSchema(BaseModel):
    email: str
    first_name: str
    last_name: str

@router.post("/auth/google-login")
def google_login(request, data: GoogleLoginSchema):
    if not data.email or "@" not in data.email:
        raise HttpError(400, "Email tidak valid")
    
    username = data.email.split("@")[0]
    
    user, created = User.objects.get_or_create(
        email=data.email,
        defaults={
            'username': username,
            'first_name': data.first_name,
            'last_name': data.last_name,
            'is_active': True
        }
    )
    
    if not created:
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.save()
        
    access_token, _ = get_access_token_for_user(user)
    refresh_token, _ = get_refresh_token_for_user(user)
    
    return {
        "access": access_token,
        "refresh": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }