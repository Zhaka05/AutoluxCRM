
## Project Description
Open Source software solution for Car Wash CRM

- create ticket
- assign worker
- extract data
- calculate reward for workers
- view/modify existing tickets
- manage orders

## Project Start

Download dependencies:

Create your virtual environment

```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --reload
```

The server will start in port 8000. To check:

```bash
curl localhost:8000
```