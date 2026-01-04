![wallpaper_20230818232154_00000046.jpg](https://4f2dd13d.zycs-img-3ao.pages.dev/v2/FwMUuVG.jpeg)

## 🤔 常用正则表达式

#### ⭕ 排除节点

```python
^((?!套餐|备用|重置|客户|Date|Reset|\d{3} GB|机场).)*$
```

## :white_check_mark: cron表达式

### :white_check_mark: 圈x task 任务中使用 cron 表达式规范

#### :sunglasses: 5 位说明

> \* \* \* \* \*  从左到右依次表示：分 时 日 月 星期

#### :sunglasses: 6 位说明

> \* \* \* \* \* \* 从左到右依次表示：秒 分 时 日 月 星期

#### :heavy_check_mark: 简单示例

> `*/4 7-22/1 * * *    每天7-22点 每4分钟执行一次`
>
> `* 9,12,18 * * *      每天9点 12点 18点分别执行一次`
>
>  `0 0-16/8 * * *        每天0点 8点 16点各一次`
>
>  `0 * * * *                 每1小时执行一次`

---

## 📑参考

:link:[圈 x 规则文件(🐱blackmatrix7)](https://github.com/blackmatrix7/ios_rule_script)

:link:[GitHub 正则表达式学习文档(超详细👍👍👍)](https://github.com/Parantric/learn-regex/blob/master/translations/README-cn.md)

[:link: 圈 x 图标仓库 ✪✪✪](https://github.com/Parantric/mini)

[🐶 GitHub 徽章生成网站](https://shields.io/category/test-results)

:link: [圈 x 官方配置(主要是知道有哪些标签)](https://github.com/Parantric/Quantumult-X-Official/blob/master/sample-my.conf)





