gunicorn api_app:app --daemon && streamlit run main_app.py && echo "Deployed and Done"
