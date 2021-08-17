function postImage(url,formData){
  fetch(url,{ 
    method: 'POST',
    body: formData,
  })
  .then(function(response) {
    return response.text()
  }).then( (response) => {
    document.getElementById('resultSize').innerText = (response);
  })
}

function judge(x){
    if(x)
      return "Upload Error"
    else 
      return "Upload Success!"
}

function showImg(thisimg) { // 顯示上傳的圖片
	var img = thisimg.files[0];
	// if(window.FileReader) {
  //     var fr = new FileReader();
      
  //     var showimg = document.getElementById('showimg');
  //     fr.onloadend = function(e) {
  //     showimg.src = e.target.result;
	// };
	// fr.readAsDataURL(file);
	// showimg.style.display = 'block';
	// }
  // Check if the file is an image.
  let showimg = document.getElementById('showimg');
  const reader = new FileReader();
  reader.addEventListener('load', (event) => {
    showimg.src = event.target.result;
  });
  reader.readAsDataURL(img);
  showimg.style.display = 'block';
}

function getElementByXpath(path) {
  return document.evaluate(path, document, null, XPathResult.STRING_TYPE, null).stringValue;
}

function submit() {
    let formData = new FormData();
    let fileField = document.querySelector('input[type="file"]');
    console.log(fileField.files[0]);
    // url = 'https://hand-write-calculator.herokuapp.com/upload';
    // url = 'http://192.168.31.195:3000/upload';
    //let url = 'http://192.168.1.101:80/test_predict';
    let url = 'http://35.189.181.126:80/test_predict';
    formData.append('', fileField.files[0]);// 設定上傳的檔案
    postImage(url, formData);
    document.getElementById('resultText').innerText = judge((fileField.files[0])==undefined);
  }

function Evaluate(correct_or_not){ // 可以運算的地方
  document.getElementById('state').innerText = "OK";
  //let url='http://192.168.1.101:80/evaluate';
  let url= 'http://35.189.181.126:80/evaluate';
  if(correct_or_not == "true")
  {
    let ans = getElementByXpath('//*[@id="resultSize"]/text()[3]').replace("The text is ","");
    document.getElementById('detectionResult').innerText = ans;
  }
  else
  {
    document.getElementById('detectionResult').innerText = (document.getElementById('input_text').value)
  }
  let str = document.getElementById('detectionResult').innerText;
  let newStr = str;
  let count = 0;
  for (let i = 0 ; i < str.length; i++)
  {
    if(str[i] == '+')
    {
      count = count+1;
    }
  }
  for (let j = 0; j < count; j++)
  {
    newStr = newStr.replace('+','%2B');
  }

  let math_expresion = new FormData();
  math_expresion.append('question',newStr);
  fetch (url,{
      method: 'POST',
      body: math_expresion
    }).then(function(response) {
      return response.text()
    }).then( (response) => {
      document.getElementById('CalculateResult').innerText = (response);
    })
}
function modification(thistext){//之後修改
  let resultSize_text = document.getElementById('resultSize').innerText;
  let input_text = document.getElementById('input_text');
  input_text.style.display = 'block';
  let t = getElementByXpath('//*[@id="resultSize"]/text()[3]').replace("The text is ","");
  input_text.value = t;
  input_text_name = document.getElementById('input_text_name');
  input_text_name.innerText = "修改輸入";
  modified = document.getElementById('modified');
  modified.style.display = 'block';
}
  let Correct = document.getElementById("True"); //正確 
  let modified = document.getElementById("modified");//修正後遞交
  if(Correct)// Null的話不會去讀
      Correct.addEventListener('click',function(){Evaluate("true");});  
  if(modified)// Null的話不會去讀
      modified.addEventListener('click',function(){Evaluate("false");});  

  let Modify = document.getElementById("modify");//修正
  if(Modify)// Null的話不會去讀
      Modify.addEventListener('click',function(){modification()}); 

  let fileinput = document.getElementById("fileinput");//上傳圖片
  fileinput.addEventListener('change',function(){showImg(this)}); //當有事件發生改變，執行相應的函式  

  let submitt = document.getElementById("submitt");//遞交手寫資料
  if(submitt)// Null的話不會去讀
      submitt.addEventListener('click',function(){submit(); 
        Modify.style.display = 'block';  Correct.style.display = 'block'; });
