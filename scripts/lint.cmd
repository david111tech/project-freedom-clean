@echo off
echo Running lint...
flake8 src warhead
black --check src warhead
echo Linting Completed.
