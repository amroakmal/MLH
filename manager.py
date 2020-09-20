def add_new_course_to_current_courses(data):
    with open(Path(__file__).parent.joinpath("courses_config.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_course(course_name, language, labs):
    current_courses = get_courses() 
    for course in current_courses:
        if course.lower() == course_name.lower():
            return "Course already present", 404
    current_courses = get_courses_config()
    current_courses[course_name] = {"course_type": "stdout", "language": language, "labs": labs}
    add_new_course_to_current_courses(current_courses)
    stdout_common.create_course_data(course_name, labs)
