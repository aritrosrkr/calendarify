import os
import ijson
import requests
import sys
import welcome
from datetime import datetime

COURSE_DATA_URL = "https://usis-cdn.eniamza.com/connect.json"
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
CACHE_FILE = os.path.join(CACHE_DIR, "connect.json")

# Convert "2025-06-14" -> "Saturday, June 14, 2025"
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%A, %B %d, %Y")
    except ValueError:
        return "Invalid date"

# Convert "13:50:00" -> "1:50 PM"
def format_time(time_str):
    try:
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        return time_obj.strftime("%I:%M %p").lstrip("0")
    except ValueError:
        return "Invalid time"

def ensure_cache():
    """Ensure the cache file exists; if not, download and save."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    if not os.path.exists(CACHE_FILE):
        print("🌐 Downloading course data for the first time...")
        try:
            response = requests.get(COURSE_DATA_URL, stream=True)
            response.raise_for_status()
            with open(CACHE_FILE, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print("✅ Course data cached.")
        except Exception as e:
            print(f"❌ Failed to fetch and cache course data: {e}")
            sys.exit(1)


def collectCourseData(courses):
    welcome.clear_terminal()
    print("🔍 Cross-checking the schedule...")

    ensure_cache()  # 📦 Ensure cache file is ready

    validCourses = []

    try:
        with open(CACHE_FILE, "rb") as f:
            items = ijson.items(f, "item")
            for obj in items:
                code = obj.get("courseCode", "").strip().upper()
                section = obj.get("sectionName", "").strip()

                for inputCourse, inputSection in courses:
                    if code == inputCourse.upper() and section == inputSection:
                        if obj not in validCourses:
                            print(f"✅ Found: {inputCourse} - Section {inputSection}")
                            validCourses.append(obj)
                        break
    except Exception as e:
        print(f"❌ Error reading course data: {e}")
        sys.exit(1)

    welcome.clear_terminal()
    print("\n🗓️ Schedule Summary:")
    if not validCourses:
        print("⚠️ No valid course schedules found.")
    else:
        for idx, course in enumerate(validCourses, 1):
            code = course["courseCode"]
            section = course["sectionName"]
            classStartDate = course["sectionSchedule"]["classStartDate"]
            classEndDate = course["sectionSchedule"]["classEndDate"]
            classDays = [x['day'] for x in course["sectionSchedule"]["classSchedules"]]
            classStartTime = course["sectionSchedule"]["classSchedules"][0]['startTime']
            classEndTime = course["sectionSchedule"]["classSchedules"][0]['endTime']
            midExamDate = course["sectionSchedule"]["midExamDate"]
            finalExamDate = course["sectionSchedule"]["finalExamDate"]
            faculties = course["faculties"]
            room = course["roomName"]
            labSchedules = course["labSchedules"]
            labRoom = course["labRoomName"] 
            print(f"{idx}. {code} - {section}")
            print(f"  ->Course Start Data: {format_date(classStartDate)}")
            print(f"  ->Course End Date:  {format_date(classEndDate)}")
            if midExamDate:
                print(f"  ->Course Mid Exam Data: {format_date(midExamDate)}")
            if finalExamDate:
                print(f"  ->Course Final Exam Date:  {format_date(finalExamDate)}")
            if not labSchedules:
                print("   --Class Schedule--")
                print(f"        -> Days: ", *classDays)
                print(f"        -> Faculties: {faculties}")
                print(f"        -> Room: {room}")
                print(f"        -> Start Time: {format_time(classStartTime)}")
                print(f"        -> End Time: {format_time(classEndTime)}")
            else:
                print("   --Theory Schedule--")
                print(f"        -> Days: ", *classDays)
                print(f"        -> Faculties: {faculties}")
                print(f"        -> Room: {room}")
                print(f"        -> Start Time: {format_time(classStartTime)}")
                print(f"        -> End Time: {format_time(classEndTime)}")
                print("   --Lab Schedule--")
                print(f"        -> Days: {labSchedules[0]['day']}")
                print(f"        -> Room: {labRoom}")
                print(f"        -> Start Time: {format_time(labSchedules[0]['startTime'])}")
                print(f"        -> End Time: {format_time(labSchedules[0]['endTime'])}")
            print('\n')
    while True:
        print("\n🔁 What would you like to do next?")
        print("1. Continue to Calendar Creation")
        print("2. Go Back and Re-enter Courses")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            return validCourses
        elif choice == "2":
            print("🔄 Returning to course entry...")
            return None
        elif choice == "3":
            print("👋 Exiting. Have a great day!")
            sys.exit(0)
        else:
            print("❌ Invalid input. Please enter 1, 2, or 3.")
