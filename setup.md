Setup:
1. create a virtual env with name 'venv' using python3.9
2. Install all requirements with command 'pip install -r requirements.txt'
3. create a database in postgres
4. create .env file and add DATABASE_URL = 'postgresql+psycopg2://postgres_username:postgres_password@localhost/database_name'
5. activate environment by command 'source venv/bin/activate' 
6. Open python shell by command 'python3' and execute the function load_organisations in load_data/load_organisations
7. run server by command 'uvicorn main:app --reload'
8. Now the server will be up and running