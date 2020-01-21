import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor
import json
import base64

def show_faces(photo):

    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
        image = Image.open(photo)
        imgWidth, imgHeight = image.size
        draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected face         
    for faceDetail in response['FaceDetails']:
        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']

        points = (
            (left,top),
            (left + width, top),
            (left + width, top + height),
            (left , top + height),
            (left, top)
        )
        draw.line(points, fill='#00d400', width=2)

    result_path = '/tmp/test2_result.jpg'

    image.save(result_path)
    return open(result_path, 'rb')


def lambda_handler(event, context):
    # TODO implement
    photo='test2.jpg'

    result_image=show_faces(photo)

    return {
        'statusCode': 200,
        "isBase64Encoded": True,
        'body': base64.b64encode(result_image.read()).decode("utf-8"),
        'headers': {
            'Content-Type': 'image/jpg'
        }
    }