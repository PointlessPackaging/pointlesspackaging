from google.cloud import vision
import io

pics = ['https://i.imgur.com/2EUmDJO.jpg', 'https://i.imgur.com/FPMomNl.png']

client = vision.ImageAnnotatorClient()
image = vision.types.Image()

for pic in pics:
    image.source.image_uri = pic
    response = client.face_detection(image=image)

    print('=' * 79)
    print('File: {pic}')
    for face in response.face_annotations:
        likelihood = vision.enums.Likelihood(face.surprise_likelihood)
        vertices = [f'({v.x},{v.y})' for v in face.bounding_poly.vertices]
        print(f'Face surprised: {likelihood.name}')
        print(f'Face bounds: {",".join(vertices)}')
