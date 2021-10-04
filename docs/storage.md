# Google Cloud Storage

## Glosary

- **Bucket**: Identifier segment of a google cloud storage root directory in a project. 
- **Blob**: Object in the bucket.

## Functions:
- def create_bucket(bucket_name):
- def delete_bucket(bucket_name):
- def enable_default_kms_key(bucket_name, kms_key_name):
- def get_bucket_labels(bucket_name):
- def add_bucket_label(bucket_name):
- def remove_bucket_label(bucket_name):
- def list_blobs(bucket_name)
- def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    - This can be used to list all blobs in a "folder", e.g. "public/".
- def upload_blob(bucket_name, source_file_name, destination_blob_name):
- def download_blob(bucket_name, source_blob_name, destination_file_name):
- def delete_blob(bucket_name, blob_name):
- def make_blob_public(bucket_name, blob_name):
- def rename_blob(bucket_name, blob_name, new_name):
- def copy_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):

## References

https://cloud.google.com/python/getting-started/using-cloud-storage

https://github.com/GoogleCloudPlatform/getting-started-python

https://github.com/GoogleCloudPlatform/getting-started-python/tree/master/3-binary-data

https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/snippets.py

- ReadTheDocs

    https://google-cloud-python.readthedocs.io/en/0.8.0/storage-client.html
    
    https://googleapis.github.io/google-cloud-python/latest/storage/index.html