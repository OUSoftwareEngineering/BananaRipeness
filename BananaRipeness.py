def banana():
    # [START vision_quickstart]
    import io
    import os
    import colorsys

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
    #response = client.label_detection(image=image)
    #labels = response.label_annotations

    #print('Labels:')
    #for label in labels:
    #    print(label.description)
    # [END vision_quickstart]

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    #print('Properties:')

    colorMax = 0
    mostColor = "N/A"

    for color in props.dominant_colors.colors:
        x = color.pixel_fraction

        if color.color.red > 230 and color.color.green > 230 and color.color.blue > 230:
            pass
        elif x > colorMax:
            colorMax = x
            mostColor = color.color

    R = mostColor.red
    G = mostColor.green
    B = mostColor.blue

    hsv = colorsys.rgb_to_hsv(R, G, B)

    hue = hsv[0] * 360
    value = hsv[2]

    if hue > 0 and hue < 65 and value > 65:
        print("The banana(s) is(are) ripe.")
    elif hue > 65 and hue < 110 and value > 65:
        print("The banana(s) is(are) unripe.")
    else:
        print("The banana(s) is(are) too ripe.")

if __name__ == '__main__':
    banana()