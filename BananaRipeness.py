def banana():
    # [START vision_quickstart]
    import io
    import os

    # Imports the Google Cloud client library
    # [START vision_python_migration_import]
    from google.cloud import vision
    from google.cloud.vision import types
    # [END vision_python_migration_import]

    # Instantiates a client
    # [START vision_python_migration_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_python_migration_client]
    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'Resources/bananaPic.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)
    # [END vision_quickstart]

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    colorMax = 0
    mostColor = "N/A"

    for color in props.dominant_colors.colors:
        x = color.pixel_fraction

        if (x > colorMax):
            colorMax = x
            mostColor = color.color

    R = mostColor.red / 255
    G = mostColor.green / 255
    B = mostColor.blue / 255

    hue = 0;

    theMax = max(R, G, B)
    theMin = min(R,G,B)

    maxMin = theMax - theMin

    if maxMin > 0:
        if theMax == R:
            hue = (G-B)/(theMax-theMin)
        if theMax == G:
            hue = 2.0 + (B-R)/(theMax-theMin)
        if theMax == B:
            hue = 4.0 + (R-G)/(theMax-theMin)

        hue = hue * 60

        if hue < 0:
            hue = hue + 360

    print(hue)

    print("TESTING THIS: " + str(mostColor.red))
    print("TESTING THIS: " + str(mostColor.green))
    print("TESTING THIS: " + str(mostColor.blue))

if __name__ == '__main__':
    banana()