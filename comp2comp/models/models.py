import enum
import os
from pathlib import Path
from typing import Dict, Sequence

import wget
from keras.models import load_model


class Models(enum.Enum):
    ABCT_V_0_0_1 = (
        1,
        "abCT_v0.0.1",
        {"muscle": 0, "imat": 1, "vat": 2, "sat": 3},
        False,
        ("soft", "bone", "custom"),
    )

    STANFORD_V_0_0_1 = (
        2,
        "stanford_v0.0.1",
        # ("background", "muscle", "bone", "vat", "sat", "imat"),
        # Category name mapped to channel index
        {"muscle": 1, "vat": 3, "sat": 4, "imat": 5},
        True,
        ("soft", "bone", "custom"),
    )
    TS_SPINE_FULL = (
        3,
        "ts_spine_full",
        # Category name mapped to channel index
        {
            "L5": 18,
            "L4": 19,
            "L3": 20,
            "L2": 21,
            "L1": 22,
            "T12": 23,
            "T11": 24,
            "T10": 25,
            "T9": 26,
            "T8": 27,
            "T7": 28,
            "T6": 29,
            "T5": 30,
            "T4": 31,
            "T3": 32,
            "T2": 33,
            "T1": 34,
            "C7": 35,
            "C6": 36,
            "C5": 37,
            "C4": 38,
            "C3": 39,
            "C2": 40,
            "C1": 41,
        },
        False,
        (),
    )
    TS_SPINE = (
        4,
        "ts_spine",
        # Category name mapped to channel index
        {"L5": 18, "L4": 19, "L3": 20, "L2": 21, "L1": 22, "T12": 23},
        False,
        (),
    )
    STANFORD_SPINE_V_0_0_1 = (
        5,
        "stanford_spine_v0.0.1",
        # Category name mapped to channel index
        {"L5": 24, "L4": 23, "L3": 22, "L2": 21, "L1": 20, "T12": 19},
        False,
        (),
    )

    def __new__(
        cls,
        value: int,
        model_name: str,
        categories: Dict[str, int],
        use_softmax: bool,
        windows: Sequence[str],
    ):
        obj = object.__new__(cls)
        obj._value_ = value

        obj.model_name = model_name
        obj.categories = categories
        obj.use_softmax = use_softmax
        obj.windows = windows
        return obj

    def load_model(self, model_dir):
        """Load the model from the models directory.

        Args:
            logger (logging.Logger): Logger.

        Returns:
            keras.models.Model: Model.
        """
        try:
            filename = Models.find_model_weights(self.model_name, model_dir)
        except Exception:
            print("Downloading muscle/fat model from hugging face")
            Path(model_dir).mkdir(parents=True, exist_ok=True)
            wget.download(
                f"https://huggingface.co/stanfordmimi/stanford_abct_v0.0.1/resolve/main/{self.model_name}.h5",
                out=os.path.join(model_dir, f"{self.model_name}.h5"),
            )
            filename = Models.find_model_weights(self.model_name, model_dir)
            print("")

        print("Loading muscle/fat model from {}".format(filename))
        return load_model(filename, compile=False)

    @staticmethod
    def model_from_name(model_name):
        """Get the model enum from the model name.

        Args:
            model_name (str): Model name.

        Returns:
            Models: Model enum.
        """
        for model in Models:
            if model.model_name == model_name:
                return model
        return None

    @staticmethod
    def find_model_weights(file_name, model_dir):
        for root, _, files in os.walk(model_dir):
            for file in files:
                if file.startswith(file_name):
                    filename = os.path.join(root, file)
        return filename
