# app.py

import welcome  # import the welcome screen
import dataCollection
import checkSchedule
import icsCreator

def main():
    welcome.show_welcome()
    while True:
        courses = dataCollection.collectCourses()
        validCourses = checkSchedule.collectCourseData(courses)
        if validCourses is None:
            continue
        else:
            icsCreator.generate_calendar(validCourses)
            break

if __name__ == "__main__":
    main()

