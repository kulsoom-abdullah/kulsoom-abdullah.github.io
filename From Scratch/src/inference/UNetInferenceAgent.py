"""
Contains class that runs inferencing
"""
import torch
import numpy as np

from networks.RecursiveUNet import UNet

from utils.utils import med_reshape

class UNetInferenceAgent:
    """
    Stores model and parameters and some methods to handle inferencing
    """
    def __init__(self, parameter_file_path='', model=None, device="cpu", patch_size=64):

        self.model = model
        self.patch_size = patch_size
        self.device = device

        if model is None:
            self.model = UNet(num_classes=3)

        if parameter_file_path:
            self.model.load_state_dict(torch.load(parameter_file_path, map_location=self.device))

        self.model.to(device)

    def single_volume_inference_unpadded(self, volume):
        """
        Runs inference on a single volume of arbitrary patch size,
        padding it to the conformant size first

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        
        raise NotImplementedError

    def single_volume_inference(self, volume):
        """
        Runs inference on a single volume of conformant patch size

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        self.model.eval()

        # Assuming volume is a numpy array of shape [X,Y,Z] and we need to slice X axis
        slices = []

        # TASK: Write code that will create mask for each slice across the X (0th) dimension. After 
        # that, put all slices into a 3D Numpy array. You can verify if your method is 
        # correct by running it on one of the volumes in your training set and comparing 
        # with the label in 3D Slicer.
        # <YOUR CODE HERE>
        slices = np.zeros(volume.shape)
        for slice_idx in range(volume.shape[0]):
            # normalize the image
            slice0 = volume[slice_idx,:,:]
            slice0 = slice0.astype(np.single)
            slice0_norm = slice0 / 255.0

            # convert to pytorch tensor

            slice0_t = torch.from_numpy(slice0_norm).unsqueeze(0).unsqueeze(0)

            # predict the label
            pred = self.model(slice0_t.to(self.device))

            # normal image slice

            pred =  np.squeeze(pred.cpu().detach())

            slices[slice_idx,:,:] = torch.argmax(pred, dim=0)  

        return slices
#         for X in volume:

#             X = X.astype(np.single)
#  5
#   X = X/255.
#  6
#   X_t = torch.from_numpy(X).unsqueeze(0).unsqueeze(0)
#  7
#   prediction = self.model(X_t.to(self.device))
#  8
#   prediction = np.squeeze(prediction.cpu().detach())
#  9
#   slices.append(torch.argmax(prediction, dim = 0))

#   return  np.array(slices)
#         slc_tensor = torch.from_numpy(volume).type(torch.cuda.FloatTensor).unsqueeze(1).to(self.device)
#         prediction = self.model(slc_tensor)
#         masks = torch.argmax(prediction, dim = 1).cpu().detach().numpy().astype(int)
        
#         return # 
 