# PostgreSQL 데이터베이스 연결 완료! 🎉

## ✅ 완료된 작업

### 1. 환경 설정 파일
- ✅ `app/core/config.py` - 애플리케이션 설정 관리
- ✅ `app/core/database.py` - 데이터베이스 연결 및 세션 관리

### 2. 데이터베이스 모델
- ✅ `app/models/menu.py` - 메뉴 테이블
- ✅ `app/models/option.py` - 옵션 테이블
- ✅ `app/models/order.py` - 주문 및 주문 항목 테이블

### 3. 마이그레이션 설정
- ✅ `alembic.ini` - Alembic 설정
- ✅ `alembic/env.py` - 마이그레이션 환경 설정
- ✅ `alembic/versions/` - 마이그레이션 버전 디렉토리

### 4. 유틸리티 스크립트
- ✅ `create_env_file.py` - .env 파일 자동 생성
- ✅ `test_db_connection.py` - 데이터베이스 연결 테스트
- ✅ `init_database.py` - 데이터베이스 초기화 및 테스트 데이터 생성
- ✅ `setup_database.bat` - 원클릭 데이터베이스 설정

## 🗄️ 데이터베이스 스키마

```
┌─────────────────────┐
│      menus          │
├─────────────────────┤
│ id (PK)            │
│ name               │
│ description        │
│ price              │
│ image_url          │
│ stock_quantity     │
│ is_available       │
│ created_at         │
│ updated_at         │
└─────────────────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐
│   menu_options      │
├─────────────────────┤
│ id (PK)            │
│ menu_id (FK)       │
│ name               │
│ value              │
│ price              │
│ is_available       │
│ created_at         │
│ updated_at         │
└─────────────────────┘

┌─────────────────────┐
│      orders         │
├─────────────────────┤
│ id (PK)            │
│ order_number       │
│ customer_name      │
│ total_price        │
│ status             │
│ notes              │
│ created_at         │
│ updated_at         │
│ completed_at       │
└─────────────────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐
│   order_items       │
├─────────────────────┤
│ id (PK)            │
│ order_id (FK)      │
│ menu_id (FK)       │
│ quantity           │
│ unit_price         │
│ total_price        │
│ options (JSON)     │
│ created_at         │
└─────────────────────┘
```

## 🚀 사용 방법

### 자동 설정 (권장)

```bash
cd backend
setup_database.bat
```

### 수동 설정

```bash
# 1. .env 파일 생성
python create_env_file.py

# 2. 데이터베이스 생성 (PostgreSQL)
psql -U postgres -c "CREATE DATABASE orderbean_db;"

# 3. 연결 테스트
python test_db_connection.py

# 4. 데이터베이스 초기화
python init_database.py

# 5. 서버 실행
python -m uvicorn app.main:app --reload
```

## 📋 데이터베이스 설정

`.env` 파일에 다음 정보를 설정하세요:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=postgresql

# Database URL
DATABASE_URL=postgresql+asyncpg://postgres:postgresql@localhost:5432/orderbean_db
```

## 🔧 주요 기능

### 비동기 데이터베이스 연결

```python
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def some_endpoint(db: AsyncSession = Depends(get_db)):
    # 데이터베이스 작업
    result = await db.execute(select(Menu))
    menus = result.scalars().all()
    return menus
```

### 모델 사용 예시

```python
from app.models import Menu, MenuOption, Order, OrderItem, OrderStatus

# 메뉴 생성
menu = Menu(
    name="아메리카노",
    description="진한 에스프레소",
    price=4000,
    stock_quantity=100
)
db.add(menu)
await db.commit()

# 주문 생성
order = Order(
    order_number="ORD-001",
    customer_name="홍길동",
    total_price=8000,
    status=OrderStatus.PENDING
)
db.add(order)
await db.commit()
```

### 관계 조회

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# 메뉴와 옵션 함께 조회
result = await db.execute(
    select(Menu).options(selectinload(Menu.options))
)
menus = result.scalars().all()

for menu in menus:
    print(f"{menu.name}: {menu.price}원")
    for option in menu.options:
        print(f"  - {option.name}: {option.value} (+{option.price}원)")
```

## 📊 초기 테스트 데이터

### 메뉴 (5개)
1. 아메리카노 - 4,000원
2. 카페라떼 - 4,500원
3. 카푸치노 - 4,500원
4. 바닐라 라떼 - 5,000원
5. 카라멜 마키아또 - 5,500원

