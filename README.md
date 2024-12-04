# Climate Prediction and Analysis Dashboard

## Project Description
The Climate Prediction and Analysis Dashboard is an interactive web application designed to provide users with insights into climate data and predictive analytics. Built using Python and Streamlit, this dashboard leverages various data visualization libraries to present complex climate data in an accessible and user-friendly format.

### Features
- **Data Visualization**: The dashboard utilizes libraries such as Matplotlib and Altair to create dynamic and informative visualizations, allowing users to explore climate trends and patterns effectively.
- **Predictive Modeling**: By integrating machine learning models from TensorFlow and Scikit-learn, the application can forecast future climate conditions based on historical data, providing valuable insights for researchers, policymakers, and the general public.
- **User Interaction**: Users can interact with the dashboard to filter data, select different visualization types, and view predictions based on their specific interests or requirements.
- **Comprehensive Analysis**: The application supports various climate-related datasets, enabling users to conduct in-depth analyses and draw meaningful conclusions about climate change and its impacts.

### Technologies Used
- **Python**: The primary programming language for developing the application.
- **Streamlit**: A powerful framework for building interactive web applications quickly and easily.
- **Matplotlib & Altair**: Libraries for creating a wide range of visualizations to represent climate data effectively.
- **TensorFlow & Scikit-learn**: Machine learning libraries used for building predictive models to analyze climate trends.

### Purpose
The Climate Prediction and Analysis Dashboard aims to raise awareness about climate change and its implications by providing users with tools to visualize and analyze climate data. By making complex data more accessible, the project seeks to empower individuals and organizations to make informed decisions regarding climate action and sustainability.

## Requirements

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run src/main1.py
```
to create a new environment with terminal
```bash
conda env create -f environment.yml
``` 
Use a Virtual Environment:
A virtual environment isolates your Python installation and avoids the need for admin privileges when installing packages. This is a good practice for managing project dependencies. You can create and activate a virtual environment as follows:

```bash
python -m venv myenv
```
Then activate the virtual environment:

On Windows:

```bash
myenv\Scripts\activate
```
After activating the environment, install packages without requiring elevated permissions:

```bash
pip install package_name
```
