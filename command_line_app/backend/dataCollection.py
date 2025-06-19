import welcome
import sys
import checkSchedule

def get_valid_course_input():
    while True:
        course_input = input("Enter course (CourseName - Section): ").strip()
        if course_input.lower() == 'q':
            print("👋 Exiting course entry.")
            welcome.clear_terminal()
            sys.exit(0)
        if '-' in course_input:
            name, _, section = course_input.partition('-')
            name, section = name.strip(), section.strip()
            if name and len(section) == 2 and section.isdigit():
                return (name, section)
        print("❌ Invalid format. Use: CourseName - Section (e.g., CSE220 - 01)")

def collectCourses():
    welcome.clear_terminal()

    courses = []

    while True:
        # Ask for number of courses
        while True:
            user_input = input("📦 Enter the number of courses (or type 'q' to quit): ").strip().lower()
            if user_input in {"q", "exit"}:
                print("👋 Exiting course entry.")
                welcome.clear_terminal()
                sys.exit(0)
            try:
                coursesNo = int(user_input)
                assert coursesNo > 0, "Number of courses must be a positive integer."
                break
            except ValueError:
                print("❌ Please enter a valid integer.")
            except AssertionError as e:
                print(f"❌ {e}")

        # Input course details
        for i in range(1, coursesNo + 1):
            print(f"📘 Course {i} of {coursesNo}")
            course = get_valid_course_input()
            if course in courses:
                print(f"⚠️ Course '{course[0]} - Section {course[1]}' is already added. Skipping duplicate.")
            else:
                courses.append(course)

        # Display added courses
        print("\n✅ Courses added:")
        for idx, (name, section) in enumerate(courses, 1):
            print(f"{idx}. {name} - Section {section}")

        # Prompt for next action
        while True:
            print("\n🔁 What would you like to do next?")
            print("1. Add more courses")
            print("2. Start over (remove all)")
            print("3. Finish and cross-check the routine")
            choice = input("Enter choice (1/2/3): ").strip()
            if choice == "1":
                break  # Continue to add more
            elif choice == "2":
                courses.clear()
                print("🧹 All courses cleared. Starting over.\n")
                break
            elif choice == "3":
                if len(courses) <= 0:
                    print("❌⚠️ No courses were entered. Please add at least 1 course")
                    break
                print("✅ Course entry complete. Now cross-checking of the routine will start.")
                return courses
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
