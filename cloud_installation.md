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

If the `django-deployment` deployment was not created yet, create it:

```bash
kubectl create -f yc_deploy.yaml
```
