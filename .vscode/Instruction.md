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

## **Step 5: Run with Docker Compose (If Applicable)**
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

## **Step 6: Access the Django Application**
Once the container is running, open a browser and visit:

👉 **http://localhost:8000**

If running APIs, use **Postman** or **cURL** to test endpoints.

---

With these steps, anyone can build and run the Dockerized Django application on their machine effortlessly! 🚀

