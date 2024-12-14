# Vlmeting
针对CVE抓取的一款工具，支持windows、Linux
使用方法：

例如 Windows版本

Web端

解压好后，可以用phpstudy 宝塔登启动一个web端，建议php版本7.4

例如：

原生启动：php -S 0.0.0.0 -t /目录

服务端（用于采集数据）：

window：

Vlmeting.exe -h
![cad1f6b256b07c927ce8b55430d5ea1d](https://github.com/user-attachments/assets/07a80365-a690-42a7-b5d9-1c3c4fa893f9)
编辑填好config.yaml后

正常启动：

第一次启动建议加-c（启动服务正常抓取所有数据）

Vlmeting.exe -s -c -t 1 

-f参数指定指纹抓取，包含指纹里面的都会推送，具体可以自行添加finger.yaml

Vlmeting.exe -s -c -t 1  -f

最后启动完后将web端的upload.php路径修改成:随机符号(自己定义)834u94394ttf.php （安全）

把修改完的路径放到服务端的config.yaml,启动服务端，如何web端就可以看到内容了

![image](https://github.com/user-attachments/assets/8a0a8d21-25b5-46df-ba36-a7ba8c11c589)




