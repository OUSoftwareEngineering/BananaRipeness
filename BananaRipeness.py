from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def banana(picturePath, app):
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
    picture = picturePath
    file_name = os.path.join(
        os.path.dirname(__file__), picture)

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

    #Placeholder for percent of color seen in a photo
    colorMax = 0

    #Placeholder for the color with the highest percent in a photo
    mostColor = "N/A"

    #Loop through the colors found in a photo
    for color in props.dominant_colors.colors:

        #Get the percentage of the color that is in the photo
        x = color.pixel_fraction

        #Check if the 'main color' is white, ignore it if so
        if color.color.red > 230 and color.color.green > 230 and color.color.blue > 230:
            pass
        elif x > colorMax:
            colorMax = x
            mostColor = color.color

    #Get RGB values
    R = mostColor.red
    G = mostColor.green
    B = mostColor.blue

    #Calculate the HSV value from RGB values
    hsv = colorsys.rgb_to_hsv(R, G, B)

    #Calculate hue
    hue = hsv[0] * 360

    #Calculate value
    value = hsv[2]

    if hue > 0 and hue < 65 and value > 65:
        gui(picture, "The banana(s) is(are) ripe.", app)
    elif hue > 65 and hue < 110 and value > 65:
        gui(picture, "The banana(s) is(are) unripe.", app)
    else:
        gui(picture, "The banana(s) is(are) too ripe.", app)

def gui(pic, ripeness, app):
    image = Image.open(pic)
    app.picture = ImageTk.PhotoImage(image)
    if not hasattr(app, 'pic'):
        app.pic = Label(app, image=app.picture)
    else:
        app.pic['image'] = app.picture
    if not hasattr(app, 'text'):
        app.text = Label(app, text=ripeness)
    else:
        app.text['text'] = ripeness
    app.pic.grid()
    app.text.grid()


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = Button(self, text='Open Image',
            command=self.openFile)
        self.quitButton.grid()

    def openFile(self):
        root = self
        root.filename = filedialog.askopenfilename(initialdir="C:/Users/ecyrb/PycharmProjects/BananaRipeness/Resources", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        banana(root.filename, self)

if __name__ == '__main__':
    app = Application()
    app.master.title('Bananalyzer')
    app.mainloop()
