#  HandWrite Calculator Project (Public)

---
###### tags: `Object Detection`, `YOLOv4`
colaborator: [Kevin](https://github.com/kevin60613)

---
## Part0. Overview 

由於單純的程式碼對於一般使用者極度不友善，因此本研究在考量使用者需求時，決定將系統架設於網站上，並把系統分為前端(Front-End)與後端(Back-End)，前端主要是以GUI(Graphical User Interface)圖形使用者介面，友善且清楚地標示，提供使用者上傳數學式截圖的地方。而後端主要的功能就是將前端傳來的圖片，利用深度學習模型，以Expression Tree與Tree Traversal的方式將辨識結果以LaTex語法回傳給使用者，使得使用者可以加以確認辨識結果是否有問題，並再把經過使用者確認後的數學式回傳給後端，讓後端將確認無誤的數學式經由Wolfram Alpha的API計算，再計算後把數學式的最終答案回傳給使用者。

## Part1. System Flow Chart

![](https://i.imgur.com/XwIzU9o.png)


## Part2. Object Detection

We use 40000 pictures as our datasets and 20000 pictures as test set in this dataset [Aida Calculus Math Handwriting Recognition Dataset
](https://www.kaggle.com/datasets/aidapearson/ocr-data) 
And we use [YOLOv4](https://github.com/AlexeyAB/darknet) as our deep learning model.
We detect the math equation on the paper and send these information to our system. 

## Part3. Design Method (Algorithm)

### Expression Structured Tree

物件偵測進行完後，還必須加上一些處理，因為最終必須將預測的結果是以Latex語法顯示，在當物件偵測完成後，它只僅僅告訴我們物件的預測結果，而對於每個符號之間的相對關係並沒有明確地描述，所以在此專題加上了算式架構樹(Expression Structured Tree)，加上算式架構樹可以幫助我們有效分辨符號之間關係，也可以處理除法、根號、次方等複雜算式，判斷符號與符號之間的關係，主要有三種可能性，分別為上中下，一般狀況是判斷右邊的符號是否在左邊符號的上方、中間、下方，再根據判斷的結果建立樹節點。以圖一手寫式子為例，圖二為圖一所構成的樹，其中E為算式架構樹的根(root)、sq為平方根(square root)、s為次方(superscript)，建樹流程如圖三所示。

---

#### Fig.1 手寫運算式
![](https://i.imgur.com/g9VhcyQ.png)

#### Fig.2 算式架構樹
![](https://i.imgur.com/NYrooZZ.png)

#### Fig.3 建樹流程圖
![](https://i.imgur.com/F22tsHv.png)

---


### 算式架構樹的走訪

建立樹後，還必須要把樹的每個節點都走訪(traversal)一遍，這樣就可以按照符號之間的關係排好。這過程並不複雜，如次方只須加上^{}，來表示在括號裡的是指數，沒被括到的數字就是跟底數在同個水平軸上符號或數字，剩下符號像是除法或根號也是只須按照節點內容加上需要的符號即可完成。圖四為演算法的pseudo code.

---
#### Fig.4 Traversal的Pseudo code
![](https://i.imgur.com/PJ2WX2s.png)

---

## Part4. Experiemental Results

### Training Results
本專題使用Aida Calculus Math Handwriting Recognition Dataset註[2]，且取40000張圖片作為訓練集，20000張圖片作為驗證集。我們最後採用的權重為迭代18000次。mAP(Mean Average Precision)如圖五所示。

#### Fig.5 Mean Average Precision
![](https://i.imgur.com/xJeKnHp.png)

--- 
### Detection Results

利用了訓練18000次的權重，我們對手寫運算式圖六進行預測，辨識結果如圖七所示，再利用python的anytree套件將算式圖運算元之間相對關係轉換成算式架構樹，圖八為圖七的算式架構樹，走訪完算式架構樹後即可獲得以LaTeX語法表示的算式(如圖九)。

---

#### Fig.6 Origin Input
![](https://i.imgur.com/Pjw91Zm.png)
#### Fig.7 Detect operators and operends
![](https://i.imgur.com/2WD34nk.png)
#### Fig.8 Expression Structured Tree

![](https://i.imgur.com/5YMCyrb.png)
#### Fig.9 LaTeX output

![](https://i.imgur.com/7lWaoiD.png)

---

### Website Description

本專題將伺服器架設於GCP(Google Cloud Platform)，並且利用HTML, CSS以及JavaScript 搭配Bootstrap 進行前端使用者介面的設計（如圖10），而後端利用python中的Flask輕量級框架。在這個框架下，可以簡單地擴充各式各樣的功能，如本專題中最常使用到的「檔案上傳」。

使用者上傳圖片後，會交給後端去將數學式進行預測，並且在預測完後會詢問使用者此數學式是否正確，而預估算式則是利用JavaScript中的函式庫「Mathjax」，可以直接將LaTex數學式語法直接清楚的呈現。這時候使用者可以選擇「正確」或是「修正」來確定正確的數學式（如圖11），並再將確認沒問題的數學式傳到後端利用Wolfram alpha的API運算結果回傳給使用者（如圖12）。

---

#### Fig.10 前端圖形使用者介面(GUI)
![](https://i.imgur.com/P6YUBxc.png)
#### Fig.11 辨識數學式頁面
![](https://i.imgur.com/O1OwTAK.png)
#### Fig.12 計算結果頁面
![](https://i.imgur.com/jzt6pQZ.png)


---

## Part5. Suggestion and Conclusion

本研究中探討了YOLOv4(You Only Look Once)對於數學式的辨識的能力。在個別數字的辨識上我們以迭代18000次的權重，來對我們的輸入數學圖，進行數學式的辨識。在數學式的辨識上，我們是先將整張圖所有的運算子與運算元進行偵測，再偵測後，接著再利用我們的建樹方法將每個運算元依照運算子的x,y位置來決定是建在子樹還是兄弟節點（如分數、次方、四則運算等等），接著再以遞迴的方式去造訪每一個節點，並以該樹來輸出相對應的數學式。接著調用wolfram的API，將數學式進行運算並回傳給使用者。總而言之，我們這個專題提供給學生，或是任何對於數學式運算有困難的人士，一個友善的使用者介面及強大方便的辨識及運算能力。

## Part6. Future Works

為了提高辨識的精準度，未來物件辨識的深度學習模型可能會棄用速度快但精準度相對來說沒那麼高的單階段(one stage)網路(如本研究使用的YOLOv4)，轉而採用速度雖慢但是精度相對卻高許多的雙階段網路(two stage)來進行預測(如Faster R-CNN)。提供更多數學運算的功能(如反三角函數、對數、雙曲線函數等等)，在有良好的建樹方法基礎之下，想增加新功能僅僅需要增加新的訓練集及修改少部分的程式碼即可。


## Part7. References

[1] Zanibbi, R., Blostein, D., Cordy, J.R.: Recognizing mathematical expressions using tree transformation. IEEE Trans. PAMI, 24, 1455–1467 (2002)

[2] Aida Calculus Math Handwriting Recognition Dataset

[3] Brown wooden board photo (https://unsplash.com/photos/h0Vxgz5tyXA)
