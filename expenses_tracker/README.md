# EXPENSES TRACKER
#### Video Demo:  <https://youtu.be/AF6TDS_D1SM?si=kDN61uBHR11P6yxF>
#### Description:

Task Expenses is a comprehensive web-based expense management application developed using the Flask framework. The application aims to streamline expense tracking, providing users with a user-friendly interface to manage and analyze their financial transactions effectively.

## Project Overview

The main components of the project include:

- **app.py:** This is the main Python file containing the Flask application and route definitions. It handles user authentication, routing, and interactions with the SQLite database.

- **helpers.py:** The helpers module includes various utility functions used throughout the application. It includes functions for password hashing, login validation, and error handling.

- **templates:** The templates folder contains HTML templates used by Flask for rendering different pages. These templates provide the structure for the application's frontend.

- **expenses.db:** This SQLite database file stores user information, expenses, and expense categories. It's essential for persistently storing user data and maintaining the application's state.

## Features

### User Authentication

The application implements secure user authentication using hashed passwords. Users can register for an account, log in, and log out securely.

### Expense Tracking

Users can add new expenses by specifying the category and amount. The application records these expenses and provides a summary on the dashboard.

### Expense History

The "expense_history" route allows users to view a detailed table of their expense history. It includes information such as category, amount, and date for each recorded expense.

### Dashboard

The dashboard, accessible through the root route ("/"), provides a summary of the user's overall financial status. It includes total expenses for each category, the most expensive category, total expenses, and the user's cash balance.

### Design Choices

#### CS50 Library

The application utilizes the CS50 library for database interactions. This choice was made for its simplicity and effectiveness in handling database operations, allowing for a more straightforward implementation of user and expense-related queries.

#### Flash Messages

Flash messages are used to provide real-time feedback to users after certain actions, such as successful logins, registrations, or added expenses. This enhances the user experience by providing clear and immediate feedback.


