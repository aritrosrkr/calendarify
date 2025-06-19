import os
import ijson
import gzip
import requests
import sys
import welcome

# 📌 Change this to your actual URL
COURSE_DATA_URL = "https://usis-cdn.eniamza.com/connect.json"

# 🗂️ Cache location: terminal_app/cache/connect.json.gz
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "connect.json")


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
        with gzip.open(CACHE_FILE, "rb") as f:
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
            code = course.get("courseCode", "N/A")
            section = course.get("sectionName", "??")
            faculties = course.get("faculties", "N/A")
            print(f"{idx}. {code} - {section} || {faculties}")

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
