import json
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from sqlalchemy import create_engine, text


class UnitView(View):
    @staticmethod
    def post(request):
        data = json.loads(request.body)
        params = {
            "Code": data["code"],
            "Caption": data["name"],
            "Brief": data["brief"],
            "UnitID": 0,
            "Status": 1
        }

        query = text(f"""EXEC dbo.asp_addQntUnit :Code, :Caption, :Brief, :UnitID, :Status""")

        engine = create_engine(settings.CONNECTION)
        with engine.begin() as connection:
            connection.execute(query, params)

            update_query = f""" UPDATE DICTIONARYTS SET fVALUE=fVALUE  """
            connection.execute(text(update_query))

        return JsonResponse("ok", status=200, safe=False)
