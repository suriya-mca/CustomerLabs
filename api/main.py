from ninja import NinjaAPI
from .routers import router as main_router 
        
api = NinjaAPI()

api.add_router("/v1", main_router)