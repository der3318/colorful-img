
## 🎨 Render Colorful Image

![python](https://img.shields.io/badge/python-3+-blue.svg)
![matplotlib](https://img.shields.io/badge/matplotlib-3.6.1-green.svg)
![pillow](https://img.shields.io/badge/PIL-9.2.0-brightgreen.svg)
![cv2](https://img.shields.io/badge/opencv%20python-4.6.0.66-yellow.svg)

A python script to render image into different color styles.

<img src="/Images/Demo.png?raw=true">


### 📝 How to Use

Setup the python environment via `python -m pip install -r requirements.txt` and simply invoke [generate.py](https://github.com/der3318/colorful-img/blob/main/generate.py) with the image file name or path. It will generate 13 colorful images under the same directory, with extension `.stype[01-13].[jpg/png]`.

<img src="/Images/Usage.png?raw=true">


### 💡 How This Works

First, every pixel in the input image is converted into HSV descriptors from RGB values.

| <img src="/Images/ColorFormat.jpeg?raw=true"> |
| :- |
| (sample illustration from https://blog.csdn.net/Mark_md/article/details/115132435) |

Then, add a "unified shift" to to the hue (H) channel of each cell. By doing so, the relative values in the image are still kept, but the overall color theme is transformed. Repeat the same process using differnet "shifts" (in the sample, it is 1/13, 2/13, ..., 12/13), to render diffenet kinds of color styles.

