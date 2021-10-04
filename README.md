# Walk a Story Backend

Backend service for the **Walk a Story** application It manages users, videos, comments, ratings and walks. In addition, it uses Google Cloud Storage as a file store in order to simplify the storage of large files.

## Develop

- Install [requirements.txt](requirements.txt)
- Run [main.py](main.py) with:
    - Edit [config.py](config.py) if was necessary
    - Required environment variable with run:
        - GOOGLE_APPLICATION_CREDENTIALS={{PATH/API-cloud.json}}

## Config, Build and Run

### Environment variables

[Config file](config.py) with all default env variables.

Editable env variables in compose file:

  - **GOOGLE_APPLICATION_CREDENTIALS**: Google cloud json credential file absolute path.
    [Credential file](docker-compose/config-files/API-cloud.json).
  - REST_URL: Internal URL of service.
  - **REST_PORT**: Internal port of service
  - BUCKET_NAME: bucket/segment of Google Cloud Storage
    - **bememories** (testing)
        - https://console.cloud.google.com/storage/browser/bememories
    - **co-crew** (production, first it should be all removed to ignore conflicts)
        - https://console.cloud.google.com/storage/browser/co-crew
  - DEBUG_FRONTEND: If **True** then allow run simple frontend to check the service works.
  - **SECURE_API**: If **True** then login required with cookie between frontend and backend.
  - BASE_PATH: set a main directory into bucket selected.
    - Example: gs://{{**BUCKET_NAME**}}/{{**BASE_PATH**}}/{{**place_id**}}/

### Google Video Analytics notification

The bucket/segment co-crew is **already configured** with the event generator after changes. This is used to determine when the Video Analyzer has generated the automatic analysis for an uploaded video.

Documentation and code of Google Cloud function [here](google-cloud-function).

### Docker build  

 ```
$ docker build -t "registry.hopu.eu/bememories-record/backend:0.5.1" .
$ docker push registry.hopu.eu/bememories-record/backend:0.5.1
```

### Online Swarm deploy

[Swarm compose](docker-compose/swarm-compose.yml) file.

- Configs:
    - google-cloud-json (credential file, [here](docker-compose/config-files/API-cloud.json))

## Usage

[Postman collection](/docs/walk-a-story.postman_collection.json) with all calls to REST API.


## TODO

- None

## References

- https://cloud.google.com/storage/docs/authentication
- https://cloud.google.com/storage/docs/uploading-objects
- https://www.codementor.io/@sheena/understanding-sqlalchemy-cheat-sheet-du107lawl
- https://pypi.org/project/Flask-Cors/1.10.3/
- https://aukera.es/blog/tracking-video-html5-gtm/

## Google Cloud Services

#### Google Cloud Video Intelligence

Documentation [here](/docs/video-intelligence.md)

#### Google Cloud Storage

Documentation [here](/docs/storage.md)

#### Google Cloud Function

Notify new files in Google Cloud Storage.
Documentation [here](/google-cloud-function/README.md)

## Issues

- None
