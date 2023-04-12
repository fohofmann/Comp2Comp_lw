import inspect
from typing import Dict, List
from comp2comp.inference_class_base import InferenceClass

class InferencePipeline(InferenceClass):
    """Inference pipeline."""

    def __init__(self, inference_classes: List = None, config: Dict = None):
        self.config = config
        # assign values from config to attributes
        if self.config is not None:
            for key, value in self.config.items():
                setattr(self, key, value)

        self.inference_classes = inference_classes

    def __call__(self, inference_pipeline=None, **kwargs):
        # print out the class names for each inference class
        #print("Planned inference pipeline:")
        #for i, inference_class in enumerate(self.inference_classes):
        #    print(f"({i + 1}) {inference_class.__repr__()}")
        #print("")

        print("Starting inference pipeline.\n")

        if inference_pipeline:
            for key, value in kwargs.items():
                setattr(inference_pipeline, key, value)
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

        output = {}
        for inference_class in self.inference_classes:

            function_keys = set(inspect.signature(inference_class).parameters.keys())
            function_keys.remove("inference_pipeline")

            if "kwargs" in function_keys:
                function_keys.remove("kwargs")

            assert function_keys == set(
                output.keys()
            ), "Input to inference class, {}, does not have the correct parameters".format(
                inference_class.__repr__()
            )

            print("\nRunning {}".format(inference_class.__repr__()))

            if inference_pipeline:
                output = inference_class(inference_pipeline=inference_pipeline, **output)
            else:
                output = inference_class(inference_pipeline=self, **output)

            # print("Finished {}".format(inference_class.__repr__()))

        print("Inference pipeline finished.\n")

        return output


if __name__ == "__main__":
    """Example usage of InferencePipeline."""
    # getting rid of any dosma-dependecies

    print("You should use the inference pipeline as a module instead of running it as a script.")
