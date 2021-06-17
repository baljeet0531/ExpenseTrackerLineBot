# ReadME.md

## 將修改的檔案push到遠端流程

> 通常我都用第一種
1. add >> commit >> pull(有comflict的話要處理) >> push
2. stash >> pull >> stash pop(有comflict的話要處理) >> add >> commit >> push

## git 操作
* **看哪些檔案有變動**
```
$ git status
```

* **add (加修改過的檔案準備commit)**
    * 加全部檔案
    ```
    $ git add . 
    ```
    * 只加Linebot_function.py及Linebot_server.py
    ```
    $ git add Linebot_function.py Linebot_server.py
    ```
* **commit**
```
$ git commit -m "commit title"
```
> commit title就看你這次做了什麼，自己取個標題
> for example: add notify feature, fix website bug之類的

* **pull (從遠端拉最新檔案)**
```
$ git pull origin master
```
* **push (將本機檔案上傳遠端)**
```
$ git push origin master
```

* **stash (暫存)**
```
$ git stash
```

* **stash pop (將暫存取出來)**
```
$ git stash pop
```