streamlit run main_app.py --logger.level=debug 2>logs.txt && gunicorn api_app:app
