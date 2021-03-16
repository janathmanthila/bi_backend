from django.db import models


class Student(models.Model):
    class Meta:
        ordering = ["id"]

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Mark(models.Model):
    class Meta:
        ordering = ["id"]

    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    subject = models.CharField(max_length=500)
    mark = models.FloatField()
    semester = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2')])
    grade = models.IntegerField(max_length=2)
    year = models.IntegerField(max_length=4)

    # To reduce the student name duplication, I moved the student name to another table and add a foreign key reference

    def __str__(self):
        return f"{self.student.name} - {self.subject} in {self.year}-{self.semester}"