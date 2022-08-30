import unittest
from enum import Enum

from mytoolkit.db.dataclass import DataClass
from mytoolkit.db.mongo.base_model import BaseModel

db_config = {
    "host": "127.0.0.1",
    "port": 27017,
    "db": "test"
}


class Gender(Enum):
    NONE = 0
    MAN = 1
    WOMAN = 2


class Subject(Enum):
    MATH = "math"
    ENGLISH = "english"
    CHINESE = "chinese"


class Score(DataClass):
    def define_fields(self):
        self.subject = self.define("subject", Subject)
        self.score = self.define_int("score")
        return super().define_fields()


class Student(BaseModel):
    COLLECTION = "student"

    def define_fields(self):
        self.name = self.define_str("name")
        self.age = self.define_int("age")
        self.gender = self.define("gender", Gender)
        self.scores = self.define_list("scores", Score)

        return super().define_fields()


class TestMongoModel(unittest.TestCase):
    def test_create_data(self):
        student = Student()
        student.name = "cn_qlg"
        student.age = 18
        student.gender = Gender.MAN
        student.scores = [
            Score({"subject": Subject.MATH, "score": 100}),
            Score({"subject": Subject.CHINESE, "score": 99})
        ]
        student.create()

    def test_bulk_insert(self):
        student_a = Student()
        student_a.name = "cn_qlg2"
        student_a.age = 18
        student_a.gender = Gender.MAN
        student_a.scores = [
            Score({"subject": Subject.MATH, "score": 100}),
            Score({"subject": Subject.CHINESE, "score": 99})
        ]

        student_b = Student()
        student_b.name = "cn_qlg2"
        student_b.age = 18
        student_b.gender = Gender.MAN
        student_b.scores = [
            Score({"subject": Subject.MATH, "score": 100}),
            Score({"subject": Subject.CHINESE, "score": 99})
        ]
        students = [student_a, student_b]
        res, d = Student.insert_many(students, ignore_duplicated=True)
        print(res, d)

    def test_count(self):
        self.assertTrue(Student.count({}) > 0)


if __name__ == '__main__':
    from mytoolkit.db.mongo.connection import connect
    connect(**db_config)
    unittest.main()
