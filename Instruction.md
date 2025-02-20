# Installation and Setup Guide

This guide provides step-by-step instructions to build and run the Dockerized Django application on any machine.

---

## **Prerequisites**
Before proceeding, ensure the following are installed:

- **Docker**: [Download & Install Docker](https://www.docker.com/get-started)
- **Docker Compose** (if using `docker-compose.yml`)
- **Git** (to clone the repository)

---

## **Step 1: Clone the Repository**
Clone the project repository to your local machine:

```sh
git clone https://github.com/arvind0603/receipt-processor-challenge.git
cd receipt_processor
```

---

## **Step 2: Run with Docker Compose (If Applicable)**
If using `docker-compose.yml`, start all services with:

```sh
docker-compose up -d
```

To rebuild after changes:
```sh
docker-compose up --build -d
```

To stop the services:
```sh
docker-compose down
```

---


**Check if the container is running:**
```sh
docker ps
```

---

## **Step 3: Access the Django Application**
Once the container is running, open a browser and visit:

👉 **http://localhost:8000**

If running APIs, use **Postman**, **Insomnia** or **cURL** to test endpoints.

**Add Receipt:** http://127.0.0.1:8000/receipts/process

```sh
curl --request POST --url http://127.0.0.1:8000/receipts/process --header "Content-Type: application/json" --data '{"retailer": "Target", "purchaseDate": "2022-02-01", "purchaseTime": "23:00", "items": [{"shortDescription": "Mountain Dew 12PK", "price": "6.49"},{"shortDescription": "Emils Cheese Pizza", "price": "12.25"},{"shortDescription": "Knorr Creamy Chicken", "price": "101.26"},{"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},{"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}], "total": "135.35"}'

```

**Get Points:** http://127.0.0.1:8000/receipts/{UUID}/points
```sh
curl --request GET --url http://127.0.0.1:8000/receipts/bbe739c7-d778-44b3-af00-a79dec61997c/points
```
---

## **Quick run from the Insomnia (API calls)**
![Insomnia2025-02-1920-02-08-ezgif com-resize](https://github.com/user-attachments/assets/385f542d-c782-40fc-a651-311afd7c58a9)

---

