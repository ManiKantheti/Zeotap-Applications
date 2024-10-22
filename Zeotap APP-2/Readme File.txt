# Weather Monitoring System

''' Overview'''
The Weather Monitoring System is a Python application that monitors real-time weather data for various cities. It alerts users when the temperature exceeds a defined threshold for consecutive updates and visualizes daily weather summaries and alerts.

''' Approach'''
1. **Install Required Libraries**: Ensure you have Python and the necessary libraries installed.
2. **Execute the Code**: Run the application using the terminal.
3. **Visualization and Alerts**: The application provides a visualization window and alerts in the terminal.

## Setup Instructions

""" Install Python and Required Libraries""
- Make sure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- Install the required libraries using pip:
""pip install pandas ,matplotlib, requests""


"""""""For exact application we need to run the main.py application."""""""

'''Execute the Code'''

Open your terminal and navigate to the directory where the code is located which is names as main.py.

Run the application with the following command:

""python main.py""



'''Application Behavior'''

Upon execution, a visualization window will open, displaying the current temperatures and alerts. Initially, there will be no alerts shown in the first window.

Important: You must close the first visualization window to start receiving alerts in the terminal.

Once the first window is closed, alerts will begin to display in the terminal, and a second visualization window will open, representing the alerts in a line graph.

Closing the second visualization window is mandatory to evaluate and display new alerts.

After closing the second window, the application will take some time to evaluate the alerts and display the visualizations again.

You can exit the application at any time by pressing Ctrl + C. This will trigger a sleep method before shutting down the application.


'''Adjusting Alert Frequency'''
For faster analysis of alerts, you can modify the UPDATE_INTERVAL variable at the start of the code to a smaller value (in seconds).




""Example Output""

The application will display:

A visualization window with current temperatures and alerts.

Alerts in the terminal after closing the first visualization window.

A line graph in the second visualization window showing triggered alerts.

'''Notes'''
Ensure that you have a stable internet connection to fetch weather data.

Adjust the configuration parameters in the code as needed to suit your monitoring requirements.


"""""""For exact bouns criteria application we need to run the main.py application."""""""


'''Bonus challenges'''

For the bouns challenges we need to run the extendedapp.py

Open your terminal and navigate to the directory where the code is located
which is named as extendedapp.py.

Run the application with the following command:

""python extendedapp.py""



'''License'''

This project is open-source and available under the MIT License.


Verify