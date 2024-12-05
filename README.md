### 基于原wxauto开源工程扩展功能，细节可以查看原工程文档

### 欢迎指出bug

### Windows版本微信客户端自动化，可实现单一会话的当前图片、视频自动存储，目前代码仅限法定工作日运行

### 使用方式
配置backup_config.ini，指定会话名称以及存储目的路径
[BackupSettings]
chat_name = xxx
backup_base_dir = xxx

运行python wechat_media_backup.py

可以扩展使用windows上任务计划程序进行每日自动执行

### 注意事项
未完整测试，使用过程中可能遇到各种Bug

### 免责声明
代码仅用于技术的交流学习使用，禁止用于实际生产项目，请勿用于非法用途和商业用途！如因此产生任何法律纠纷，均与作者无关！



