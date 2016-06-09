# Developing Django in VS2015

## Install MySQL

It comes with excellent support for .Net. Developer web installer will install VS components. Install MySQL Community Editions, then:

	conda install mysql-connector-python
	conda install pymysql

## Create new project

Virtual envs are hard to set up when certain packages are missing. Use conda to install django and additional tools.



To run manage.py command, open a powershell in the project's directory and run 

	 .\djangotest-env\Scripts\python.exe manage.py