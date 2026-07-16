from ninja import FilterSchema
from typing import Optional


class CourseFilter(FilterSchema):
    name: Optional[str] = None
    price_min: Optional[int] = None   # Filter harga minimum
    price_max: Optional[int] = None   # Filter harga maksimum
    teacher: Optional[str] = None     # Filter berdasarkan username pengajar