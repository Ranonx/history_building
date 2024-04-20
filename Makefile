.PHONY: run clean-db

# Run the Flask application
run:
	python src/app.py

# Clean the SQLite database
clean:
	rm -f instance/database.db

# Update the requirements.txt
update:
	pip freeze > requirements.txt