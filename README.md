## Overview
A Local ITS, designed to work offline with hugging face models based on Ruffle&Riley (Schmucker et al., 2024), created as a requirement for conducting inference benchmarks for a final year research project titled "Local and Personalized Large Language Models in Intelligent Tutoring Systems" conducted at the University of Guyana towards the Bachelor's in Computer Science

## Installation and setup
#### Front end
Ensure that nodejs and npm is installed: https://nodejs.org/en/download, then run within root directory
```
npm i
```
#### Backend

Ensure that python is installed. It is advised that you create a virtual env either using conda or python virtualenv. Then run:

```
cd server
pip install -r requirements. txt
```

## Run and usage

#### Terminal 1
Run chat module using:
```
cd server/flaskr/chat
watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM \
                                                        python app.py
```

#### Terminal 2
Run flask api using:
```
cd server
python -m flaskr
```

#### Termainal 3
Run angular application using:
```
ng serve -o
```

## Notes on Usage
It is required that you place relevant content within server/flaskr/storage/pdfs. Content utilised within the course of the study is property of the University of Guyana and therefore, cannot be publicly shared. Hence for usage of the system, content must be provided.

Secondly, in line 162 in server/flaskr/chat/app.py, replace the hardcoded prompt with a relevant prompt for you content. Note that a relevant tutoring script will have to be created using your own content. The module for generating a tutoring script is located in /script_generation. See further section for usage

## Script Generation
Script generation module can be ran as follows, assuming all dependencies in requirements.txt is installed. See Installation and setup.

Before running change hardcoded path in script_generation/helpers.py on line 66 to desired path of content. Then run:
```
python -m script_generation
```

## Current Status 
At current executables cannot be exported. Pyinstaller encounters errors on compiling pytorch. Do note that this and all afore mentioned instructions have only been tested on linux mint. 

## References
- Schmucker, R., Xia, M., Azaria, A., & Mitchell, T. (2024, July 2). Ruffle &Riley: Insights from Designing and Evaluating a Large Language Model-Based Conversational Tutoring System. Springer.com. https://doi.org/10.1007/978-3-031-64302-6_6
- Ruffle&Riley Github repo: https://github.com/rschmucker/ruffle-and-riley


