# Minikube deploy

## Prerequisites

- [kubectl](https://kubernetes.io/docs/tasks/tools/);
- Virtualization software, for example: HyperV, Docker (go [here](https://minikube.sigs.k8s.io/docs/drivers/) for more);
- [Minikube](https://minikube.sigs.k8s.io/docs/start/);
- [Helm](https://helm.sh/docs/intro/install/);

## Cluster start

Run:

```bash
minikube start
```

Verify that the cluster is running:

```bash
kubectl cluster-info
```

## Adding a PostgreSQL  database

_Note_: For production installation, remember to replace the formal values (like `replace_me`) with real values of your choice.

- Install the PostgreSQL Helm Chart:

```bash
helm install django-db --set auth.postgresPassword=replace_me oci://registry-1.docker.io/bitnamicharts/postgresql
```

where `django-db` is a release name;

- Verify that the `django-db-postgresql-0` pod is running and ready:

```bash
kubectl get pods
```

Verify that the `data-django-db-postgresql-0` persistent volume claim was created:

```bash
kubectl get pvc
```

- Create the user and the database:

Connect to the pod:

```bash
kubectl exec -it django-db-postgresql-0 -- /opt/bitnami/scripts/postgresql/entrypoint.sh /bin/bash
```

Start the `psql` utility:

```bash
PGPASSWORD=replace_me psql
```

Create a database:

```bash
CREATE DATABASE k8s_db;
```

Create a user:

```bash
CREATE USER k8s_user WITH ENCRYPTED PASSWORD 'replace_me';
```

Change the user's role to `SUPERUSER`:

```bash
ALTER USER k8s_user WITH SUPERUSER;
```

Exit the `psql` utility:

```bash
exit
```

Exit the pod:

```bash
exit
```

## Set the environmental variables

### Configmap environmental variables

Use ConfigMaps for not-secret configuration data.

- Go to the `k8s_minikube` folder:

```bash
cd k8s_minikube
```

- Create the `django-config` configmap:

```bash
kubectl create -f configmap.yaml
```

### Secret environmental variables

Use Secrets for things that are actually secret, like API keys and credentials.

_Note_: for production installation, remember to replace the formal values (like `replace_me`) with real values of your choice.

- Encode the secret key:

```bash
echo -n 'replace_me' | base64
```

- The output will be like this:

```bash
cmVwbGFjZV9tZQ==
```

- Create the `secret.yaml` file and fill it up like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: django-secret
type: Opaque
data:
  secret_key: cmVwbGFjZV9tZQ==
stringData:
  database_url: postgres://k8s_user:replace_me@django-db-postgresql:5432/k8s_db
```

- Apply the secret:

```bash
kubectl apply -f secret.yaml
```

## Organize the `media` storage

Create the `vol-django` Persistent Volume and the `pvc-django` Persistent Volume Claim:

```bash
kubectl create -f pv_pvc.yaml
```

Crete the `chown-unit-media` job to change the `/media` folder owner to `unit`:

```bash
kubectl create -f chown_unit_media.yaml
```

## Deployment and service configuration

- Apply the deployment and service configuration

```bash
kubectl apply -f deploy.yaml
```

- Verify that the `django-service` is created and the `django-deployment` pods are running:

```bash
kubectl get all
```

## Migrations execution

- Create the `django-migrate` job:

```bash
kubectl apply -f migrate.yaml
```

- Verify that the `django-migrate` job has been created:

```bash
kubectl describe job django-migrate
```

- Verify that migrations are completed:

Find out the name of the pod that was created by the job. The name will begin with `django-migrate`:

```bash
kubectl get pods
```

Print the pod's logs:

```bash
kubectl logs django-migrate-jlj8p
```

where `django-migrate-jlj8p` is the pod's name

_Note_: The job and the pod will be deleted in 120 seconds according to the `spec.ttlSecondsAfterFinished` parameter in the `migrate.yaml` manifest file.

See also: [How to deploy the latest version](#how-to-deploy-the-latest-version).

## Superuser creation

- Find out which `django-deployment` pods are running:

```bash
kubectl get pods
```

- Connect to any `django-deployment` pod:

```bash
kubectl exec -it django-deployment-688676fd6-dl7q5 -- bash
```

where `django-deployment-688676fd6-dl7q5` is the pod's name;

Create a superuser:

```bash
python manage.py createsuperuser
```

Exit the pod:

```bash
exit
```

## Ingress installation

- Enable the NGINX Ingress controller:

```bash
minikube addons enable ingress
```

- Verify that the NGINX Ingress controller is running and ready:

```bash
kubectl get pods -n ingress-nginx
```

- Create the Ingress object:

```bash
kubectl apply -f ingress.yaml
```

- Verify that the Ingress is applied:

```bash
kubectl get ingress
```

- Get the minikube IP:

```bash
minikube ip
```

- Edit the `hosts` file, which is usually situated in the `C:\Windows\System32\drivers\etc\` directory (for Windows 11). Add the mapping of the minikube IP to the `star-burger.test` host name. For example:

```config
172.26.28.91 star-burger.test
```

where `172.26.28.91` is the minikube IP

- Verify that the website works:

```bash
curl star-burger.test
```

## Clearing the session store

Create the `django-clearsessions` cronjob, which will run monthly:

```bash
kubectl create -f clearsessions.yaml
```

- Verify that the `django-clearsessions` cronjob is created:

```bash
kubectl get cronjob
```

- You can trigger the `django-clearsessions` cronjob manually:

```bash
kubectl create job --from=cronjob/django-clearsessions clear-job
```

where `clear-job` is a job name;

## Usage

Open the [website](http://star-burger.test/).

## How to change the environmental variables

- Edit the `configmap.yaml` file;
- Apply the `configmap.yaml` file changes:

```bash
kubectl apply -f configmap.yaml
```

- Restart the deployment:

```bash
kubectl rollout restart deployment django-deployment
```

## How to deploy the latest version

_Note_: remember to replace `fchef` with your login at [Docker Hub](https://hub.docker.com/) in the commands below and in the following files: `deploy.yaml`, `clearsessions.yaml`, `migrate.yaml`, `chown_unit_media.yaml`.

- Make changes;
- Commit;
- Go to the `backend_main_django` folder:

```bash
cd backend_main_django
```

- Build images:

```bash
docker build . -t fchef/k8s_django:latest -t fchef/k8s_django:$(git log -1 --pretty=%h)
```

- Return to the root project folder

```bash
cd ..
```

- Verify that images have been built. You should see two `fchef/k8s_django` images in the list: the first image will be with a tag `latest`, and the second image will be with the commit hash as a tag. Both of these images will have the same `IMAGE ID`.

```bash
docker image ls
```

- Push the images to [Docker Hub](https://hub.docker.com/):

```bash
docker push --all-tags fchef/k8s_django
```

- Go to the `k8s_minikube` folder:

```bash
cd k8s_minikube
```

- [Execute migrations](#migrations-execution);

- Restart the deployment:

```bash
kubectl rollout restart deployment django-deployment
```

- Verify that all `django-deployment` pods are running and ready:

```bash
kubectl get pods
```

## How to deploy a certain version

- Syntax:

kubectl set image deployment/{deployment_name} {container_name}={image_name}:{image_tag}

- Example:

kubectl set image deployment/django-deployment django-web=fchef/k8s_django:81d48a3

## How to stop the minikube cluster

Run:

```bash
minikube stop
```

## How to delete the minikube cluster

Run:

```bash
minikube delete
```

[Back to README](../README.md)
