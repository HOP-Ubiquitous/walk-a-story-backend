# TODO upload to google cloud function with public IP of co-crew-backend
CO_CREW_BACKEND_URL = 'https://walk-a-story-backend-service'


def notify(data, context):
    url = CO_CREW_BACKEND_URL+"/api/v1/analyzer/notify"

    if data['name'].endswith('.json'):
        payload = "{ \"notification\":\"" + data['name'] + "\"}"
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
        }

        import requests
        requests.request("POST", url, data=payload, headers=headers)
