from django.conf import settings
from django.http import JsonResponse
from django.views import View
from sqlalchemy import create_engine, text


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
                                E.fCAPTION AS name,
                                E.fUNIT AS unit_code,
                                Q.fCAPTION AS unit_name
                            FROM
                                EMPLOYEES AS E
                                LEFT JOIN QNTUNIT Q ON E.fUNIT = Q.fCODE""")
            result = connection.execute(query)
            employees_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]

        return JsonResponse(employees_list, status=200, safe=False)

    @staticmethod
    def post(request):
        pass
