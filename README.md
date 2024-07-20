# UtAgro

## Description
This Django project serves as [describe what your project does or aims to achieve]. It is built using the Django web framework, providing [mention any specific functionalities or features].

## Installation
1. Make sure you have Python and pip installed. You can download them from [Python's official website](https://www.python.org/downloads/).
2. Clone this repository to your local machine.
    ```bash
    git clone https://github.com/jhobs007/uAg_BackEnd_API.git
    ```
3. Navigate to the root directory where manage.py is located.
    
4. Create virtual env (For Linux 2nd For windows).
    ```bash
    virtualenv env 
    ```
    ```bash
    python -m vnev env
    ```
5. Activate virtual env(Linux | Windows).
    ```bash
    source env/bin/activate
    ```
    ```bash
     env\Scripts\activate
    ```
5. Install dependencies.
    ```bash
    pip install -r requirements.txt
    ```
6. Migrate.
    ```bash
    python manage.py migrate
    ```
7. Add .env in root directory
    

## Usage
1. Create a Django superuser.
    ```bash
    python manage.py createsuperuser
    ```
2. Run the development server.
    ```bash
    python manage.py runserver
    ```
3. Open a web browser and go to [http://localhost:8000](http://localhost:8000) to view the application.
4. You can access the Django admin panel at [http://localhost:8000/admin](http://localhost:8000/admin) and log in with the superuser credentials created in step 1.

## Configuration
- You can configure the project settings in `settings.py` file located in the project's main directory.
- Make sure to set up the database settings according to your preference (default is SQLite).

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a new Pull Request.

## License
[Choose an appropriate license for your project and mention it here.]

## Credits
[Give credit to any contributors, libraries, or resources you've used in your project.]
