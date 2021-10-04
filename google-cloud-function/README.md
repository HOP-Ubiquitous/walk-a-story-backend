# Google Cloud Function

- **notify**: handler function name

- **bememories**: bucket name

- **google.storage.object.finalize**: event to trigger, new object in google cloud storage

**Command to deploy:**
```
$ gcloud functions deploy notify --runtime python37 --trigger-resource {{bucket_name}} --trigger-event google.storage.object.finalize
```

**Values**
```
def notify(data, context):

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    print('Bucket: {}, New File: {}'.format(data['bucket'], data['name']))
    print('Metageneration: {}'.format(data['metageneration']))
    print('Created: {}'.format(data['timeCreated']))
    print('Updated: {}'.format(data['updated']))
```