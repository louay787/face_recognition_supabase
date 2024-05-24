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
