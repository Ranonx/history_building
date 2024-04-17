.PHONY: run clean-db

# Run the Flask application
run:
	python src/app.py

# Clean the SQLite database
clean-db:
	rm -f instance/mydatabase.db