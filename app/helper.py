from app import blob_service, blob_container, blob_url
import uuid


def add_image(uploaded_image):
    filename = uploaded_image.filename
    ext = filename.split('.')[-1]

    storage_filename = str(uuid.uuid1()) + '.' + ext 

    blob_client = blob_service.get_blob_client(container=blob_container, blob=storage_filename)
    blob_client.upload_blob(uploaded_image)

    return blob_url + storage_filename