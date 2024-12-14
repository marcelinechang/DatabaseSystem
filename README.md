# DatabaseSystem
> 2024 Fall Semester
>
> Course：Database System
> 
> Lecturer：Prof. CAI,Yun-Cheng
> 
> Name：Chang, Huai-Tzu
> 
> Markdown document：https://markdown.tw/

 # Video Presentations for Final Project #
[E-commerce Website - Maitokitsune](https://youtu.be/dQuAXjnWlO0) / [Code](https://github.com/marcelinechang/DatabaseSystem/tree/main/FinalProject_E-commerceWebsite-Maitokitsune)  / [Database ER Diagarm](https://app.eraser.io/workspace/Rsitlghy5ibG0Np2vQD6?origin=share)
 [![IMAGE ALT TEXT](./FinalProject_E-commerceWebsite-Maitokitsune/presentation.jpg)](https://youtu.be/dQuAXjnWlO0 "Presentaion Video of Final Project")
 * **Frontend (User Features)**:
   * User Registration/Login: Secure account creation and access.
   * Profile Management: Users can update their personal information.
   * Product Browsing and Shopping Cart: View products, add items to the cart, and modify cart contents.
   * Order Submission and History: Submit orders and review past orders.
* **Backend (Administrator Features)**:
   * Admin Registration/Login: Separate account system for administrators.
   * Dashboard for Sales and Inventory: Visual representation of top 5 best-selling products and products with low stock levels (≤ 5 units).
   * Product Management: Create, update, or delete products with ease.
   * Order Management: Administrators can view, edit, or cancel orders.
* **Additional Highlights**:
   * Password Encryption: Passwords are hashed using werkzeug.security's generate_password_hash before being stored in the database, ensuring user security.
   * User Feedback with Flash Messages: Utilizes Flask.flash and JavaScript for user notifications that automatically disappear after 2 seconds, enhancing user experience.
   * Dynamic Order Details: Order details are dynamically displayed using JavaScript for better interactivity.
   * Database Integrity: Foreign key relationships are utilized to maintain data consistency, ensuring cascaded deletion of related records.

 ![Screenshot](./FinalProject_E-commerceWebsite-Maitokitsune/er_diagram.png)

 # Video Presentations for Homework #

 **HW1** :
[What's Your Zodiac Sign](https://youtu.be/qHA9-f-NW98) / [Code](https://github.com/marcelinechang/DatabaseSystem/tree/main/HW1_ZodiacSign)   
* Used Flask and MySQL to build a web application and database  
* Implemented Create, Read, Update, and Delete (CRUD) functionality

**HW2** : [A Mock Database for a Pet Care Center - Furry Oasis](https://youtu.be/v_XagPPHcP4) / [Code](https://github.com/marcelinechang/DatabaseSystem/tree/main/HW2_PetCareCenter-FurryOasis)  / [Database ER Diagarm](https://app.eraser.io/workspace/V90JlxaSMDJYiLstcw9Z?origin=share&elements=Qjr-M0vQJZT9-Wzr4UENtg)  

* **Upcoming Appointments Section**:
   * Displays a list of scheduled appointments over the next 7 days, including today.
   * Includes relevant details such as appointment date, time, and pet information.
* **Appointment CRUD Features Features**:
   * Options to make new appointments for both existing and new pets.
   * Interactive forms include fields for pet and owner details, type of service (grooming, boarding, medical), and appointment scheduling preferences.
* **Filtering Options**:
   * Allows filtering of appointments by species and type of service.
 
![Screenshot](./HW2_PetCareCenter-FurryOasis/er_diagram.png)

**HW3** : [Tell Me About U](https://youtu.be/y3Db4-Dd6WQ) / [Code](https://github.com/marcelinechang/DatabaseSystem/tree/main/HW3_TellMeAboutU)  
* Creating a NoSQL database using MongoDB.
* Implementing Create, Read, and Update functionality.
* Developing a multi-page web application, with separate pages for adding and updating data.
* Adding buttons for querying data and toggling the display or hiding of all records.
* Designing the update page to dynamically display content based on the selected data.

**HW4** : [Personal Preference Information](https://youtu.be/ILfGN8aaCIs) / [Code](https://github.com/marcelinechang/DatabaseSystem/tree/main/HW4_PersonalPreferenceInformation)  
* Implements a confirmation dialog to prevent accidental deletions, ensuring data integrity.
* Allows filtering of records based on selected fields. Users can select multiple fields for precise results, or leave all fields unselected to apply a global search.
* Automatically adapts to the available fields in each record, enabling efficient and relevant modifications.

 # Notes #

## How to Install MongoDB on a MacBook Pro with M3 Chips ##

1. **Download and Install MongoDB Compass (GUI) for Apple Silicon:**
   - Visit: [MongoDB Compass Download](https://www.mongodb.com/try/download/compass)
   - The version I used is MacOS arm64 (M1) (11.0+) 1.44.5 (Stable).
   - Reference: [How to Install MongoDB Compass on Mac | Install MongoDB Compass on macOS (2024)](https://youtu.be/sSoVyHap3HY?si=WS7P00NhEJW1M2Ez)

2. **Download the MongoDB Community Server for Apple Silicon:**
   - Visit: [MongoDB Community Server Download](https://www.mongodb.com/try/download/community)
   - The version I used is MacOS arm64 8.0.1.
   - Reference: [MongoDB Installation on MacBook Pro with Apple Silicon Chip (M3)](https://medium.com/@meetwithIT/mongodb-installation-on-macbook-pro-with-apple-silicon-chip-m3-f1fea73da739)
    
3. **Creating a New Connection in MongoDB Compass**

## Free ER Diagram Tool ##

* [draw.io](https://www.drawio.com/)
* [lucidchart](https://www.lucidchart.com/pages/)
* [DiagramGPT](https://www.eraser.io/diagramgpt)
