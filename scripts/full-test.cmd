@echo off
echo Running Full Test Suite...
pytest --maxfail=1 --disable-warnings -q
coverage run -m pytest
coverage html
echo Full Suite Completed.
