# Real-time Face Recognition

<img src="/home/louay/Downloads/Untitled-2024-02-02-2028.png" style="zoom: 50%;" />



# How to run ?

- Install os dependencies

  ```bash
  sudo apt-get install build-essential cmake pkg-config
  sudo apt-get install libx11-dev libatlas-base-dev
  sudo apt-get install libgtk-3-dev libboost-python-dev
  ```

- Install dlib 

  ```bash
  git clone https://github.com/davisking/dlib.git dlib
  cd  dlib && python3 setup.py install
  ```

- Create a venv and Install debs from requirements.txt

  ```bash
  python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
  ```

- Execute this command then configure  your secrets inside .env file

  ```bash
  cp .env.example .env
  ```

- Run script

- ```
  python main.py
  ```

### Resources

- https://github.com/medsriha/real-time-face-recognition
- https://martlgap.medium.com/how-to-build-a-simple-live-face-recognition-app-in-python-529fc686b475
- https://towardsdatascience.com/real-time-face-recognition-an-end-to-end-project-b738bb0f7348
- https://github.com/Arhanmansoori/FACE-RECOGNITION-ATTENDANCE-SYSTEM-USING-PYTHON-WITH-REAL-TIME-DATA-BASE-AND-EXCEL-RECORD/commit/817bd09d7c3b10469faf347247896bd84b0cbec7
- https://supabase.com/docs/reference/python/introduction 'base de donnee'
  https://www.youtube.com/watch?v=HQ_ytw58tC4s
           ##############

# To do List
- [x] Fix uknown faces not detected
- [ ] -in regestir class make a classifier job that ask for your role and add it to supabase table to make it clear:
  (ki tamel rehister labeed jdid yotleeb alik ismek w role mte3k par exemple chef personnel/khadeem .. fi partie supabase lezm tetzed parite f tableau l role  w fpartie code class Attendance lezm tetzed m3a kol regsieter jdida y aski e role  )
- [ ] -in register add a key to take picture (time to change position for fast detection )
  -connection beetwn app and code 
  -search for app to make statics from data base and relate them to mobile app 
  -learn flutter and android studio 

         ###################

-supabase pass 8jrxj2CK2Coi6QcU
-supabase key pGJLv1zRlYhZPqKT
******** supabase / python code : attendance mangment system ********


 fama deux posibilite y ema l'attendance managment tsyr fel python code(kima andhla + kima-) ****
yema direct ma lapplication (kifkif)
When you have a mobile app for attendance management, you have a couple of options for how to relate it to the Supabase database:

1. **Direct Integration with Supabase:**
   In this approach, your mobile app communicates directly with the Supabase database to perform operations such as marking attendance, fetching attendance records, generating reports, etc. Your mobile app sends requests to Supabase's REST API or uses Supabase's client libraries to interact with the database.
    This approach simplifies the architecture by eliminating the need for an intermediary Python codebase.

2. **Indirect Integration via Python Code:**
   Alternatively, you can maintain a Python backend that serves as an intermediary between your mobile app and the Supabase database. Your mobile app communicates with the Python backend through an API (e.g., REST API), and the Python backend, in turn, interacts with the Supabase database using Supabase's client libraries.
    This approach allows you to add business logic, perform data validation, or implement additional features in the Python backend before interacting with the database.

Choosing between these approaches depends on various factors such as the complexity of your application, the need for business logic or data processing, security requirements, scalability considerations, and team expertise.

Here are some considerations for each approach:

**Direct Integration with Supabase:**
- **Simplicity:** Direct integration simplifies the architecture by removing the need for an additional backend layer.
- **Real-time Updates:** Supabase provides real-time capabilities, allowing your mobile app to receive updates immediately as they occur in the database.
- **Scalability:** Supabase is designed to scale automatically, handling concurrent requests from multiple clients.
- **Security:** Ensure that your Supabase API keys are securely managed to prevent unauthorized access.

**Indirect Integration via Python Code:**
- **Business Logic:** You can implement complex business logic or data processing in the Python backend before interacting with the database.
- **Data Validation:** Perform data validation and enforce constraints in the backend to ensure data integrity.
- **Additional Features:** The Python backend can implement additional features such as authentication, authorization, caching, or integration with other services.
- **Flexibility:** You have more flexibility to customize and extend the functionality of your application within the backend.

Ultimately, the best approach depends on your specific requirements, constraints, and preferences. If your mobile app primarily involves simple CRUD operations on the database with minimal processing logic, direct integration with Supabase may be sufficient. However, if you anticipate the need for complex business logic or additional backend features, an indirect integration via Python code may be more appropriate. 

   

### app mobile 
APPlication: 
sign in  (adress/password required )
/home page date and time /sections() ely mawjoud fel sujet 
/attendance : imort from data base information about specfic id and form it (daly/weekly/monthly)
insert new user(khadeem)
remove user(khadeem)
camera feed option in app that give access to admin to open the camera 



### Rasberry pi setup

 methode rasberrylocalAdress   ping raspberrypi.local
 methode ssh commands: 
-ssh pi@adrsIP
-continueFingerPrint / motpass(fel config mta3 l Pi)

updates:
sudo apt-get update
sudo apt-get upgrade -y

*prepartion python: 
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
*install python
terminal  : wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tar.xz
            tar -xvf Python-3.10.0.tar.xz
            (cd Python-3.10.0
            ./configure --enable-optimizations)
            (make -j 4 
            sudo make altinstall)
            python3.10 --version
            
            python3 -m pip install --upgrade pip
            python3 -m pip install opencv-python
            python3 -m pip install numpy
            python3  -m pip install flask





###  Code IMPORT

import cv2 
import face_recognition 
import ABC
import os
import numpy as np
import datetime


# project
