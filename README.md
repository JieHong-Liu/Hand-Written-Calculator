# HWC (Hand Write Calculator implemented by python.)
# HandWrite Calculator Project


+ APP LINK: https://hand-write-calculator.herokuapp.com/home
+ dataset : https://github.com/sueiras/handwritting_characters_database

+ 流程
    1. API處理
    2. API照片處理
    3. 手寫辨識處理
    4. latex語法計算 or CALL Wolfram Alpha API 

+ Heroku 帳號密碼
    + hwcalculator123@gmail.com
    + passwordHWC123@@
+ google 帳號密碼
    + ![](https://i.imgur.com/ogfNkPT.png)



+ [Project Gantt Chart](https://docs.google.com/spreadsheets/d/1qRaeDJop0vqYx3cT2eMnDg9TIcGX7atjdee7rgkw2dg/edit#gid=536189438)


+ 做專題時遇到的困難
    1. 如何post照片給後端
        + postman 上傳照片失敗
            + [解法](https://stackoverflow.com/questions/63987217/postman-error-while-uploading-files-through-form-data-body-type)
        + 後端flask如何接收上傳的照片
            + [解法](https://www.itread01.com/article/1533275386.html)
        + 結果
            + 正常結果
                + ![](https://i.imgur.com/iJyBIuU.png)
            + 上傳錯誤格式
                + ![](https://i.imgur.com/qkNHe67.png)
    2. 將API部屬至heroku
        + cv2 bug
            + https://stackoverflow.com/questions/63845382/importerror-libgl-so-1-error-when-accessing-heroku-app
        + Assertion Error:
            + 刪除一樣名字的function.
    3. API前後端串接
        + Internal Error 500
            + fetch寫法錯誤
    4. 將網頁發到heroku上
        + jinja2.exceptions.TemplateNotFound: ../index.html 
        + 也就是找不到html檔
            + [解法](https://blog.csdn.net/shangxiaqiusuo1/article/details/103684463)
            + https://ithelp.ithome.com.tw/articles/10222132        
        + 找不到js檔
            + 新增static的資料夾
    5. 環境建置
        + Python版本 3.6
        + 需要安裝的套件
            + HWC的requirements和scikit-learn以及scikit-image
            + opencv 版本 3.4.2.16
        + 目前需要修改的程式(short_test)
            ![](https://i.imgur.com/7d2ALOR.png)
            + 在model 加上  tf.reset_default_graph()即可修正
            ![](https://i.imgur.com/BJ8IeKX.png) 
   6. 需要放入HWC的必要檔案有哪些:
        + short_test.py
        + few_test_eq
        + Latex
        + model
        + seq_mod
        + Seq2SeqModel
        + train_images_mean.npy
        + train_images_std.npy
    7. flask後端return的資料回不到前端(只能在F12的response)
        + 解決方法
        ![](https://i.imgur.com/wREoSSb.png)
        + 第6行是指說我的回傳要轉成什麼型態，這邊選text(string的意思)
        + 再把回傳結果印出來 
        + 相關連結:https://ithelp.ithome.com.tw/articles/10252941 
    8. 檔案import失敗==
        + 解決方法:
    9. url decoding
        + '+'變成'%2B'
    10. 
        

+ 可能有用的連結:
    + [Wolfram Alpha API](https://products.wolframalpha.com/api/)
    + [Postman基本教學](https://xenby.com/b/151-%E6%8E%A8%E8%96%A6-%E4%BD%BF%E9%96%8B%E7%99%BCapi%E6%9B%B4%E6%96%B9%E4%BE%BF%E7%9A%84%E5%B7%A5%E5%85%B7-postman)
    + [API基本教學+前後端串聯(25~27)](https://ithelp.ithome.com.tw/users/20107247/ironman/3719)
    + [FLASK建立網站教學](https://ithelp.ithome.com.tw/users/20120116/ironman/2532)
    + [Heroku教學](https://www.youtube.com/watch?v=wWRYBUzEG6E&ab_channel=%E5%BD%AD%E5%BD%AD%E7%9A%84%E8%AA%B2%E7%A8%8B)
    + [Fetch - Web APIs](https://developer.mozilla.org/zh-TW/docs/Web/API/Fetch_API/Using_Fetch)
    + [JavaScript](https://ithelp.ithome.com.tw/articles/10213148)



$\int sin(x) dx$

+ wolfram alpha token:L6A69L-RRJU9794TQ

$( x + 4 ( / ( 2 + 3)$