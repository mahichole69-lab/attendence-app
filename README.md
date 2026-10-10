# CI/CD Pipeline for Attendance Application

## 1. Project Overview
The Attendance Management System is a web application developed using Python and Flask. It helps manage student registration, attendance records, attendance percentages, and date-wise attendance details.

The project aims to automate application deployment using a CI/CD pipeline.

## 2. Project Objectives
- Develop a web-based attendance management application.
- Register students and manage attendance records.
- Calculate attendance percentages.
- Store and manage source code using GitHub.
- Automate the build and deployment process using AWS CI/CD services.

## 3. Technologies Used
- Python
- Flask
- HTML
- CSS
- JavaScript
- Git and GitHub
- AWS CodePipeline
- AWS CodeBuild
- Amazon EC2 or Amazon S3 for deployment, depending on the final implementation

## 4. Application Features
- Student Registration
- Mark Attendance
- Attendance Percentage Calculation
- Date-wise Attendance Records
- Web-based User Interface

## 5. AWS Services
### AWS CodePipeline
Used to create and manage the CI/CD workflow.

### AWS CodeBuild
Used to build and test the application.

### GitHub
Used to store and manage the application source code.

### Deployment Service
The application will be deployed using the AWS hosting service selected during implementation.

## 6. Project Workflow
1. Develop the attendance application using Python and Flask.
2. Store the source code in GitHub.
3. Configure AWS CodeBuild.
4. Create an AWS CodePipeline.
5. Configure the deployment stage.
6. Test the application after deployment.

## 7. Project Structure
attendance-app/
- app.py
- requirements.txt
- templates/
  - index.html
- static/
  - script.js
  - style.css
- data/
- README.md

## 8. How to Run Locally
1. Install Python.
2. Open the project folder in the terminal.
3. Install the required dependencies:

   pip install -r requirements.txt

4. Run the application:

   python app.py

5. Open the local address displayed in the terminal in your web browser.

## 9. Project Outcome
The project demonstrates the development of a Flask-based attendance management application and the implementation of an automated CI/CD deployment workflow using GitHub and AWS services.

## 10. Author
Mahesh Shivaji Chole