### 옵션 (각 메뉴당 6개)
- 사이즈: Regular, Large (+500원)
- 샷 추가: 1샷 (+500원), 2샷 (+1,000원)
- 온도: HOT, ICE

### 테스트 주문 (1개)
- 주문번호: ORD-20251102-001
- 고객: 홍길동
- 상태: 주문 접수
- 항목: 아메리카노 2개, 카페라떼 1개

## 🔍 데이터 확인

### psql 사용

```bash
# 데이터베이스 접속
psql -U postgres -d orderbean_db

# 모든 메뉴 조회
SELECT id, name, price, stock_quantity FROM menus;

# 옵션과 함께 메뉴 조회
SELECT m.name, mo.name as option_name, mo.value, mo.price
FROM menus m
LEFT JOIN menu_options mo ON m.id = mo.menu_id
ORDER BY m.id, mo.id;

# 주문 상세 조회
SELECT 
    o.order_number,
    o.customer_name,
    m.name as menu_name,
    oi.quantity,
    oi.total_price
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN menus m ON oi.menu_id = m.id;

# 주문 상태별 집계
SELECT status, COUNT(*) as count, SUM(total_price) as total
FROM orders
GROUP BY status;
```

### Python 스크립트

```python
import asyncio
from app.core.database import AsyncSessionLocal
from app.models import Menu, Order
from sqlalchemy import select

async def check_data():
    async with AsyncSessionLocal() as session:
        # 메뉴 조회
        result = await session.execute(select(Menu))
        menus = result.scalars().all()
        
        print("메뉴 목록:")
        for menu in menus:
            print(f"- {menu.name}: {menu.price}원")
        
        # 주문 조회
        result = await session.execute(select(Order))
        orders = result.scalars().all()
        
        print("\n주문 목록:")
        for order in orders:
            print(f"- {order.order_number}: {order.status.value}")

asyncio.run(check_data())
```

## 🛠️ Alembic 마이그레이션

### 새 마이그레이션 생성

```bash
alembic revision --autogenerate -m "Description of changes"
```

### 마이그레이션 적용

```bash
alembic upgrade head
```

### 현재 버전 확인

```bash
alembic current
```

### 마이그레이션 히스토리

```bash
alembic history
```

### 롤백

```bash
# 한 단계 롤백
alembic downgrade -1

# 특정 버전으로 롤백
alembic downgrade <revision_id>

# 모든 마이그레이션 롤백
alembic downgrade base
```

## ⚙️ 데이터베이스 설정 옵션

### config.py 설정

```python
from app.core.config import settings

# 데이터베이스 URL
print(settings.database_url)

# 디버그 모드 (SQL 쿼리 로깅)
settings.DEBUG = True  # SQL 쿼리를 콘솔에 출력
```

### database.py 설정

```python
# 연결 풀 설정
engine = create_async_engine(
    settings.database_url,
    echo=settings.DEBUG,      # SQL 로깅
    pool_pre_ping=True,       # 연결 유효성 검사
    pool_size=10,             # 기본 연결 수
    max_overflow=20,          # 추가 연결 수
)
```

## 🐛 문제 해결

### 연결 오류

```bash
# PostgreSQL 서비스 확인
services.msc

# 포트 확인
netstat -an | findstr 5432

# 데이터베이스 존재 확인
psql -U postgres -l
```

### 패키지 오류

```bash
# asyncpg 재설치
pip uninstall asyncpg
pip install asyncpg

# 전체 재설치
pip install -r requirements.txt --force-reinstall
```

### 마이그레이션 오류

```bash
# 마이그레이션 디렉토리 초기화
alembic init alembic

# 또는 직접 테이블 생성 (개발 환경)
python init_database.py
```

## 📝 다음 단계

1. ✅ 데이터베이스 연결 설정
2. ✅ 모델 정의
3. ⏳ **API 엔드포인트 구현**
   - GET /api/v1/menus - 메뉴 조회
   - POST /api/v1/orders - 주문 생성
   - GET /api/v1/admin/orders - 관리자 주문 조회
4. ⏳ 비즈니스 로직 구현
5. ⏳ 프론트엔드 연동

## 📚 참고 자료

- **SQLAlchemy 2.0 문서**: https://docs.sqlalchemy.org/en/20/
- **Alembic 문서**: https://alembic.sqlalchemy.org/
- **asyncpg 문서**: https://magicstack.github.io/asyncpg/
- **PostgreSQL 문서**: https://www.postgresql.org/docs/

---

**작성일**: 2025년 11월 2일  
**버전**: 1.0.0  
**상태**: ✅ 데이터베이스 연결 완료

