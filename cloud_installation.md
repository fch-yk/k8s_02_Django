# Cloud installation

The project was deployed in the [Yandex Cloud](https://cloud.yandex.com/en/) cluster.

The website can be accessed [here](https://edu-focused-keller.sirius-k8s.dvmn.org/) for a while.

It is assumed that the cloud cluster already exists. The project deployment in the cloud cluster depends on the cloud service provider and the cluster configuration.

## Key features of the cloud installation

- The project was installed in the `edu-focused-keller` namespace;
- The project uses a database from the [Managed Service for PostgreSQL](https://cloud.yandex.ru/docs/managed-postgresql/quickstart?from=int-console-help-center-or-nav);
- The [Yandex Application Load Balancer](https://cloud.yandex.ru/docs/application-load-balancer/concepts/?from=int-console-help-center-or-nav) directs traffic to the service;
- The project uses [PVC](https://cloud.yandex.com/en/docs/managed-kubernetes/operations/volumes/dynamic-create-pv#create-pvc) to store media;
- The website is run under the `unit` user, that is why it is necessary to change the owner of the `/media` folder, which is linked to the Persistent Volume; see [How to organize the `media` storage](#how-to-organize-the-media-storage)

## How to set the environmental variables

### How to set configmap environmental variables

Use ConfigMaps for not-secret configuration data.

- Go to the `k8s_cloud` folder:

```bash
cd k8s_cloud
```

- Create the `django-config` configmap:

```bash
kubectl apply -f yc_configmap.yaml
```

### How to set secret environmental variables

Use Secrets for things which are actually secret like API keys, credentials.

_Note_: for production installation, remember to replace the formal values (like `replace_me`) with real values of your choice.

- Go to the `k8s_cloud` folder:

```bash
cd k8s_cloud
```

- Encode the secret key:

```bash
echo -n 'replace_me' | base64
```

- The output will be like this:

```bash
cmVwbGFjZV9tZQ==
```

- Create the `yc_secret.yaml` file and fill it up like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: django-secret
type: Opaque
data:
  secret_key: cmVwbGFjZV9tZQ==
stringData:
  database_url: postgres://replace_user:replace_password@replace_host:replace_port/replace_db
```

- Apply the secret:

```bash
kubectl apply -f yc_secret.yaml
```

## How to organize the `media` storage

- Go to the `k8s_cloud` folder:

```bash
cd k8s_cloud
```

Create the `pvc-django` Persistent Volume Claim:

```bash
kubectl create -f yc_pvc.yaml
```

Crete the `chown-unit-media` job to change the `/media` folder owner to `unit`:

```bash
kubectl create -f yc_chown_unit_media.yaml
```

If the `django-deployment` deployment was not applied yet, apply it:

```bash
kubectl apply -f yc_deploy.yaml
```

## How to change the environmental variables

- Go to the `k8s_cloud` folder:

```bash
cd k8s_cloud
```

- Edit the `yc_configmap.yaml` file;
- Apply the `yc_configmap.yaml` file changes:

```bash
kubectl apply -f yc_configmap.yaml
```

- Restart the deployment:

```bash
kubectl rollout restart deployment django-deployment
```

- _Note_: You can also delete the deployment and apply it again (instead of restarting):

```bash
kubectl delete -f yc_deploy.yaml
kubectl apply -f yc_deploy.yaml
```

## Migrations execution

- If the `k8s_cloud` folder is not the current folder, go to it:

```bash
cd k8s_cloud
```

- Create the `django-migrate` job:

```bash
kubectl apply -f yc_migrate.yaml
```

- Verify that the `django-migrate` job has been created:

```bash
kubectl get job django-migrate
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

_Note_: The job and the pod will be deleted in 120 seconds according to the `spec.ttlSecondsAfterFinished` parameter in the `yc_migrate.yaml` manifest file.

See also: [How to deploy the latest version](#how-to-deploy-the-latest-version).

## How to deploy the latest version

_Note_: remember to replace `fchef` with your login at [Docker Hub](https://hub.docker.com/) in the commands below and in the following files: `yc_deploy.yaml`, `yc_clearsessions.yaml`, `yc_migrate.yaml`.

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

- Verify that images are built. You should see two `fchef/k8s_django` images in the list: the first - with a tag `latest`, the second - with the commit hash as a tag. Both of these images will have the same `IMAGE ID`.

```bash
docker image ls
```

- Push the images to [Docker Hub](https://hub.docker.com/):

```bash
docker push --all-tags fchef/k8s_django
```

- If the `k8s_cloud` folder is not the current folder, go to it:

```bash
cd k8s_cloud
```

- [Execute migrations](#migrations-execution);

- Restart the deployment:

```bash
kubectl rollout restart deployment django-deployment
```

- _Note_: You can also delete the deployment and apply it again (instead of restarting):

```bash
kubectl delete -f yc_deploy.yaml
kubectl apply -f yc_deploy.yaml
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

## How to clear the session store

Create the `django-clearsessions` cronjob, which will run monthly:

```bash
kubectl create -f yc_clearsessions.yaml
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
