from google.cloud import vision
import io

desired_labels = [
    "Plastic",
    "Room",
    "Paper",
    "Cardboard"
]


class Analyzer:
    def __init__(self, path):
        self.path = path
        self.materials_label = None
        self.logo_label = None

    def get_materials(self):
        self.detect_labels()
        res = self.filer_response()
        return self.materials_label

    def filer_response(self):
        labels = self.get_sublist(self.materials_label, desired_labels)
        res = []
        for label in labels:
            res.append("contains " + label)
        return res

    def detect_labels(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations
        # print('Labels:')

        self.materials_label = []
        for label in labels:
            self.materials_label.append(label.description)
            # print(label.description)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

    def detect_logo(self, path):
        pass

    @staticmethod
    def get_sublist(l1, l2):
        return list(filter(lambda x: x in l2, l1))
