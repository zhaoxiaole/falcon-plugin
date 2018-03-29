# falcon-plugin
open-falcon activemq监控脚本

系统需求

操作系统：Linux Python >= 2.6

主要逻辑

从activemq-server的api接口读取相关数据,agent获取数据

汇报字段
--------------------------------
| metric |  tags | type | note |
|--------|-------|------|------|
|activemq_pending|name(Queue名字)|GAUGE|队列中处于等待被消费状态消息数|
|activemq_consumers|name(Queue名字)|GAUGE|队列消费者数量|
|activemq_enqueue|name(Queue名字)|GAUGE|队列入队消息总数|
|activemq_dequeued|name(Queue名字)|GAUGE|队列完成消费的消息数|
|activemq_enqueue_rate|name(Queue名字)|COUNTER|队列入队消息的speed|
|activemq_dequeued_rate|name(Queue名字)|COUNTER|队列消费的speed|

使用方法

1、修改60_activemq-monitor.py脚本的url，username，password

2、将脚本放到falcon-agent的plugin目录，在portal中将对应的plugin绑定到主机组，falcon-agent会主动执行60_activemq-monitor.py脚本，60_activemq-monitor.py脚本执行结束后会输出json格式数据，由falcon-agent读取和解析数据

