# **Intership Project**
<p>By Pongsakorn Anantarativakorn(Owner) from Kasetsart University<br>

* Goal:

  1.Connect all type of senser(in this project is voltage meter) that has RS485 communication port with internet using python
  
  2.Store the data in Postgres database using PostgresSQL lib in python(psycopg2)

Note:This project involve using hardware such volmeter,RS485 to RJ45 or USB convertor and copper wires.
* Requirment:
  
  Python:>3.7

  Volmeter(In this project, i use Elecnova dts1946-4p)

  RS485 to Ethernet converter(In this project, i use Protoss-PE11)

  copper wire
  
# **Getting Started**
typing the below line in terminal to install all requirements lib
```
pip install -r requirements.txt
```
 Client.py is the first file that my senior sent it to me as an example. It is an example how to use ModBusTCP libray
