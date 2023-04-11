[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[**Original Repository**](https://github.com/StanfordMIMI/Comp2Comp/)
| [**Original Paper**](https://arxiv.org/abs/2302.06568)
| [**Citation**](https://github.com/StanfordMIMI/Comp2Comp/#citation)

**This is a fork of the [Comp2Comp](https://github.com/StanfordMIMI/Comp2Comp/) repository. Please refer to the original repository for more information.**

## General information
This fork is a lightweight version of the original [Comp2Comp repository](https://github.com/StanfordMIMI/Comp2Comp/).
Some quick and dirty adaptions were made to reduce dependencies, complexity and required writing rights on the host system, making the implementation at HPC-systems simpler.
- predefined pipeline, reduced arguments
- reduction of dependencies (e.g. dosma)
- reduced output
- usage of the original TotalSegmentator instead of the forked Standford version
- download and integration of weights and models prior to execution
- paths moved to parent directory
- files and modules not needed removed

## Citations
If you use this code, you should cite the following papers:

[Comp2Comp](https://github.com/StanfordMIMI/Comp2Comp)
> Blankemeier L., Desai A., Chaves J. M. Z., Wentland A., Yao S., Reis E., Jensen M., Bahl B., Arora K., Patel, B. N. et al. Comp2Comp: Open-Source Body Composition Assessment on Computed Tomography, 2023. URL: https://arxiv.org/abs/2302.06568. arXiv: 2302.06568

[TotalSegmentator](https://github.com/wasserth/TotalSegmentator)
> Wasserthal J., Meyer M., Breit H., Cyriac J., Yang S., Segeroth M. TotalSegmentator: robust segmentation of 104 anatomical structures in CT images, 2022. URL: https://arxiv.org/abs/2208.05868. arXiv: 2208.05868

[nnU-Net](https://github.com/MIC-DKFZ/nnUNet)
> Isensee, F., Jaeger, P. F., Kohl, S. A., Petersen, J., & Maier-Hein, K. H. (2021). nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. Nature methods, 18(2), 203-211.


