from django.conf import settings
from django.http import JsonResponse
from django.views import View
from sqlalchemy import create_engine, text
import json


class EmployeesView(View):
    ...

    @staticmethod
    def get(request):
        engine = create_engine(settings.CONNECTION)
        with engine.connect() as connection:
            query = text(f"""
                            SELECT
                                E.fEMPLID AS id,
                                E.fEMPLCODE AS code,
                                E.fCAPTION AS name
                            FROM
                                EMPLOYEES AS E""")
            result = connection.execute(query)
            employees_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]

        return JsonResponse(employees_list, status=200, safe=False)

    @staticmethod
    def post(request):
        engine = create_engine(settings.CONNECTION)
        with engine.connect() as connection:
            data = json.loads(request.body)
            print(data)
            params = {
                "EmplCode": data["code"],
                "Caption": data["name"],
                "Address": data["address"],
                "Phone": data["phone"],
                "Passport": data["passport"],
                "EmplCard": data["empl_card"],
                "IsSalesConsultant": 0,
                "TS": 1,
                "Status": 1,
                "EmplID": 10000001

            }

        query = text(f"""
        EXEC dbo.asp_addEmployee :EmplCode, :Caption, :Address, :Phone, :Passport, :EmplCard, :IsSalesConsultant, :TS,
        :Status, :EmplID""")

        engine = create_engine(settings.CONNECTION)
        with engine.begin() as connection:
            connection.execute(query, params)

            update_query = f""" UPDATE DICTIONARYTS SET fVALUE=fVALUE  """
            connection.execute(text(update_query))

        return JsonResponse("ok", status=200, safe=False)
