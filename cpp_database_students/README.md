# Запросив в чату "Згенеруй мені C++ технічне завдання" так вот:

Project Title:
Student Information Management System

Project Description:
Develop a C++ program that enables the management of student data and their grades.

============================================

# Functional Requirements:

1. Addition of Students:
- The program should allow the addition of new students to the database.
- Basic information such as name, surname, group number, and student ID should be stored for each student.

2. Grade Entry:
- The program must provide the ability to input grades for each student for various subjects.
- Grades should be stored in a suitable format and linked to the specific student.

3. Viewing and Editing Information:
- Users should be able to view information about all students, including their grades.
- Implement the ability to edit student information or their grades.


4. Calculation of Average Grade:
- The program should calculate the average grade for each student and display this information.

5. Statistics Output:
- Implement the ability to output statistics about grades, such as the average grade per group, median, variance, etc.

# Non-functional Requirements:

1. Programming Language:
- The entire project should be implemented using the C++ programming language.

2. Graphical Interface:
- Optionally, a text-based or console graphical interface can be added for user interaction.

3. Data Storage:
- Data should be stored in a text file to allow for saving and restoring information between sessions.

4. Error Handling:
- The program should handle user input gracefully and provide error messages in case of any issues.

# Additional Features:

1. Sorting:
- Implement the ability to sort the list of students based on various criteria such as name, surname, average grade, etc.

2. Student Groups:
- Allow the grouping of students and output statistics for each group.

============================================

Для запуску потрібно:

- docker run --name postgres -e POSTGRES_PASSWORD= ######## -p 5432:5432 -d postgres:latest
- make
- ./MyProject
- make clear

============================================

Джерела які використовував:

- Бібліотека sstream
- БД Postgres https://habr.com/ru/articles/322966/
- Бібліотека libpg https://www.postgresql.org/docs/7.2/libpqplusplus.html


--------------------------------------------
--------------------------------------------

Назва проекту:
Система керування інформацією про студентів

Опис проекту:
Розробити програму на мові програмування C++, яка дозволяє керувати даними про студентів та їхні оцінки.

============================================

# Функціональні вимоги:
1. Додавання студентів:
- Програма повинна дозволяти додавати нових студентів до бази даних.
- Зберігати базову інформацію, таку як ім'я, прізвище, номер групи та номер студентського квитка, для кожного студента.
2. Введення оцінок:
- Програма повинна надавати можливість вводити оцінки для кожного студента за різними предметами.
- Оцінки повинні зберігатися в відповідному форматі та пов'язуватися з конкретним студентом.
3. Перегляд та редагування інформації:
- Користувач повинен мати можливість переглядати інформацію про всіх студентів, включаючи їхні оцінки.
- Реалізувати можливість редагування інформації про студента або його оцінок.
4. Обчислення середньої оцінки:
- Програма повинна розраховувати середню оцінку для кожного студента та виводити цю інформацію.
5. Виведення статистики:
- Реалізувати можливість виведення статистики щодо оцінок, такої як середня оцінка за групою, медіана, дисперсія і т.д.
# Нефункціональні вимоги:
1. Мова програмування:
- Весь проект повинен бути реалізований мовою програмування C++.
2. Графічний інтерфейс:
- На вибір може бути доданий текстовий або консольний графічний інтерфейс для взаємодії з користувачем.
3. Збереження даних:
- Дані повинні зберігатися в текстовому файлі для можливості збереження та відновлення інформації між сеансами роботи.
4. Обробка помилок:
- Програма повинна гідно обробляти введення користувача та надавати повідомлення про помилки у разі їх виникнення.
# Додаткові функції:
1. Сортування:
- Реалізувати можливість сортування списку студентів за різними критеріями, такими як ім'я, прізвище, середня оцінка і т.д.
2. Групи студентів:
- Дозволити розподіл студентів за групами та виведення статистики для кожної групи.