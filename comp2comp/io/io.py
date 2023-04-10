from pathlib import Path
from typing import Dict, Union

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
