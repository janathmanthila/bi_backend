from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from django.db.models import Sum, Avg
from faker import Faker
import random

from .models import *
from .serializers import *


GRADES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12' ]

BASE = [
    {"subject": "Maths", "years": ['2001', '2002', '2003'], "color": "#009888"},
    {"subject": "Science", "years": ['2004', '2005', '2006'], "color": "#FF9A00"},
    {"subject": "IT", "years": ['2007', '2008', '2009', '2010'], "color": "#50342C"}
]

FIELDS = {"Marks": "mark"}


@api_view(['POST'])
def create_dataset(request):
    fake = Faker()
    Mark.objects.all().delete()
    Student.objects.all().delete()

    # Create Students
    for student in range(0, 20):
        Student.objects.create(name=fake.name(), email=fake.email(), city=fake.city(), phone=fake.phone_number())

    students = Student.objects.all()
    for item in BASE:
        used_grade_index = -1
        for year in item["years"]:
            for semester in ['1', '2']:
                for increment in range(0, 2):
                    grade = GRADES[used_grade_index+1]
                    used_grade_index += 1
                    for student in students:
                        # This will prevent creation of records if the count exceeded 10000. But this might
                        # effect for the analysis coz the data is not fully completed.
                        if Mark.objects.all().count() < 10000:
                            Mark.objects.create(student=student, subject=item["subject"], mark=random.randint(1, 100),
                                                semester=semester, grade=grade, year=year)
                        else:
                            break
    return Response("Data Created Successfully")


@api_view()
def get_students(request):
    return Response(StudentListSerializer(Student.objects.all(), many=True).data)


@api_view(['POST'])
def fetch_summery_data(request):
    if request.data:
        results = []
        for summery in request.data:
            grade = summery['grades']
            semesters = summery['semesters']
            students = summery['students']
            subjects = summery['subjects']
            years = summery['years']
            value = Mark.objects.filter(grade__range=grade, semester__in=semesters, student__in=students, subject__in=subjects, year__range=years).aggregate(Sum(FIELDS[summery['field']]))
            data = {**summery, 'value': value['mark__sum'] or 0}
            results.append(data)
        return Response(results)
    else:
        raise APIException("Invalid Request")


@api_view(['POST'])
def fetch_chart_data(request):
    if request.data:
        result = []
        for chart in request.data:
            grade = chart['grades']
            semesters = chart['semesters']
            semesters.sort()
            students = chart['students']
            years = chart['years']
            if chart['type'] == "Line and Bar":
                subjects = chart['subjects']
                column_data = []
                avg_data = []
                for subject in subjects:
                    value = Mark.objects.filter(grade__range=grade, semester__in=semesters, student__in=students, subject=subject, year__range=years).aggregate(Sum('mark'))
                    column_data.append(value['mark__sum'] or 0)

                    avg_value = Mark.objects.filter(grade__range=grade, semester__in=semesters, student__in=students,
                                                    subject=subject, year__range=years).aggregate(Avg('mark'))
                    avg_data.append(round(avg_value['mark__avg'] or 0, 2))
                series = [
                    {
                        "name": "Subject",
                        "type": 'column',
                        "data": column_data,
                        "lineWidth": 1
                    },
                    {
                        "name": 'Subject Average',
                        "data": avg_data
                    }
                ]

                data = {
                    **chart,
                    'series': series,
                    "yAxis": [
                        {
                            "title": {
                                "text": 'Marks'
                            },

                        },
                    ],
                    "xAxis": [
                        {
                            "categories": chart['subjects']

                        },
                    ]
                }
                result.append(data)
            else:
                multiple_column_data = []
                lables = []
                for item in BASE:
                    col_data = {
                        "name": item['subject'],
                        "type": 'column',
                        "data": [],
                        "lineWidth": 1,
                        "color": item['color']
                    }

                    for year in range(years[0], years[1]+1):
                        for semester in semesters:

                            value = Mark.objects.filter(grade__range=grade, semester=semester, student__in=students,
                                                        subject=item['subject'], year=year).aggregate(Sum('mark'))
                            col_data["data"].append(value['mark__sum'] or 0)

                    multiple_column_data.append(col_data)
                for year in range(years[0], years[1] + 1):
                    for semester in semesters:
                        lables.append(f"{year} - {semester}")
                data = {
                    **chart,
                    'series': multiple_column_data,
                    "yAxis": [
                        {
                            "title": {
                                "text": 'Marks'
                            },

                        },
                    ],
                    "xAxis": [
                        {
                            "categories": lables

                        },
                    ]
                }
                result.append(data)

        return Response(result)
    else:
        raise APIException("Invalid Request")


