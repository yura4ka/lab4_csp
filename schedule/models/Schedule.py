from math import floor

from .Database import Database
from .ScheduleLesson import ScheduleLesson


class Schedule:
    lessons: list[ScheduleLesson]

    def __init__(self, db: Database):
        self.lessons = []
        self.db = db
        for cl in db.classes.values():
            for _ in range(floor(cl.hours_per_week / 2)):
                self.lessons.append(
                    ScheduleLesson(
                        class_id=cl.id,
                        classroom_id=-1,
                        teacher_id=-1,
                        day=-1,
                        slot=-1,
                    )
                )
        self.max_weak_violations = len(self.lessons)

    def setData(self, data: dict[int, int]):
        for i in range(len(self.lessons)):
            self.lessons[i].day = data.get(i * 4 + 0, -1)
            self.lessons[i].slot = data.get(i * 4 + 1, -1)
            self.lessons[i].teacher_id = data.get(i * 4 + 2, -1)
            self.lessons[i].classroom_id = data.get(i * 4 + 3, -1)

    def get_timetable(self):
        timetable: list[list[list[ScheduleLesson]]] = [
            [[] for _ in range(4)] for _ in range(5)
        ]
        for lesson in self.lessons:
            if not (lesson.day == -1 or lesson.slot == -1):
                timetable[lesson.day - 1][lesson.slot - 1].append(lesson)
        return timetable

    def has_conflicts(self):
        timetable = self.get_timetable()
        for day in timetable:
            for slot in day:
                size = len(slot)
                for i in range(size):
                    lesson1 = slot[i]
                    if self.__check_wrong_teacher_violation(lesson1):
                        return True
                    if self.__check_capacity_violation(lesson1):
                        return True
                    for j in range(i + 1, size):
                        lesson2 = slot[j]
                        if (
                            lesson1.classroom_id == lesson2.classroom_id
                            and lesson1.classroom_id != -1
                        ):
                            return True
                        if (
                            lesson1.teacher_id == lesson2.teacher_id
                            and lesson1.teacher_id != -1
                        ):
                            return True
                        if (
                            self.db.get_group_by_class_id(lesson1.class_id).id
                            == self.db.get_group_by_class_id(lesson2.class_id).id
                        ):
                            return True

        return False

    def print(self):
        t = self.get_timetable()
        for i, d in enumerate(t):
            print(f"\n===========Day {i + 1}===========")
            for j, s in enumerate(d):
                print(f"\n==========Lesson {j + 1}==========")
                self.db.print_schedule_lessons(s)

    def __check_capacity_violation(self, lesson: ScheduleLesson):
        if lesson.classroom_id == -1:
            return False
        return (
            self.db.classrooms[lesson.classroom_id].capacity
            < self.db.get_group_by_class_id(lesson.class_id).student_count
        )

    def __check_wrong_teacher_violation(self, lesson: ScheduleLesson):
        if lesson.classroom_id == -1:
            return False
        return not any(
            s.type == self.db.classes[lesson.class_id].type
            and s.subject_id == self.db.get_subject_by_class_id(lesson.class_id).id
            for s in self.db.teachers.get(lesson.teacher_id).subjects
        )
