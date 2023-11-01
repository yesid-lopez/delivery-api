# Delivery API Service

Repo url: https://github.com/yesid-lopez/delivery-api

## Architecture

The following is the e2e flow for the application:

![e2e](https://raw.githubusercontent.com/yesid-lopez/delivery-api/main/docs/e2e.png?token=GHSAT0AAAAAAB5U4C3JFIM4PSXNSTSCWG62ZKCSHYA)

Whenever a new raw order arrives, the application initiates a preprocessing step: It fetches the average preparation time based on the venue ID from Redis and calculates the order's hour of the day. Then, after the model has been loaded, the delivery duration time is predicted by the model.

Additionally, the average preparation time is loaded in a separate task. This allows us to separate responsibilities, and in case average preparation times are added, it just updates Redis without deploying the entire application. On the other hand, the model weights are loaded on a separate path; this allows us to update the model weights easily in case a new model has been released.

Main Tools and libraries:
- FastAPI
- Redis
- Docker
- Pydantic
- Poetry

## Future Improvements

- Move the insert of average preparation time as a pipeline in flyte/kubeflow
- Create a pipeline for the training script
- Save the model weights in S3 for a better artifact versioning
- Add k8s configuration files in order to deploy the app in production
- The logging has been added in the current application in order to add in the future Prometheus/Grafana to monitor the data drifting, AB test analysis and monitor the general performance of the model.
- Add integration and e2e tests for a better testing coverage.
- Currently, the application is designed to make inferences on one order at a time. If batch inference is intended, the current implementation must be changed to support that
- If the preprocessing step becomes more complex in the future, create an external service to take care of this.

## Examples of request

### Successful request

You can either use swagger (http://localhost:8000/docs) or any tool.

Examples with curl:
```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "venue_id": "8a61c05",
  "time_received": "2023-11-01T18:18:19.335Z",
  "is_retail": 0
}'
```

example of response:
```bash
200 status code

{
  "delivery_duration": 20.340660095214844
}
```

### Venue does not exist request

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "venue_id": "invalid_venue",
  "time_received": "2023-11-01T18:18:19.335Z",
  "is_retail": 0
}'
```
response
```bash
400 status code
{
  "detail": "Venue does not exist in cache"
}
```

## Running the app

```bash
make all
make run
```

Add the features in the cache service:
```bash
make seed-redis
```

## Running the app in develop mode

```bash
make all
make run-dev
```

Add the features in the cache service:
```bash
make seed-redis
```

you can open http://localhost:8000/docs and you will see the swagger application

## Executing unit tests

And execute the unit tests:
```bash
make unit-test
```

## Executing lint and type checking

And execute the unit tests:
```bash
make type-check
make lint
```