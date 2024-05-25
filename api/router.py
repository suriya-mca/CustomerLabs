from ninja import Router 
from django.core.serializers import serialize

# from .schema import *
# from .models import *


router = Router()

@router.get("/home")
def home(request):
    
    return "hi"