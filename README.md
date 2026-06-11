#This project is represent a library#
This project help to handle a library activity. it hold tow tables: Books and Members.
this 2 tables contain all the data we need for the library
#The code for create docker with mysql is:#
docker run -d --name library -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 mysql

#The structure of the tables is:#
Books:
|id|title|auther|genre|is_available|borrowed_by_member_id|

Members:
|id|name|email|is_active|total_borrows|

#The structure of the folders is:#
library-api/ 
│ 
│ 
├── main.py 
├── database/ 
│   ├── db_connection.py 
│   ├── book_db.py 
│   └── member_db.py 
├── routes/ 
│   ├── book_routes.py 
│   ├── member_routes.py 
│   └── report_routes.py 
├── logs/ 
│   └── app.log 
│ 
├── README.md 
├── requirements.txt 
└── .gitignore 

#The rules of the system:#
-create a new book
-genre has to be one of Fiction/Non-Fiction/Science/history/Other
-create new member
-email should be uniq
-non active member can not borrow a book
-it immposible to borrow unaccessable book 
- member can not hold more than 3 books
- book can be return only by who borrwed it
- 
#Endpoint#
Books:
POST/books
GET/books
GET/books/{id} 
PUT/books/{id} 
PUT/books/{id}/borrow/{member_id} 
PUT/books/{id}/return/{member_id} 
- 
Mebers:
POST/members 
GET/members 
GET/members/{id} 
PUT/members/{id} 
PUT/members/{id}/deactivate 
PUT/members/{id}/activate 
- 
Reports:
GET/reports/summary 
GET/eports/books-by-genre 
GET/reports/top-member 

#Run instructions#
start the container
enter to main.py
and run it then enter to link and add the suffix '/docs'
- and then a app will open there you can run the routs
- 
#The flow of the system#
- the user enter a  title/author/genre then the system create a new book and define is_available=True, borrowed_by=NULL
- the genre should be Fiction/Non-Fiction/Science/history/Other else error will be back
- In create new member the user input should be name/email then  is_active_member=True, total_borrows=0 will be define
- the email of the new member should be uniq
- it immposible to borrow unaccessable book 
- member can not hold more than 3 books
- book can be return only by who borrwed it