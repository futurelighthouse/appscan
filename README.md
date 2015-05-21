#AppScan Platform

###1. Introduce
This is an app check platform for detecting security problem, which is based on [Drozer](https://github.com/mwrlabs/drozer) and [Androguard](https://github.com/androguard/androguard)
###2. Env
To run the code, you may need to prepare the following things,   


1. __Python 2.7__ 

2. __Django 1.9__   

3. __Drozer 2.3.4__ (to configue it, you can refer to [Running on the     edge](https://github.com/mwrlabs/drozer/wiki/Running-on-the-edge) and then set Drozer as a system environment variable)
 
4. __Androguard__   

To make it easily, you can use [Santoku](https://santoku-linux.com/) and just need install Django   

###3. Run

--1. At first, prepare a mobile or AVD, install drozer agent and keep the agent on.

--2. Run "python manage.py runserver" to start Django service

--3. Upload an Apk by access "http://127.0.0.1:8000/index"

###4. To be contined
