import os
import subprocess
import pydicom

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
        # save paths, define output directory
        inference_pipeline.dicom_series_path = str(self.input_dir)
        self.output_dir = inference_pipeline.output_dir

        # save series name
        inference_pipeline.dicom_series_name = str(self.input_dir).split("/")[-1]
        
        # select first, not hidden file in input directory
        for file in os.listdir(self.input_dir):
            if not file.startswith(".") and file.endswith(".dcm"):
                break
        
        # read dicoms, save date
        dcmData = pydicom.filereader.dcmread(str(self.input_dir) + "/" + file)
        inference_pipeline.dicom_series_date = dcmData.StudyDate

        # print series name and date
        print("Series name: ", inference_pipeline.dicom_series_name)
        print("Series date: ", inference_pipeline.dicom_series_date)

        # call dcm2niix directly, subprocess, verbose alwyas on
        subprocess.call(
            f"dcm2niix -o {self.output_dir} -z y -f 'converted_dcm' {self.input_dir}", shell=True
        )

        # save "mv" to inference pipeline
        inference_pipeline.path_nifti = str(self.output_dir) + "/converted_dcm.nii.gz"

        # remove json file
        os.remove(str(self.output_dir) + "/converted_dcm.json")

        return {}
