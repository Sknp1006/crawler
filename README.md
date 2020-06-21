# crawlers
简介：基于scrapy的爬虫项目，主要是做着玩，并探索scrapy~  
## BiliBili crawler
项目描述：这是一个用于抓取哔哩哔哩视频弹幕和评论的爬虫，抓取范围是自己关注列表里全部UP主的视频。  
## AoiSloa crawler
### 项目描述：  
  * 绅士必备，妹子图爬虫( •̀ ω •́ )✧  
  * 在原同名项目的基础上修改了网站，以及优化了下载参数，添加了log.txt
  * 未来应该会有更多功能加入，敬请期待~
### 遇到的问题：
  * scrapy.Request与response.follow好像有性能上的差距，体现在使用follow的callback调用自己时，下载无法达到较高速度。  
  * 其次是用follow无法传递meta字典，我需要传递图片所在的分区名，例如：meinv

  
