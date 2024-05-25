import orjson
from ninja import NinjaAPI
from ninja.parser import Parser
from ninja.renderers import BaseRenderer

from .router import router as main_router

class ORJSONParser(Parser):
    def parse_body(self, request):
        return orjson.loads(request.body)

class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)  
        
api = NinjaAPI(parser=ORJSONParser(), renderer=ORJSONRenderer())

api.add_router("/api/v1", main_router)