import dataclasses
from datetime import datetime
from supabase import create_client




class Attendance():
    USERS={}
    def __init__(self,supabase_url, supabase_key) :
                self.supabase = create_client(supabase_url, supabase_key)
        

    def fetch_records (self):
            query = self.supabase.from_("attendance").select("*").order("time")
            return query.execute().data

    def mark_attendance (self, name, time):
        if name in self.USERS and (self.USERS[name]-datetime.now()).total_seconds()<60:
            return 
        
        self.USERS[name] = datetime.now()
        record = {"name": name, "time": time}
        data , count = self.supabase.table("attendance").insert(record).execute()
        if "error" in data:
            print("Failed to add row:", data["error"])
        else:
            print("Row tzeed(table+).")
                    