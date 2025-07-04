# manager

Renovate Repos Manager

## Local dev environment

##### Prerequisites

- kind installed
- kubectl installed
- make installed

##### Instructions

1. Create Environment

    ```bash
    make up
    ```

2. Access the application at `http://127.0.0.1:5000`.

3. Delete cluster

    ```bash
    make down
    ```

## OpenShift Deployment

This section outlines deploying the Afula application to an OpenShift cluster

### Prerequisites

- OpenShift CLI (`oc`) installed and configured to connect to your cluster.
- The image `ghcr.io/platform-engineering-org/afula-manager:latest` should be accessible by your OpenShift cluster.

### Preparing the Deployment File

- The provided `deploy/template.yaml` serves as a starting point. It is pre-configured to use `image: ghcr.io/platform-engineering-org/afula-manager:latest`.
- Before applying, consider the following customizations for your environment:
  - **Image (If different):** If you use an image other than `ghcr.io/platform-engineering-org/afula-manager:latest`, update `spec.template.spec.containers[0].image` in the Deployment resource.
  - **Route Host (Optional):** If you want a specific hostname for your application, ensure the `spec.host` field in the Route resource is set. If omitted, OpenShift will generate a hostname.
  - Review other configurations like resource requests/limits, replicas, labels, etc., and adjust as needed.

### Deployment Steps

1. **Login to OpenShift (if not already):**

    ```bash
    oc login ...
    ```

2. **Target Namespace:**
    The `deploy/template.yaml` file does not specify a namespace. You must target the desired OpenShift project (namespace) when applying the configuration.
    You can either switch to your target project first:

    ```bash
    oc project <your-target-namespace>
    # or, if creating for the first time:
    oc new-project <your-target-namespace>
    ```

    Create the params.env file

    ```
    cp params.env.template params.env
    ```

    Then, edit params.env and fill in any required values. This file may contain sensitive information such as API tokens, credentials, or environment-specific configuration, so it should not be tracked in Git.

    And then apply:

    ```bash
    oc process -f deploy/template.yaml --param-file=params.env | oc apply -f -
    ```

    Alternatively, specify the namespace directly with the `apply` command:

    ```bash
    oc process -f deploy/template.yaml --param-file=params.env | oc apply -n <your-target-namespace> -f -
    ```

3. **Apply the Deployment Configuration:**
    (Covered in the step above)

### Accessing the Service (OpenShift)

- To find the hostname (replace `<your-target-namespace>` with the actual namespace used):

    ```bash
    oc get routes -n <your-target-namespace>
    ```

- Access the application via `http://<ROUTE_HOSTNAME>`.

### Cleaning Up (OpenShift)

To remove the resources deployed to OpenShift (replace `<your-target-namespace>` with the actual namespace used):

```bash
oc process -f deploy/template.yaml --param-file=params.env | oc delete -n <your-target-namespace> -f -
```
