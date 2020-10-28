# Evaluating StackGAN-v2 with metamorphic testing

Metamorphic Testing is conducted to evaluting the robustness and stability of metamorphic. Metamorhic relations are generated to identify the correctness of the testing result. Details of this metamorhic testing is documented below:

### Data

- Prepare the datasets by downloading [Birds](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html), then extract and place into `Data/ birds`.
- Download the preprocessed char-CNN-RNN text embeddings for [Birds](https://drive.google.com/open?id=0B3y_msrWZaXLT1BZdVdycDY5TEE) [[1]](#1) and place into `Data/ birds`.

### StackGAN-v2 

- Follow the instructions and steps from [StackGAN-v2](https://github.com/hanzhanggit/StackGAN-v2) to training the datasets and evaluate the result.

### MRs
- **<a id="MR01">MR<sub>01</sub></a>**: Introduction of an unobtrusive object consistently in all training image dataset should not drastically affect the Inception Score
- **<a id="MR02">MR<sub>02</sub></a>**: Introduction of an unobtrusive object consistently in all training image dataset should result in a grey-tinted effect and impact the Inception Score 
- **<a id="MR03">MR<sub>03</sub></a>**: Introduction of an unobtrusive object in only a selected portion of the training image dataset should result in a diminished effect of the grey-tinted effect and a higher Inception Score
- **<a id="MR04">MR<sub>04</sub></a>**: The action of performing Gaussian Blurring on the training data images should result in a diminished Inception Score, but not result in any grey-tinted effect.
- **<a id="MR05">MR<sub>05</sub></a>**: Introduction of an unobtrusive object consistently in all training image dataset should result in a grey-tinted effect and impact the Inception Score in a similar manner, regardless of the colour of the object introduced.

### Implementation
#### Preparing testing datasets 
##### Modifing images datasets by adding a unobtrusive object [[MR<sub>01</sub>]](#MR01), [[MR<sub>03</sub>]](#MR03), [[MR<sub>05</sub>]](#MR05)
- Make sure datasets had set up.

- Create a new folder and place the additional object.

- Direct to `Data/ birds` and run `python addExtraBird.py -r -o directory/to/place/modified/datasets -d directory/place/extra/object  directory/place/source/images`

- replace the modified images with original images datasets

  **Optional:** 

- run `python fixModifiedBird.py -r -o directory/to/place/modified/datasets -d directory/place/extra/object  directory/place/source/images -C class_number -I [image_number]` (eg. python fixModifiedBird.py -r -o "output" -d "extra_birds" "CUB_200_2011/images" -C 001 -I 0002 0004) to change the position of the extra object placed in the source image

##### Modifing images datasets by adding multiple unobtrusive object [[MR<sub>02</sub>]](#MR02)
- Make sure datasets had set up.
- Create a new folder and place the additional object.
- Direct to `Data/ birds` and run `python addExtraTree.py -r -o directory/to/place/modified/datasets -d directory/place/extra/object  directory/place/source/images -n maximum_number_of_additional_object` 

##### Blurring images from datasets [[MR<sub>04</sub>]](#MR04)
- Make sure datasets had set up.
- Direct to `Data/ birds` and run `python blurImages.py  -r -o directory/to/place/modified/datasets directory/place/source/images`
- replace the modified images with original images datasets

#### Training with modified datasets
- Direct to `Code/` and run `python main.py -python main.py --cfg cfg/birds_3stages.yml --gpu 0`

#### Evaluating Results
- Direct to `Code/` and run `python main.py --cfg cfg/eval_birds.yml --gpu 0`


### references
<a id="1">[1]</a> StackGAN: Text to Photo-realistic Image Synthesis with Stacked Generative Adversarial Networks [Paper](https://arxiv.org/pdf/1612.03242v1.pdf) [Code](https://github.com/hanzhanggit/StackGAN-v2)
