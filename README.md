# rhyme_helper

- 简介：
    - rhyme_helper是一个Shell下的押韵字词寻找工具
    - 用户输入汉字序列,程序会为用户返回一些与所输汉字押韵的字或词

- 安装
    1. 用户必须首先安装python3环境、mysql数据库以及pymysql包
    2. mysql中创建一个新的数据库，并将给出的rhyme_helper.sql导入到新创建的数据库中
    3. 在rhyme_config.cfg文件中修改mysql连接所用用户名、密码和数据库名

- 用法: `python3 rhyme_helper.py ChineseWords [wide/nowide] [amount]`

- 示例:
    ````
    $ python3 rhyme_helper.py 网 wide 20
    上 行 场 方 长 长 当 商 量 将 向 强 强 两 厂 广 党 项 放 相
    ````

- 最后: 纯属自娱自乐
