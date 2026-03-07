# 原神角色语音包 for peon-ping

基于《原神》6.2 中文语音，为 18 个角色制作的 [CESP 1.0](https://openpeon.com/create) 格式语音包，适用于 [peon-ping](https://github.com/PeonPing/peon-ping)。

每个语音包覆盖全部 8 个 Open Peon 标准触发类别，每类 2–4 条音频，让 AI 编程助手的提示音有了更多角色选择。

---

## 角色列表

| 包名 | 角色 | 风格 |
|---|---|---|
| `nahida` | 纳西妲 | 草神，充满好奇心与知识渴望 |
| `furina` | 芙宁娜 | 水神，戏精性格，喜爱表演与掌声 |
| `hutao` | 胡桃 | 往生堂堂主，古灵精怪，顺口溜台词 |
| `klee` | 可莉 | 火花骑士，童声爆炸系，炸弹是最爱 |
| `sigewinne` | 希格雯 | 美露莘护士长，温柔治愈 |
| `diona` | 迪奥娜 | 猫耳调酒师，傲娇萝莉 |
| `sayu` | 早柚 | 风系忍者，嗜睡属性 |
| `yaoyao` | 瑶瑶 | 仙家弟子，乖巧懂事 |
| `qiqi` | 七七 | 僵尸小药师，记忆差靠笔记本 |
| `dori` | 多莉 | 奸商萝莉，摩拉至上 |
| `lynette` | 琳妮特 | 枫丹魔术师助手，猫耳无口 |
| `charlotte` | 夏洛蒂 | 蒸汽鸟报记者，真实至上 |
| `mika` | 米卡 | 西风骑士团测绘员，害羞正太 |
| `kachina` | 卡齐娜 | 纳塔回声之子，喜欢亮晶晶的石头 |
| `iansan` | 伊安珊 | 纳塔健身教练，活力少女 |
| `mualani` | 玛拉妮 | 纳塔向导，鲨鱼妹，热情开朗 |
| `citlali` | 茜特菈莉 | 纳塔黑曜石奶奶，烟谜主，反差萌 |
| `lanyan` | 蓝砚 | 纳塔青鸟，手工艺工会，随心而动 |

---

## 安装

**前置条件：** 已安装 [peon-ping](https://github.com/PeonPing/peon-ping)

```bash
# 克隆本仓库
git clone https://github.com/yourname/yuanshen-sound-pack.git
cd yuanshen-sound-pack

# 将语音包复制到 peon-ping 的包目录
cp -r packs/* ~/.openpeon/packs/
```

---

## 使用

```bash
# 切换到某个角色
peon packs use nahida

# 预览各触发类别效果
peon preview session.start
peon preview task.complete
peon preview task.error
peon preview --list

# 查看所有已安装语音包
peon packs list

# 切回默认包
peon packs use peon

# 多角色轮转（随机切换）
peon packs rotation add nahida,furina,hutao,klee,qiqi
peon rotation round-robin
```

---

## 音频类别映射

每个语音包均覆盖全部 8 个 CESP 标准类别，语音来源按角色性格精心挑选：

| 类别 | 触发时机 | 选用的语音类型 |
|---|---|---|
| `session.start` | 开始工作会话 | 早安/午安问候、角色初次登场台词 |
| `task.acknowledge` | 收到新任务 | 战斗技能施放语音（短促有力） |
| `task.complete` | 任务完成 | 宝箱开启、战斗技能命中成功 |
| `task.error` | 发生错误 | 被攻击语音（hit_H）、低血量语音 |
| `input.required` | 等待用户输入 | 闲置对话（idle）、角色待机 |
| `resource.limit` | 资源不足警告 | 低血量烦躁、体力警告语音 |
| `user.spam` | 用户操作过于频繁 | 队友低血量提醒、待机感叹 |
| `session.end` | 结束工作会话 | 夜间问候、告别语音 |

---

## 重新构建

如需从原始素材重新生成语音包（例如更换音频文件后）：

**前置条件：**
- Python 3.10+
- ffmpeg（用于将超过 1MB 的 WAV 文件压缩为 MP3）
- 原神 6.2 中文语音文件，解压至 `~/Downloads/yuanshen-chinese/`

```bash
python3 build_packs.py
cp -r packs/* ~/.openpeon/packs/
```

构建脚本会自动处理缺失文件（打印警告但不中断），并对超过 1MB 的 WAV 文件执行 `ffmpeg -qscale:a 4` 转码。

---

## 目录结构

```
packs/
├── nahida/
│   ├── openpeon.json        # CESP 清单文件
│   └── sounds/
│       ├── vo_nahida_dialog_greetingMorning.wav
│       ├── vo_nahida_battle_skill1_01.wav
│       └── ...
├── furina/
│   ├── openpeon.json
│   └── sounds/
└── ...
```

---

## 许可

音频内容版权归米哈游所有，本项目仅供个人学习与非商业使用。
语音包配置文件（`openpeon.json`）采用 [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/) 授权。
