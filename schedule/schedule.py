from CSP import CSP
from schedule.models.Database import Database
from schedule.models.Schedule import Schedule


def schedule():
    db = Database("./schedule/data")

    schedule = Schedule(db)

    db.print_classrooms()
    db.print_teachers()
    db.print_groups()

    teacherDomain = {t for t in db.teachers}
    classroomDomain = {c for c in db.classrooms}
    dayDomain = range(1, 6)
    slotDomain = range(1, 5)

    variables = {}
    for i in range(len(schedule.lessons)):
        variables[i * 4 + 0] = dayDomain
        variables[i * 4 + 1] = slotDomain
        variables[i * 4 + 2] = teacherDomain
        variables[i * 4 + 3] = classroomDomain

    def is_correct(data):
        s = Schedule(db)
        s.setData(data)
        return s.calculate_conflicts() == 0

    csp = CSP(variables)
    csp.add_constraint(variables, is_correct)

    print("running..")
    result = csp()
    schedule.setData(result)

    schedule.print()
    print("\n")
    schedule.calculate_conflicts(print_conflicts=True)
