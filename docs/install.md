# Installation 

## Download 
Download and unzip latest release

## Open the Folder in Terminal

Right-click the folder "coffee-analysis" and select the option for your OS:

- **Windows** — Hold Shift + right-click → "Open in Terminal" or "Open PowerShell window here"
- **Mac** — Right-click → "New Terminal at Folder" *(if missing: System Settings → Keyboard → Shortcuts → Services → enable it)*
- **Linux** — Right-click → "Open in Terminal" *(exact wording varies by file manager)*

## Create a virtual environment
```bash
python3 -m venv venv
```
## Ensure you activate the environment
For windows terminal
```bash
venv\Scripts\activate
```
For other
```bash
source venv/Scripts/activate
```
or 
```bash
source venv/Scripts/activate
```
## Install requirements
Either using
```bash
python3 -m pip install -r "requirements.txt"
```
or 
```bash
py -m pip install -r "requirements.txt"
```
whichever version of python you are using
