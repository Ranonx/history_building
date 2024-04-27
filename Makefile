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

# runs data collector
collect:
	python src/data_collector/collector.py

# runs data analyzer
analyse:
	python src/data_analyser/analyzer.py

# runs test route.py
route:
	python -m unittest tests/test_routes.py
