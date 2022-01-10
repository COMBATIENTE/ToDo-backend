- setps to run the server

1. python3.8 required
2. create vertualenv: python3.8 -m venv env_mame
3. activate the virtualenv: source/bin/activate
4. git clone https://github.com/COMBATIENTE/ToDo-backend.git
5. cd todo
6. python manage.py migrate
7. createsuperuser - python manage.py createsuperuser
7. got to browser and type localhost:8000
8. you can go localhost:8000/admin and can add user and task using django admin to test the apis working 

- apis endpoints:

1. task-list/ -> this will shows all the tasks of a user
2. task-detail/<str:pk>/ -> this is show details of a task
3. task-update/<str:pk>/ -> this will update a task of a user using task id and data for updatting that task
5. task-create/ -> this will create a task of user
6. task-delete/<str:pk>/ -> this will delete a task of user