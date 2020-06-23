from config import bd_client


def img_to_str(image_path):
    with open(image_path, 'rb') as f:
        result = bd_client.basicGeneral(f.read())
        return result
