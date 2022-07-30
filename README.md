# OpenCV：把卡Ｐ上圖

## 問題

將信用卡貼在圖中，要符合原圖中卡的位置和大小

## 資料
|img.jpg|mask.jpg|new_card.jpg|
|:-:|:-:|:-:|
|![](https://i.imgur.com/qAMqcvK.jpg =70%x)|![](https://i.imgur.com/0eCn9mk.jpg =70%x)|![](https://i.imgur.com/7WRjyHY.jpg)|

## 流程
> 1. 得到mask四個角的座標
> 2. 使用透視轉換來轉換new_card to mask
> 3. 挖出img中的卡片
> 4. 貼上經過透視轉換的new_card於img上

### 1. 得到mask四個角的座標

#### 邊緣偵測 - Canny

對mask做邊緣偵測

![](https://i.imgur.com/K94f2jH.png =35%x)

#### 輪廓偵測 - Contour
- 對邊緣偵測過的圖做輪廓偵測
- 使用``cv2.findContours``偵測
    - External：若有其他輪廓包在內部的話，只取外層的輪廓
    - CHAIN_APPROX_NONE：不做水平或垂直輪廓點的壓縮，保留所有的輪廓點
- 使用``cv2.minAreaRect``取出中心點,寬高,角度，``cv2.boxPoints``去轉換成四個角的座標
- 將座標以np.float32的形式存入``dst``

|四個點|繪製出輪廓和四點|
|:-:|:-:|
|![](https://i.imgur.com/DwcvN8f.png)|![](https://i.imgur.com/R9g8Ar6.png =50%x)|![](https://i.imgur.com/dAkvRan.png)


### 2. 透視轉換

- 座標
``src``：原圖
``dst``：要轉換成的圖片

- 要小心他只接受數值是float32

```python
dst = box
src = np.array([[0, 0], [new_card.shape[1] - 1, 0], [new_card.shape[1] - 1,
               new_card.shape[0] - 1], [0, new_card.shape[0] - 1]]).astype(np.float32)
```
- 計算轉換矩陣
```python
warp_mat = cv2.getPerspectiveTransform(src, dst)
```
- 轉換
```python
warp_dst = cv2.warpPerspective(
    new_card, warp_mat, (mask.shape[1], mask.shape[0]))
```

轉換後的圖片
![](https://i.imgur.com/Bb1evM4.png =35%x)




### 3. 挖出img中的卡片

#### 將mask黑白轉換

直接減去255``mask_blackObj = 255 - mask``

![](https://i.imgur.com/rkXfqNb.png =35%x)

#### img疊加mask

使用``cv2.bitwise_and``疊加剛剛黑白轉換的mask

![](https://i.imgur.com/4tsnYWV.jpg =35%x)

### 4. 貼上經過透視轉換的new_card於img上

使用``cv2.add``去合併

![](https://i.imgur.com/IMpt0St.jpg =35%x)

## Improvement

### 不要邊緣偵測


mask是BGR的圖片，需要convert it from BGR to grayscale (8UC1) format before finding contours.
==FindContours== function only supports a ==grayscale== image format.

```python
mask_grey = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
```

只用灰階後的mask去contour，會有noise，爛爛的
導致輪廓偵測的四個點還比第一次做的更不準
![](https://i.imgur.com/5ultbyp.png =35%x)

再用threshold binary
```python
ret, thre = cv2.threshold(mask_grey, 127, 255, cv2.THRESH_BINARY)
```
就會平平滑滑了
![](https://i.imgur.com/PtdJVB1.png =35%x)

### 不要minAreaRect()

#### Problem analysis 

合併在一起的result有右上角card和背景重疊的問題
mask 剛好的把 img.jpg 的中間挖掉了，所以不是他的問題
應該是card做perspective transform的座標有問題

minAreaRect 他只會算出==矩形==的中心和角度，多邊形的他沒辦法

#### Solution

改用``cv2.approxPolyDP``去找多邊形的頂點
![](https://i.imgur.com/TllmHw4.png =35%x)

但用這個座標是三維的，shape要改成(2,4)，還有數值的型態要轉換成float32

#### Result

![](https://i.imgur.com/sm7UqiO.jpg =35%x)


---
Reference：
1. [NumPy: 建立ndarray的常用方法](https://medium.com/@python.coding.site/numpy%E5%AD%B8%E7%BF%92101-6acb9fb3a6fe)
2. [numpy Array [: ,] 的取值方法](https://blog.csdn.net/w1300048671/article/details/76408070)
3. [Affine Transformations(for 三角形的) Python Code](https://docs.opencv.org/3.4/d4/d61/tutorial_warp_affine.html)
4. [Perspective transform講解](https://theailearner.com/tag/cv2-getperspectivetransform/)
5. [影像遮罩](https://steam.oxxostudio.tw/category/python/ai/opencv-mask.html)
6. [OpenCV – Contour輪廓](https://chtseng.wordpress.com/2016/12/05/opencv-contour%E8%BC%AA%E5%BB%93/)
7. [Python OpenCV 影像二值化 Image Thresholding](https://shengyu7697.github.io/python-opencv-threshold/)
8. [NumPy数组的变形（改变数组形状）](http://c.biancheng.net/view/7208.html)
9. [[Day 26] 從零開始學Python - 科學運算NumPy：人間用多少滄桑，換多少人的瘋狂](https://ithelp.ithome.com.tw/articles/10247302)
10. [How to use OpenCV and Python to find corners of a trapezoid similar to finding corners of a square?](https://stackoverflow.com/questions/64130631/how-to-use-opencv-and-python-to-find-corners-of-a-trapezoid-similar-to-finding-c)
