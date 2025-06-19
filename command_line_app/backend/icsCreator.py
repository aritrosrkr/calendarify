import os
import sys
import uuid
from datetime import datetime, timedelta
from pytz import timezone
from icalendar import Calendar, Event
import welcome
import tkinter as tk
from tkinter import filedialog

def get_save_filepath(default_filename="course_schedule.ics"):
    root = tk.Tk()
    root.withdraw()  # Hide main window

    filepath = filedialog.asksaveasfilename(
        defaultextension=".ics",
        filetypes=[("iCalendar files", "*.ics")],
        initialfile=default_filename,
        title="Save Calendar As"
    )
    root.destroy()
    return filepath  # returns empty string if user cancels

bdt = timezone("Asia/Dhaka")

def save_ics_file(calendar):
    filepath = get_save_filepath()

    if not filepath:
        print("❌ Save cancelled by user.")
        sys.exit(1)

    try:
        with open(filepath, "wb") as f:
            f.write(calendar.to_ical())
        print(f"✅ Calendar saved at: {filepath}")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Failed to save .ics file: {e}")
        sys.exit(1)

def format_time_ics(date_str, time_str):
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        return bdt.localize(dt)
    except ValueError:
        return None

def get_first_class_date(start_date_str, target_weekday_str):
    weekday_map = {
        "MONDAY": 0, "TUESDAY": 1, "WEDNESDAY": 2, "THURSDAY": 3,
        "FRIDAY": 4, "SATURDAY": 5, "SUNDAY": 6
    }
    target_weekday = weekday_map.get(target_weekday_str.upper())
    if target_weekday is None:
        return None

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    days_ahead = target_weekday - start_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def generate_calendar(validCourses):
    welcome.clear_terminal()
    print("📆 Generating your .ics calendar file...\n")

    calendar = Calendar()
    calendar.add("prodid", "-//BRACU Schedule Generator//")
    calendar.add("version", "2.0")

    for course in validCourses:
        courseCode = course.get("courseCode", "UNKNOWN")
        section = course.get("sectionName", "??")
        title = f"{courseCode} - {section}"
        faculty = course.get("faculties", "TBA")
        room = course.get("roomName", "TBA")

        schedule = course.get("sectionSchedule", {})
        start_date = schedule.get("classStartDate", "")
        end_date = schedule.get("classEndDate", "")
        class_schedules = schedule.get("classSchedules", [])

        for sched in class_schedules:
            day = sched.get("day", "")
            start_time = sched.get("startTime", "")
            end_time = sched.get("endTime", "")

            first_date = get_first_class_date(start_date, day)
            if first_date is None:
                continue

            dt_start = format_time_ics(first_date.strftime("%Y-%m-%d"), start_time)
            dt_end = format_time_ics(first_date.strftime("%Y-%m-%d"), end_time)
            if not dt_start or not dt_end:
                continue

            event = Event()
            event.add("uid", str(uuid.uuid4()))
            event.add("summary", title)
            event.add("dtstart", dt_start)
            event.add("dtend", dt_end)
            event.add("location", room)
            event.add("description", f"Faculty: {faculty}")
            event.add("rrule", {
                "freq": "weekly",
                "byday": [day[:2].upper()],
                "until": format_time_ics(end_date, "23:59:00")
            })
            calendar.add_component(event)

        lab_schedule = course.get("labSchedules")
        if lab_schedule:
            for lab in lab_schedule:
                lab_day = lab.get("day", "")
                lab_start = lab.get("startTime", "")
                lab_end = lab.get("endTime", "")
                lab_room = course.get("labRoomName", "LabRoom")
                lab_faculty = course.get("labFaculties", "Lab Instructor")

                first_lab_date = get_first_class_date(start_date, lab_day)
                dt_start = format_time_ics(first_lab_date.strftime("%Y-%m-%d"), lab_start)
                dt_end = format_time_ics(first_lab_date.strftime("%Y-%m-%d"), lab_end)
                if not dt_start or not dt_end:
                    continue

                event = Event()
                event.add("uid", str(uuid.uuid4()))
                event.add("summary", f"{title} - LAB")
                event.add("dtstart", dt_start)
                event.add("dtend", dt_end)
                event.add("location", lab_room)
                event.add("description", f"Faculty: {lab_faculty}")
                event.add("rrule", {
                    "freq": "weekly",
                    "byday": [lab_day[:2].upper()],
                    "until": format_time_ics(end_date, "23:59:00")
                })
                calendar.add_component(event)

        mid_date = schedule.get("midExamDate")
        mid_start = schedule.get("midExamStartTime", "00:00:00")
        mid_end = schedule.get("midExamEndTime", "00:00:00")
        if mid_date:
            event = Event()
            event.add("uid", str(uuid.uuid4()))
            event.add("summary", f"{title} - MIDTERM")
            event.add("dtstart", format_time_ics(mid_date, mid_start))
            event.add("dtend", format_time_ics(mid_date, mid_end))
            event.add("description", f"Midterm Exam for {title}")
            calendar.add_component(event)

        final_date = schedule.get("finalExamDate")
        final_start = schedule.get("finalExamStartTime", "00:00:00")
        final_end = schedule.get("finalExamEndTime", "00:00:00")
        if final_date:
            event = Event()
            event.add("uid", str(uuid.uuid4()))
            event.add("summary", f"{title} - FINAL")
            event.add("dtstart", format_time_ics(final_date, final_start))
            event.add("dtend", format_time_ics(final_date, final_end))
            event.add("description", f"Final Exam for {title}")
            calendar.add_component(event)

    save_ics_file(calendar)
