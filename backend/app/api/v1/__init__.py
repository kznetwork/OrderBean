"""
API v1 라우터 모듈
"""
from fastapi import APIRouter
from app.api.v1 import menus, orders, admin

api_router = APIRouter(prefix="/api/v1")

# 라우터 등록
api_router.include_router(menus.router)
api_router.include_router(orders.router)
api_router.include_router(admin.router)

__all__ = ["api_router"]
