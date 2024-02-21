import cv2
import numpy as np
from recognition.encodings_storage import EncodingLocalStorage
from recognition.recognition import Recognition
from Attendance import Attendance
from datetime import datetime
# from Attendance_Report import AttendanceReporter

supabase_url = "https://mhfnttlxzmusbqdnyuum.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1oZm50dGx4em11c2JxZG55dXVtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzMzMjM2MywiZXhwIjoyMDIyOTA4MzYzfQ.KUkkkp6nutcdt_t2LFvcYbHeE9xsW5wywzxT6qd51kM"
# reporter = AttendanceReporter(supabase_url, supabase_key)

attendance = Attendance(supabase_url, supabase_key)

records = attendance.fetch_records()
print("Attendance Records:")

# Generate a daily report for a specific date
# specific_date = datetime(2024, 1, 31)

# reporter.generate_daily_report(specific_date)

    # Generate a weekly report for a specific week
# start_date_of_week = datetime(2024, 1, 29)  # Assuming Monday is the start of the week
# reporter.generate_weekly_report(start_date_of_week)



# reporter = AttendanceReporter(supabase_url, supabase_key)
    

VIDEO_FEED = cv2.VideoCapture(0)

encodings_storage = EncodingLocalStorage('images')
face_recognition = Recognition(encodings_storage=encodings_storage)

while True:
    ret, frame = VIDEO_FEED.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    face_encodings, face_locations = face_recognition.face_locations_encodings(rgb_small_frame)
    matches = face_recognition.find_matches(face_encodings, face_locations)
    if matches:
        # Display the results
        for match in matches:
            name = match['name']
            attendance.mark_attendance(name,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            (top, right, bottom, left) = match['location'] 
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
           
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    # Display the resulting image
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

VIDEO_FEED.release()
cv2.destroyAllWindows()
