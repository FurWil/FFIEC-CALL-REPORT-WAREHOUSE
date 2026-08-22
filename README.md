# FFIEC-CALL-REPORT-WAREHOUSE
## Setup

### 1. Clone the repository

git clone <repository-url>

### 2. Create environment file

cp .env.example .env

### 3. Start PostgreSQL

docker compose up -d

### 4. Install Python dependencies

pip install -r requirements.txt

### 5. Run the ingestion pipeline

python python/download.py
