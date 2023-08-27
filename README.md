# Dashcam Footage Analyzer

Dashcam Footage Analyzer is a Python application that utilizes a Flask frontend to streamline the processing of dashcam footage from the 70mai A500S Dashcam.

Using `pyTesseract` and `OpenCV`, the application first separates the files into individual rides, and upon completion, undergoes a processing phase to extract information and save it in a PostgreSQL database. This information is subsequently utilized to generate a map, infer additional data via various APIs, and calculations.

## How to Use

Currently, there's no master script, however, one will be implemented soon. In the meantime, the rough steps to use the application are as follows:

1. Create the database(s), and utilize the table creation tool while filling in the appropriate details.
2. Run the `first_table_creator.py`, `second_table_insert.py`, and `third_table_sql.py` scripts sequentially.
3. Execute `plotly-test-dashboard.py` to run the app.

Please remember that this is very preliminary information. If there's enough interest in the project, plans for scalability and dockerization will be considered for ease of use.

![Dashboard Insights](https://github.com/ahnafaf/Dashcam-Footage-Analyzer/assets/108675365/8ab8ca53-19a2-4bc3-9182-f5294a9a1a12)
![Frontal](https://github.com/ahnafaf/Dashcam-Footage-Analyzer/assets/108675365/5b8c8111-ccce-41c2-8636-770913d446e2)
