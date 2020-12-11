import io


from PIL import Image
import torch as pt
import torchvision.transforms as transforms


def get_model():
    model = pt.load("MaskTypeClassifier_90_87.pth", map_location=pt.device("cpu"))
    model.eval()
    return model


def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(256),          
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


# ImageNet classes are often of the form `can_opener` or `Egyptian_cat`
# will use this method to properly format it so that we get
# `Can Opener` or `Egyptian Cat`
def format_class_name(class_name):
    class_name = class_name.replace('_', ' ')
    class_name = class_name.title()
    return class_name
