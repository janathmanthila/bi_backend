from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from django.db.models import Sum, Avg
from faker import Faker
from itertools import zip_longest
import random

from .models import *
from .serializers import *

# SUBJECTS = ['Maths', 'Science']
# SUBJECTS = ['Maths', 'Science', 'IT']
# GRADES = ['1', '2']
GRADES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12' ]
# CALENDER_YEAR = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']

BASE = [
    {"subject": "Maths", "years": ['2001', '2002', '2003']},
    {"subject": "Science", "years": ['2004', '2005', '2006']},
    {"subject": "IT", "years": ['2007', '2008', '2009', '2010']}
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

        # Create Marks Records
        # for subject in SUBJECTS:
        #     for year in CALENDER_YEAR:
        #         for semester in ['1', '2']:
        #             for grade in GRADES:
        #                 for student in Student.objects.all():
        #                     # This will prevent creation of records if the count exceeded 10000. But this might
        #                     # effect for the analysis coz the data is not fully completed.
        #                     if Mark.objects.all().count() < 10000:
        #                         Mark.objects.create(student=student, subject=subject, mark=random.randint(1, 100),
        #                                             semester=semester, grade=grade, year=year)
        #                     else:
        #                         break

    students = Student.objects.all()
    for item in BASE:
        for year in item["years"]:
            for semester in ['1', '2']:
                for grade in GRADES:
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
            if chart['type'] == "Line and Bar":
                subjects = chart['subjects']
                column_data = []
                avg_data = []
                for subject in subjects:
                    grade = chart['grades']
                    semesters = chart['semesters']
                    students = chart['students']
                    years = chart['years']
                    value = Mark.objects.filter(grade__range=grade, semester__in=semesters, student__in=students, subject=subject, year__range=years).aggregate(Sum('mark'))
                    column_data.append(value['mark__sum'] or 0)

                    avg_value = Mark.objects.filter(grade__range=grade, semester__in=semesters, student__in=students,
                                                    subject=subject, year__range=years).aggregate(Avg('mark'))
                    avg_data.append(avg_value['mark__avg'] or 0)
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
        return Response(result)
    else:
        raise APIException("Invalid Request")

