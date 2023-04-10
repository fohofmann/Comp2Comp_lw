import os
import subprocess
from pathlib import Path
from typing import Dict, Union

import nibabel as nib

from comp2comp.inference_class_base import InferenceClass


class DicomFinder(InferenceClass):
    """Find dicom files in a directory."""

    def __init__(self, input_path: Union[str, Path]) -> Dict[str, Path]:
        super().__init__()
        self.input_path = Path(input_path)

    def __call__(self, inference_pipeline) -> Dict[str, Path]:
        """Find dicom files in a directory.

        Args:
            inference_pipeline (InferencePipeline): Inference pipeline.

        Returns:
            Dict[str, Path]: Dictionary containing dicom files.
        """
        dicom_files = []
        for file in self.input_path.glob("**/*.dcm"):
            dicom_files.append(file)
        inference_pipeline.dicom_file_paths = dicom_files
        return {}


class DicomToNifti(InferenceClass):
    """Convert dicom files to nifti files, adapted from total segmentator"""

    def __init__(self, input_path):
        super().__init__()
        self.input_dir = input_path
        #self.input_dir = Path(input_path)

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
        inference_pipeline.medical_volume = nib.load(str(self.output_dir) + "/converted_dcm.nii.gz")
        inference_pipeline.path_nifti = str(self.output_dir) + "/converted_dcm.nii.gz"

        # remove json file
        os.remove(str(self.output_dir) + "/converted_dcm.json")

        return {}
