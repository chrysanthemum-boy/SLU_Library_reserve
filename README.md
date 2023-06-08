# SLU_Library_reserve
SLU（上海立信会计金融学院）图书馆座位自动预约

## 请遵守以下使用协议
- 请合理使用此脚本，切勿占用公共资源。
- 本项目仅供学术交流使用，作者不对任何因使用本脚本造成的后果负责，包括但不仅限于由滥用脚本导致的封号，账号被锁定等。
- 本项目将停止维护并将被移除，当发生以下情况之一:  
  - 本项目被立信图书馆或校方要求删除。
  - 作者发现本项目影响到了立信图书馆正常的预约服务。
  - 作者发现本项目被滥用或有其他不妥之处。

## 使用说明
### config.json参数说明
```json
{
  "username": "",  填写你的学号
  "password": "",  填写你的密码
  "email": "",     填写你的邮箱
  "habit": [
    {
      "room": "Mulan_2F_book",  房间参数
      "seat_id": "PDT2FSK120",  座位编号
      "day": "today",  （tomorrow 或者 today） 预约日期（今明两天）
      "bt": "09:30:00",   开始时间
      "et": "22:30:00"    结束时间
    }
  ],
  "state": 1   用户配置激活：1，未使用：0
}
```

### 木兰图书馆room参数
|  room   | 具体位置  |
|  :----:  | :----:  |
| Mulan_1F_101  | 101阅览室 |
| Mulan_1F_102  | 102阅览室 |
| Mulan_1F_book  | 一楼书库 |
| Mulan_2F_book  | 二楼书库 |
| Mulan_2F_data  | 二楼数字体验空间 |
| Mulan_3F_book  | 三楼书库 |

### 文博楼room参数
|  room   | 具体位置  |
|  :----:  | :----:  |
| Wenbo_3F_A_1  | 三楼阅览室A-1区 |
| Wenbo_3F_A_2  | 三楼阅览室A-2区 |
| Wenbo_3F_A_3  | 三楼阅览室A-3区 |

## 鸣谢
感谢[gzhu-libbooking-master](https://github.com/lighthookyu/gzhu-libbooking-master) 作者提供的思路。

### 注
目前只有浦东校区的图书馆信息，后续如果有需求可以增加其他校区信息。 
