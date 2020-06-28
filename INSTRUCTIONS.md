# Dash building heatmap instruction for VScode dev

1. right click on root folder > select open in terminal
2. `python -m venv .venv` to setup python virtual environment for this project. TIP: copy from here and right click in terminal to paste-and-execute.
3. Dialog should come up asking you want this env as interpreter for project: answer yes.
4. If no to (3) on blue ribbon at bottom of VSCODE, on left click on interpreter, chose the venv one you just created.
5. Might get some bits and both e.g. 'install pylint' etc. click install for them.
6. install package dependencies using `pip install -r requirements.txt` 



pip install -e . to put project in editable state. This fixes import issues.
TIP: If things break it may be easiect to just delete the whole project folder on your local drive and start over, cloning from repo