#Instawork-Fall-Internship-2022
 
Instructions:

git clone https://github.com/ArundeepChohan/Instaworks-Fall-Internship-2022.git

cd Instaworks-Fall-Internship-2022

py -m venv env

.\env\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

cd instawork

python manage.py runserver
