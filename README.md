\# SupportPilot – AI Ticket Resolution Agent



SupportPilot is an AI-powered IT support ticket processing system that classifies incoming IT support tickets, identifies their severity, assigns priority, and displays ticket analytics through a web dashboard.



\## Features

\- Ticket submission through a web interface

\- Automatic classification into Network, VPN, Password, Software, and Hardware

\- TF-IDF text feature extraction

\- Logistic Regression classification

\- Prediction confidence display

\- Rule-based severity detection

\- Automatic priority assignment (P1–P4)

\- SQLite database storage

\- Ticket processing time measurement

\- Dashboard analytics

\- Data exploration and preprocessing



\## Technology Stack

\- Python

\- Flask

\- Pandas

\- Scikit-learn

\- TF-IDF

\- Logistic Regression

\- SQLite

\- HTML and Bootstrap

\- Joblib



\## Project Structure

```text

SupportPilot/

├── app.py

├── classifier.py

├── database.py

├── severity.py

├── train\_model.py

├── eda.py

├── preprocess.py

├── requirements.txt

├── tickets.csv

├── tickets\_cleaned.csv

├── models/

│   └── ticket\_classifier.pkl

├── templates/

│   └── index.html

└── README.md

```



\## Installation



Clone the repository:



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd SupportPilot

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\## Run the Application



```bash

python app.py

```



Open http://127.0.0.1:5000/ in your browser.



\## Machine Learning Workflow

1\. Employee submits an IT support ticket.

2\. TF-IDF converts ticket text into numerical features.

3\. Logistic Regression predicts the ticket category.

4\. Rule-based logic identifies ticket severity.

5\. Priority is assigned based on severity.

6\. Ticket information is stored in SQLite.

7\. Dashboard displays ticket analytics.



\## Severity and Priority Mapping



| Severity | Priority |

|---|---|

| Critical | P1 |

| High | P2 |

| Medium | P3 |

| Low | P4 |



\## Model Evaluation



The current model achieved 90% accuracy on a 10-sample test split from a 50-row synthetic dataset. This is a preliminary result and does not establish real-world performance.



\## Limitations

\- The classifier uses a small synthetic dataset.

\- Prediction confidence may be low for unfamiliar descriptions.

\- Severity detection is keyword-based, not machine learning.

\- This is a project prototype, not a production IT support system.



\## Project Status



Milestone 1 – Ticket Processing and Classification.

