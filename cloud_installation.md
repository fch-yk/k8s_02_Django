# Cloud installation

The project was deployed in the [Yandex Cloud](https://cloud.yandex.com/en/) cluster.

The website can be accessed [here](https://edu-focused-keller.sirius-k8s.dvmn.org/) for a while.

It is assumed that the cloud cluster already exists. The project deployment in the cloud cluster depends on the cloud service provider and the cluster configuration.

## Key features of the project installation

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
  database_url: postgres://replace_user:replace_password@repace_host:replace_port/replace_db
```

- Apply the secret:

```bash
kubectl apply -f yc_secret.yaml
```

## How to organize the `media` storage

Go to the `kubernetes` folder:

```bash
cd kubernetes
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

- Edit the `yc_configmap.yaml` file;
- Apply the `yc_configmap.yaml` file changes:

```bash
kubectl apply -f yc_configmap.yaml
```

- Restart the deployment:

```bash
kubectl rollout restart deployment django-deployment
```

- _Note_: You can also delete the deployment and start it again (instead of restarting):

```bash
kubectl delete -f yc_deploy.yaml
kubectl apply -f yc_deploy.yaml
```
