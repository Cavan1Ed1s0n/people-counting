# People Counting (FastAPI + Next.js + PostgreSQL)

Detects people in uploaded images, draws boxes, stores results, and provides a paginated/searchable history UI.

## Stack
- Backend: FastAPI, SQLAlchemy, Pydantic
- Frontend: Next.js (App Router)
- Database: PostgreSQL
- Detection: Yolov8 Ultralytics
- Deployment: Docker Compose
- Monitoring stack (Prometheus + Grafana + Loki + Promtail + cAdvisor)

## Run

1. Clone repo 
```bash
cd people-counting
```
2. Run `docker-compose up -d`.  
3. Visit `http://localhost:3000` to upload an image; results appear with bounding boxes + count.  
4. Visit `http://localhost:3000/history` to browse/search/filter past records (pagination included).  

## Run in remote server
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
### Monitoring
Grafana → http://remote-server-ip:3001 (default user: admin, password: admin)

Prometheus → http://remote-server-ip:9090

cAdvisor (container metrics) → http://remote-server-ip:8080

Loki (log storage) → http://remote-server-ip:3100

Promtail → pushes logs from containers → Loki
### Dashboards
Login to Grafana → http://remote-server-ip:3001

Add data sources:

+ Prometheus: http://prometheus:9090

+ Loki: http://loki:3100

The system monitor
- **CPU / Memory / Network usage** per container (via cAdvisor + Prometheus)  
- **Backend & frontend HTTP metrics** (if you expose `/metrics`)  
- **Centralized logs** (Promtail → Loki → Grafana) 
