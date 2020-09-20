@app.route('/course', methods=['POST'])
def create_course():
    """
    Takes a json object that has the needed data: 
        1- courseName: new course name
        2- langugae: Programming language to be used with this course labs
        3- labs: An array that has the test cases to be runned, time limit for each test case
        4- course type: type of grader to be used with this course (unit testing / stdout cases comparison)
    """
    try:
        courseName = request.json['courseName']
        language = request.json['language']
        labs = request.json['labs']
    except KeyError:
        return jsonify({'status': "course name, language, and labs parameters must be included"}), 400
    try:
        manager.create_course(courseName, language, labs)
        return "SUCCESS", 200
    except:
        return "Failed to run the grader", 500
