import os
from pathlib import Path
from time import time
from typing import Union

from totalsegmentator.libs import download_pretrained_weights
from totalsegmentator.libs import nostdout
from totalsegmentator.config import setup_nnunet

from comp2comp.inference_class_base import InferenceClass


class OrganSegmentation(InferenceClass):
    """Organ segmentation."""

    def __init__(self, input_path):
        super().__init__()
        self.input_path = input_path

    def __call__(self, inference_pipeline):
        self.output_dir = inference_pipeline.output_dir
        self.output_dir_segmentations = os.path.join(self.output_dir, "segmentations/")
        if not os.path.exists(self.output_dir_segmentations):
            os.makedirs(self.output_dir_segmentations)

        seg = self.organ_seg(
            inference_pipeline.path_nifti,
            self.output_dir_segmentations + "organs.nii.gz"
        )

        inference_pipeline.segmentation = seg

        return {}

    def organ_seg(self, input_path: Union[str, Path], output_path: Union[str, Path]):
        """Run organ segmentation.

        Args:
            input_path (Union[str, Path]): Input path.
            output_path (Union[str, Path]): Output path.
        """

        print("Segmenting organs...")
        st = time()

        # Setup nnunet
        model = "3d_fullres"
        folds = [0]
        trainer = "nnUNetTrainerV2_ep4000_nomirror"
        crop_path = None
        task_id = [251]

        setup_nnunet()
        download_pretrained_weights(task_id[0])

        from totalsegmentator.nnunet import nnUNet_predict_image

        with nostdout():

            seg = nnUNet_predict_image(
                input_path,
                output_path,
                task_id,
                model=model,
                folds=folds,
                trainer=trainer,
                tta=False,
                multilabel_image=True,
                resample=1.5,
                crop=None,
                crop_path=crop_path,
                task_name="total",
                nora_tag=None,
                preview=False,
                nr_threads_resampling=1,
                nr_threads_saving=6,
                quiet=False,
                verbose=False,
                test=0,
            )
        end = time()

        # Log total time for spine segmentation
        print(f"Total time for organ segmentation: {end-st:.2f}s.")

        return seg
