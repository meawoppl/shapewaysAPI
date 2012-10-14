import os,  base64, getpass
from suds.client import Client


defaultModelOptions = {"title":"Default Title", "desc":"Default Description",
                       "view_state":2, "tags":"model,auto-upload", 
                       "has_color":0, "scale":1, "markup":0}

class Shapeways(object):
    def __init__(self, username, password, appID = "ShapeWays Python API"):
        self.appID = appID
        # Retrieve the WSDL schema
        self.client = Client("http://api.shapeways.com/v1/wsdl.php")
        # Login and store the sessionID
        self.sessionid = self.client.service.login(username, password, self.appID)
        
    def uploadModel(self, filepath, **options):
        '''This function uploads a model file.  The first argument, the path to the file, is required.
           Other optional keyword arguments are:
           'title': The title the model will be given in the Shapeways website
           'desc': A description of the model
           'view_state': 0, 1, or 2 for view-only, for sale, or hidden respectively
           'tags': a comma sperated string of tags 
           'scale': floating point value where upload-scale * scale = meters
           'file_uri: ???
           'markup': a floating point markup in $'s'''

        # Extract the filename from the path
        filename = os.path.split(filepath)[-1]
        
        # Extract the extension from the path
        modeltype = os.path.splitext(filename)[-1][1:].upper()

        # Read in the file and base64 encode it
        encodedModel = base64.b64encode( open(filepath).read() )

        # Make a current "SWModel" object
        current_model = defaultModelOptions.copy()
        current_model.update(options)
        current_model.update({"file":encodedModel,"filename":filename, "file_uri":filename, "modeltype":modeltype})


        print "Uploading model", filepath
        print self.client.service.submitModel(session_id=self.sessionid, application_id = self.appID, model=current_model)
        print "Upload complete."

    def getPrinters(self):
        return self.client.service.getPrinters(session_id=self.sessionid, application_id = self.appID)

if __name__ == "__main__":
    un, pw = raw_input("Shapeways Username:"), getpass.getpass("Shapeways Password:")
    sw = Shapeways(un, pw)

    sw.uploadModel("sphere.stl")
    print sw.getPrinters()
