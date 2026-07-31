
## Project Description
Open Source software solution for Car Wash CRM

- create ticket
- assign worker
- view/modify existing tickets
- manage orders
- extract data (soon)
- calculate reward for workers (soon)

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

## Access API documentation
```bash
http://142.93.195.38/docs
```
