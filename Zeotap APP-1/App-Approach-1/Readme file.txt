"""""""""""""""""""""""""""""""""""""""""""Rule Evaluator App""""""""""""""""""""""""""""""""""""""""""""""""

This is a Flask-based web application that allows users to create, combine, and evaluate rules using a simple rule engine interface. The rules are stored in an SQLite database, and users can interact with the application through a web interface.

"""""""Requirements"""""""
To run this application, you need to have Python and pip installed on your machine. The following Python packages are required:
""""
-Flask
-SQLite3 (included with Python standard library)
-JSON (included with Python standard library)
""""

You can install Flask using pip:

-------pip install Flask


""""""Running the Application"""""""

Start the Flask app:

Open a terminal and navigate to the directory where app.py is located.

Run the application using the command:

-----python app.py



""""""Database Initialization:""""""

Upon running the app, it will automatically create a SQLite database file named rules.db in the same directory if it does not already exist.


"""""""Access the Application:"""""""

Open your web browser and go to the following URL:

---------http://127.0.0.1:5001



This will redirect you to the main page of the Rule Evaluator app.
Application Features


""""Create Rules:""""

-Enter a rule in the input field and click the "Create Rule" button.
-A popup will confirm that the rule has been created successfully.
-You can create multiple rules, which will be stored in the rules.db file.

"""""Combine Rules:"""""

-After creating sufficient rules, click the "Combine Rules" button.

-The application will fetch and display all rules from the database combined into a single rule format.

""""""Evaluate Rules:""""""

-Enter the context data in JSON format in the specified input area.
-Click the "Evaluate Combined Rule" button to evaluate the combined rule against the provided context.
-The result will be displayed on a new HTML page.


"""""""File Structure"""""""
/<project_directory>
│
├── app.py                   # Main application file
├── rules.db                 # SQLite database file (created automatically)
├── templates/               # HTML templates
│   ├── index.html           # Main page template
│   └── result.html          # Result page template
└── static/                  # Static files (CSS, JS)
    ├── styles.css           # Stylesheet for the application
    └── script.js            # JavaScript for handling user interactions


"""Conclusion""""

This application provides a simple yet effective way to manage and evaluate rules through a web interface. 
