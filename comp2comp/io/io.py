import os
import subprocess

from comp2comp.inference_class_base import InferenceClass

class DicomToNifti(InferenceClass):
    """Convert dicom files to nifti files, adapted from total segmentator"""

    def __init__(self, input_path):
        super().__init__()
        self.input_dir = input_path

    def __call__(self, inference_pipeline):
        """Transform dicom files directory to nifti file in outputs.

        Args:
            inference_pipeline (InferencePipeline): Inference pipeline.

        Returns:
            medical volume to inference pipeline
        """
        # define output directory
        inference_pipeline.dicom_series_path = str(self.input_dir)
        self.output_dir = inference_pipeline.output_dir
        
        # call dcm2niix directly, subprocess, verbose alwyas on
        subprocess.call(
            f"dcm2niix -o {self.output_dir} -z y -f 'converted_dcm' {self.input_dir}", shell=True
        )

        # save "mv" to inference pipeline
        inference_pipeline.path_nifti = str(self.output_dir) + "/converted_dcm.nii.gz"

        # remove json file
        os.remove(str(self.output_dir) + "/converted_dcm.json")

        return {}
