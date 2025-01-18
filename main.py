from fastapi import FastAPI
from Routers import auth_router, bookings_router, ground_detail_router, ground_list, revenue_router, owner_details_router, help_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(auth_router.router)
app.include_router(bookings_router.router)
app.include_router(ground_detail_router.router)
app.include_router(ground_list.router)
app.include_router(revenue_router.router)
app.include_router(owner_details_router.router)
app.include_router(help_router.router)



