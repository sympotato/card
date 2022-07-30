# Github使用教學

## 概念

向雲端一樣的地方，可以將本機上的code存到網路上。

## 常用指令

1. 新增裝著所有要上傳的檔案資料夾以後，在資料夾中點右鍵選==Git bash here==，輸入以下指令
``git init`` -- repo初始化
``git status`` -- 查看目前資料夾中的檔案
``git add hello.txt`` -- 追蹤該檔案
``git add .`` -- 追蹤所有檔案
``git commit -m "first"`` -- 儲存變更(" "內要寫註記，註記你這次改了什麼而存檔，也可以寫first、1st等等)
commit 後看status會什麼都沒有是因為，status只顯示跟上一次commit不同的部分。
``git log`` -- 檢視歷史紀錄

2. 開始上傳到github
先在github網站上新增新的repo(新增時什麼都==別勾選==，直接建立)
``git remote add origin "https://github.com/sympotato/Mango.git"`` -- 將該新增的網址加入名叫origin的remote(遠端)
``git remote`` -- 會列出所有remote
``git push -u origin master`` -- 將資料推進github
-u是指會把origin設為預設

:::info
參考[影片](https://www.youtube.com/watch?v=Zd5jSDRjWfA)
:::

## Mac 小問題

要push時會發生的問題
即使密碼打對也會要求要使用token
![](https://i.imgur.com/0OdqK6P.png)

解決方法
去github點``setting``->滑到最底下找``Developer setting``->``Personal access tokens``->``Generate new token``->複製那行token->回到terminal再次push->但這次密碼就用這個token->完成！
[參考](https://www.wongwonggoods.com/linux/git/git-remote-support/)

###### tags: `github`
