# Automated Metamorphic Testing on StackGAN-v2

This repository is used to automate the metamorphic test cases written in paper. Metamorphic Testing is conducted to evaluting the robustness and stability of StackGAN-v2 and Metamorhic relations are generated to identify the correctness of the testing result. Details of this Automated testing is documented below:

### Data

- Prepare the datasets by downloading [Birds](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html), then extract and place into `Data/ birds`.
- Download the preprocessed char-CNN-RNN text embeddings for [Birds](https://drive.google.com/open?id=0B3y_msrWZaXLT1BZdVdycDY5TEE) [[1]](#1) and place into `Data/ birds`.

### StackGAN-v2 

- Follow the instructions and steps from [StackGAN-v2](https://github.com/hanzhanggit/StackGAN-v2) to training the datasets and evaluate the result.

### MRs
- **<a id="MR01">MR<sub>01</sub></a>**: Introduction of one bird to 100% of the images within the detected box.
- **<a id="MR02">MR<sub>02</sub></a>**: Introduction of one bird to 100% of the images outside the detected box.
- **<a id="MR03">MR<sub>03</sub></a>**: Introduction of one bird to 100% of the images in between the detected box and its 100px wide padding.
- **<a id="MR04">MR<sub>04</sub></a>**: Introduction of one bird to 100% of the images in between the detected box’s 100px wide padding and its 200px wide padding.
- **<a id="MR05">MR<sub>05</sub></a>**: Introduction of one bird to 100% of the images within the bounding box.
- **<a id="MR06">MR<sub>06</sub></a>**: Introduction of one bird to 100% of the images outside the bounding box.

### Implementation
#### Preparing testing datasets 
##### Modifing images datasets by adding an obtrusive object that similar with the focal object (birds) [[MR<sub>01</sub>]](#MR01)
- Make sure datasets had set up.
- Create a new folder and place the additional object.
- Direct to `Data/ birds` and run `python addExtraBird.py directory/place/source/images -R "addBirdRegionRecord(overlapping).txt" -d "detected_log.json" -o directory/to/place/modified/datasets -e directory/place/extra/object -s 100 100`
- replace the modified images with original images datasets

<!--  **Optional:** -->
<!-- - A txt file named 'SavedRecord.txt' will be generated after modified the training images. -->
<!-- - run `python fixModifiedBird.py -r -o directory/to/place/modified/datasets -d directory/place/extra/object  directory/place/source/images -R SavedRecord.txt -C class_number -I [image_number]` (eg. python fixModifiedBirdByRegions.py -r -o "output" -d "extra_birds" -R "SavedRecord.txt" "CUB_200_2011/images" -C 001 -I 0002 0004) to change the position of the extra object placed in the source image for [[MR<sub>06</sub>]](#MR06) where the position of the added object will not obstruct the view of the focal object (bird). -->

##### Modifing images datasets by adding an unobtrusive object that similar with the focal object (birds) [[MR<sub>02</sub>]](#MR02)
- Make sure datasets had set up.
- Create a new folder and place the additional object.
- Direct to `Data/ birds` and run `python addExtraBirdByRegions.py directory/place/source/images -R "addBirdRegionRecord(no overlapping).txt" -d "detected_log.json" -o directory/to/place/modified/datasets -e directory/place/extra/object -s 100 100` 
- replace the modified images with original images datasets

##### Modifing images datasets by adding an object that sized 100px and similar with the focal object (birds), the added objects are close to the focal object [[MR<sub>03</sub>]](#MR03)
- Make sure datasets had set up.
- Create a new folder and place the additional object.
- Direct to `Data/ birds` and run `python addExtraBirdByRegions.py directory/place/source/images -R "addBirdRecord(padding_1).txt" -d "detected_log.json" -o directory/to/place/modified/datasets -e directory/place/extra/object -s 100 100`
- replace the modified images with original images datasets

##### Modifing images datasets by adding an object that sized 100px and similar with the focal object (birds), the added objects are 100px further to the focal object [[MR<sub>04</sub>]](#MR04)
- Make sure datasets had set up.
- Create a new folder and place the additional object.
- Direct to `Data/ birds` and run `python addExtraBirdByRegions.py directory/place/source/images -R "addBirdRecord(padding_2).txt" -d "detected_log.json" -o directory/to/place/modified/datasets -e directory/place/extra/object -s 100 100`
- replace the modified images with original images datasets

##### Modifing images datasets by adding an object that similar with the focal object (birds) inside the bounding box [[MR<sub>05</sub>]](#MR05)
- Make sure datasets had set up.
- Create a new folder and place the additional object.
- Direct to `Data/ birds` and run `python addExtraBirdByRegions.py directory/place/source/images -R "addBirdRecord(inside BBOX).txt" -b "CUB_200_2011/bounding_boxes.txt" -i "CUB_200_2011/images.txt" -o directory/to/place/modified/datasets -e directory/place/extra/object -s 100 100`
- replace the modified images with original images datasets

##### Modifing images datasets by adding an object that similar with the focal object (birds) outside the bounding box [[MR<sub>06</sub>]](#MR06)
- Make sure datasets had set up.
- Create a new folder and place the additional object.
- Direct to `Data/ birds` and run `python addExtraBirdByRegions.py directory/place/source/images -R "addBirdRecord(outside BBOX).txt" -b "CUB_200_2011/bounding_boxes.txt" -i "CUB_200_2011/images.txt" -o directory/to/place/modified/datasets -e directory/place/extra/object -s 100 100`
- replace the modified images with original images datasets

#### Training with modified datasets
- Direct to `Code/` and run `python main.py -python main.py --cfg cfg/birds_3stages.yml --gpu 0`

#### Evaluating Results
- Direct to `Code/` and run `python main.py --cfg cfg/eval_birds.yml --gpu 0`


### References
<a id="1">[1]</a> StackGAN: Text to Photo-realistic Image Synthesis with Stacked Generative Adversarial Networks [Paper](https://arxiv.org/pdf/1612.03242v1.pdf) [Code](https://github.com/hanzhanggit/StackGAN-v2)
