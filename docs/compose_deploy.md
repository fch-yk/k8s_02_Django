# Deploy using Docker Compose

- Build images and start the application set:

```bash
docker compose up -d --build
```

- Run migrations:

```bash
docker exec -it django_site python manage.py migrate
```

- Createa a superuser:

```bash
docker exec -it django_site python manage.py createsuperuser
```

[Back to README](../README.md)
