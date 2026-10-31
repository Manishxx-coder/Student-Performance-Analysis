# Student Performance Analysis using Python and PySpark

College mini-project with a Streamlit dashboard.

## Features
- Reads student CSV data
- Uses PySpark to calculate totals, averages, and grades
- Ranks students by average
- Shows high performers and subject-wise averages
- Allows CSV upload and result download

## Requirements
- Windows 10/11 64-bit
- Python 3.11
- Java JDK 17 (set `JAVA_HOME` if the installer does not configure it)
- Visual Studio Code (recommended)

## Setup on Windows
1. Install Python 3.11 from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Install JDK 17 from https://adoptium.net/temurin/releases/?version=17.
3. Open this project folder in Command Prompt or VS Code terminal.
4. Create and activate a virtual environment:

   ```bat
   python -m venv venv
   venv\Scripts\activate
   ```

5. Install packages:

   ```bat
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Start the dashboard:

   ```bat
   streamlit run app.py
   ```

7. Streamlit will open a local browser page. If not, open the URL printed in the terminal (usually http://localhost:8501).

## Dataset format
CSV columns must be exactly:
`student_id,name,mathematics,science,english`

Marks should be numeric. The included dataset contains fictional sample students.

## Grade rules
- A: average >= 90
- B: average >= 75
- C: average >= 60
- D: average >= 40
- F: average < 40

## Important note
This starter project uses Spark's `local[*]` mode, which runs on your own computer. It demonstrates PySpark data processing but is not a distributed multi-machine cluster. For genuinely large/distributed data, the next extension is to run Spark on a cluster or cloud platform.

## Troubleshooting
- `python is not recognized`: reinstall Python and enable Add Python to PATH, then reopen the terminal.
- Java error: run `java -version`; confirm JDK 17 is installed and `JAVA_HOME` points to its installation folder.
- Port already in use: close the previous Streamlit terminal or run `streamlit run app.py --server.port 8502`.
- If PySpark reports a Java gateway error, verify `java -version`, `JAVA_HOME`, and that the installed Java version is compatible.
