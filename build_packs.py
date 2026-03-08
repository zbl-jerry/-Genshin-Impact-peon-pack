#!/usr/bin/env python3
"""
Build Genshin Impact Open Peon voice packs for 18 characters.
Copies WAV files and creates openpeon.json manifests.
"""

import os
import json
import shutil
import subprocess
from pathlib import Path

# Source base directory (override with env var YUANSHEN_SRC if needed)
SRC_BASE = Path(os.environ.get("YUANSHEN_SRC", Path.home() / "Downloads/yuanshen-chinese"))
# Output directory
OUT_BASE = Path(__file__).parent / "packs"

# Character definitions: (Chinese folder name, romanized pack name, display name, description)
# For each character: define category -> list of (source_file_stem, label) tuples
# Battle files are in "战斗语音 - Battle/" subdirectory

PACKS = [
    {
        "folder": "纳西妲",
        "name": "nahida",
        "display_name": "纳西妲 / Nahida",
        "description": "草神纳西妲，须弥的智慧之神，萝莉体型，充满好奇心与知识渴望。",
        "categories": {
            "session.start": [
                ("vo_nahida_dialog_greetingMorning", "早上好，我们赶快出发吧！", None),
                ("vo_nahida_draw_appear_01", "初次见面，我叫纳西妲", None),
                ("vo_nahida_dialog_greetingNoon", "午休时间到，我想喝树莓薄荷饮", None),
            ],
            "task.acknowledge": [
                ("vo_nahida_battle_skill1_01", "记住你了", "battle"),
                ("vo_nahida_battle_skill1_02", "蔓延吧", "battle"),
                ("vo_nahida_battle_skill3_01", "来我家做客吧~", "battle"),
                ("vo_nahida_character_idle_01", "不知道干什么的话，要不要我带你去转转呀", None),
            ],
            "task.complete": [
                ("vo_nahida_chest_open_01", "好奇心值得嘉奖哦", None),
                ("vo_nahida_battle_skill3_02", "知识，与你分享", "battle"),
                ("vo_nahida_chest_open_03", "有你想要的吗", None),
            ],
            "task.error": [
                ("vo_nahida_battle_hit_H_02", "被打晕了…", "battle"),
                ("vo_nahida_battle_hit_H_01", "好痛啊", "battle"),
            ],
            "input.required": [
                ("vo_nahida_character_idle_02", "又有心事吗？我来陪你一起想吧", None),
                ("vo_nahida_battle_skill1_03", "等下有点痛哦", "battle"),
            ],
            "resource.limit": [
                ("vo_nahida_dialog_annoyed", "有很多人是揣着明白装糊涂…", None),
                ("vo_nahida_battle_skill1_06", "全都看见咯", "battle"),
            ],
            "user.spam": [
                ("vo_nahida_character_idle_03", "果然要亲眼去看，才能感受到世界的美", None),
                ("vo_nahida_battle_skill1_05", "手牵手~", "battle"),
            ],
            "session.end": [
                ("vo_nahida_dialog_greetingNight", "太阳落山啦，把舞台让给夜行的大家族了", None),
                ("vo_nahida_dialog_greetingNight2", "快去睡吧，我已经为你准备好甜甜的梦啦", None),
            ],
        },
    },
    {
        "folder": "芙宁娜",
        "name": "furina",
        "display_name": "芙宁娜 / Furina",
        "description": "水神芙宁娜，枫丹的大明星，戏精性格，喜爱表演与掌声。",
        "categories": {
            "session.start": [
                ("vo_furina_draw_appear_01", "站在你面前的就是枫丹大明星——芙宁娜", None),
                ("vo_furina_dialog_greetingMorning", "早安…需要起这么早吗？", None),
                ("vo_furina_dialog_greetingNoon", "午安！我的蛋糕在哪里？", None),
            ],
            "task.acknowledge": [
                ("vo_furina_battle_skill3_01", "让世界热闹起来吧", "battle"),
                ("vo_furina_battle_skill3_03", "欢唱，以我之名！", "battle"),
                ("vo_furina_battle_skill1_02", "亮相啦！", "battle"),
            ],
            "task.complete": [
                ("vo_furina_battle_skill3_02", "闪耀时刻！", "battle"),
                ("vo_furina_chest_open_01", "意外之喜，就像蛋糕上的王冠", None),
                ("vo_furina_battle_skill1_04", "开幕", "battle"),
            ],
            "task.error": [
                ("vo_furina_battle_hit_H_01", "干什么啊！", "battle"),
                ("vo_furina_life_less30_03", "救命啊——", "battle"),
            ],
            "input.required": [
                ("vo_furina_character_idle_02", "好无聊啊，没有什么更有趣的事吗？", None),
                ("vo_furina_battle_skill1_01", "为我歌颂！", "battle"),
            ],
            "resource.limit": [
                ("vo_furina_battle_hit_H_02", "别打了！", "battle"),
                ("vo_furina_life_less30_01", "总之先休战…", "battle"),
            ],
            "user.spam": [
                ("vo_furina_character_idle_03", "人气太高也是一种苦恼，谁让我这么受欢迎呢", None),
                ("vo_furina_life_less30_teammate_02", "换我登场了！", "battle"),
            ],
            "session.end": [
                ("vo_furina_dialog_greetingNight2", "正好我也困了。明天见，记得准时叫我起来…", None),
                ("vo_furina_dialog_greetingNight", "晚上好", None),
            ],
        },
    },
    {
        "folder": "胡桃",
        "name": "hutao",
        "display_name": "胡桃 / Hu Tao",
        "description": "往生堂堂主胡桃，古灵精怪，顺口溜台词，热情豁达的生死观。",
        "categories": {
            "session.start": [
                ("vo_hutao_dialog_greetingMorning", "嗯~早起身体好，晚睡人会飘", None),
                ("vo_hutao_dialog_greetingNoon", "哟！中午好呀，吃了吗？", None),
                ("vo_hutao_dialog_greetingNight", "嘻嘻，月亮出来喽~咱也出门吧", None),
            ],
            "task.acknowledge": [
                ("vo_hutao_battle_skill1_01", "喝！", "battle"),
                ("vo_hutao_battle_skill1_02", "起！", "battle"),
                ("vo_hutao_battle_skill3_01", "吃饱喝饱，一路走好！", "battle"),
            ],
            "task.complete": [
                ("vo_hutao_chest_open_01", "撞大运咯！", None),
                ("vo_hutao_battle_skill3_02", "再会啦！", "battle"),
                ("vo_hutao_battle_skill3_03", "蝶火燎原！", "battle"),
            ],
            "task.error": [
                ("vo_hutao_battle_hit_H_02", "干嘛呀！", "battle"),
                ("vo_hutao_life_less30_03", "糟糕！", "battle"),
            ],
            "input.required": [
                ("vo_hutao_dialog_idle", "胡桃的胡是胡吃海喝的胡！嘿嘿…不好笑吗？", None),
                ("vo_hutao_life_less30_02", "噫——！", "battle"),
            ],
            "resource.limit": [
                ("vo_hutao_life_less30_01", "哎哟哎哟！", "battle"),
                ("vo_hutao_life_less30_teammate_01", "悠着点！", "battle"),
            ],
            "user.spam": [
                ("vo_hutao_life_less30_teammate_02", "放着我来！", "battle"),
                ("vo_hutao_chest_open_02", "让我看看，都有些什么好东西", None),
            ],
            "session.end": [
                ("vo_hutao_dialog_greetingNight2", "困了吗？那你好好休息，我一个人四处转转", None),
                ("vo_hutao_dialog_close", "有空也给我讲讲你自己的故事吧", None),
            ],
        },
    },
    {
        "folder": "可莉",
        "name": "klee",
        "display_name": "可莉 / Klee",
        "description": "火花骑士可莉，童声爆炸系，天真无邪，炸弹是她的最爱。",
        "categories": {
            "session.start": [
                ("vo_klee_dialog_greetingMorning", "早安！带可莉出去玩吧！", None),
                ("vo_klee_dialog_greetingNoon", "午饭时间到了！啊…吃什么呢？", None),
                ("vo_klee_chest_open_01", "可莉又找到新的宝物了！", None),
            ],
            "task.acknowledge": [
                ("vo_klee_battle_skill1_01", "蹦蹦炸弹！", "battle"),
                ("vo_klee_battle_skill3_01", "轰轰火花！", "battle"),
                ("vo_klee_life_less30_teammate_02", "你不要紧吧？", "battle"),
            ],
            "task.complete": [
                ("vo_klee_chest_open_02", "亮闪闪的，好开心！", None),
                ("vo_klee_battle_skill3_02", "火力全开！", "battle"),
                ("vo_klee_battle_skill3_03", "全——都可以炸完！", "battle"),
            ],
            "task.error": [
                ("vo_klee_battle_hit_H_02", "好疼啊！", "battle"),
                ("vo_klee_life_less30_01", "哇…怎么会这样…", "battle"),
            ],
            "input.required": [
                ("vo_klee_dialog_idle", "呜…这次居然炸歪了大风车的叶片…真对不起！", None),
                ("vo_klee_life_less30_02", "琴团长…它欺负我…", "battle"),
            ],
            "resource.limit": [
                ("vo_klee_life_die_02", "可莉…想回家了…", "battle"),
                ("vo_klee_life_less30_03", "玩累了，有点晕…", "battle"),
            ],
            "user.spam": [
                ("vo_klee_life_less30_teammate_01", "火花骑士，爆破支援！", "battle"),
                ("vo_klee_dialog_close", "能不能帮我隐瞒一下…", None),
            ],
            "session.end": [
                ("vo_klee_dialog_greetingNight2", "天黑以后…拜托你回去的时候，把我也送回家好不好…", None),
                ("vo_klee_dialog_greetingNight", "晚上好！可莉不是小孩子了", None),
            ],
        },
    },
    {
        "folder": "希格雯",
        "name": "sigewinne",
        "display_name": "希格雯 / Sigewinne",
        "description": "美露莘护士长希格雯，温柔治愈，专业且充满关怀。",
        "categories": {
            "session.start": [
                ("vo_sigewinne_draw_appear_01", "我是梅洛彼得堡的护士长希格雯，让我看看…这里疼吗？", None),
                ("vo_sigewinne_dialog_greetingMorning", "早上好，睡得好吗？用温水洗脸对皮肤刺激最小", None),
                ("vo_sigewinne_dialog_greetingNoon", "午饭时间快到了，我得暂时离开一下下", None),
            ],
            "task.acknowledge": [
                ("vo_sigewinne_battle_skill3_01", "谨誓！精研医理", "battle"),
                ("vo_sigewinne_battle_skill3_03", "医嘱：即刻注射", "battle"),
                ("vo_sigewinne_battle_skill1_02", "我看看", "battle"),
            ],
            "task.complete": [
                ("vo_sigewinne_chest_open_03", "可爱的人值得最好的宝物", None),
                ("vo_sigewinne_battle_skill3_02", "别紧张哦，放松", "battle"),
                ("vo_sigewinne_life_less30_teammate_02", "救援到了！", "battle"),
            ],
            "task.error": [
                ("vo_sigewinne_battle_hit_H_01", "生气了！", "battle"),
                ("vo_sigewinne_battle_hit_H_02", "你不可爱！", "battle"),
            ],
            "input.required": [
                ("vo_sigewinne_character_idle_02", "哪里磕着碰着了吗？不舒服要随时叫我哟", None),
                ("vo_sigewinne_battle_skill1_01", "别动哟", "battle"),
            ],
            "resource.limit": [
                ("vo_sigewinne_life_less30_01", "我能治疗自己！", "battle"),
                ("vo_sigewinne_battle_skill1_03", "冷静", "battle"),
            ],
            "user.spam": [
                ("vo_sigewinne_life_less30_teammate_01", "看来得强制治疗了…", "battle"),
                ("vo_sigewinne_life_less30_03", "没关系的…", "battle"),
            ],
            "session.end": [
                ("vo_sigewinne_dialog_greetingNight", "几点啦？我喜欢黑漆漆的地方", None),
                ("vo_sigewinne_dialog_greetingNight2", "感觉入睡很困难？来聊聊心事吧", None),
            ],
        },
    },
    {
        "folder": "迪奥娜",
        "name": "diona",
        "display_name": "迪奥娜 / Diona",
        "description": "猫耳调酒师迪奥娜，傲娇萝莉，致力于调出难喝的酒来打击酒业。",
        "categories": {
            "session.start": [
                ("vo_diona_dialog_greetingMorning", "早，我要开始摧毁蒙德酒业啦", None),
                ("vo_diona_dialog_greetingNoon", "最多…最多只能给你尝一口", None),
                ("vo_diona_chest_open_02", "亮晶晶的…想要…扑过去！", None),
            ],
            "task.acknowledge": [
                ("vo_diona_battle_skill1_03", "目标确认", "battle"),
                ("vo_diona_battle_skill1_04", "攻守兼备", "battle"),
                ("vo_diona_battle_skill3_03", "反省吧，酒鬼！", "battle"),
            ],
            "task.complete": [
                ("vo_diona_battle_skill3_01", "迪奥娜特调！", "battle"),
                ("vo_diona_chest_open_01", "让酒变难喝的材料啊，出现吧！", None),
                ("vo_diona_battle_skill1_05", "抓到你了！", "battle"),
            ],
            "task.error": [
                ("vo_diona_life_less30_03", "胜负还没分呢！", "battle"),
                ("vo_diona_life_less30_02", "喵…喵…！", "battle"),
            ],
            "input.required": [
                ("vo_diona_dialog_idle", "耳朵和尾巴才不是什么装饰，是血统的象征！", None),
                ("vo_diona_dialog_annoyed", "到底怎样才能调出难喝的酒呢…呜…我不会认输的…", None),
            ],
            "resource.limit": [
                ("vo_diona_life_less30_01", "我不会认输…！", "battle"),
                ("vo_diona_life_less30_teammate_02", "去休息去休息！", "battle"),
            ],
            "user.spam": [
                ("vo_diona_battle_skill3_02", "贪杯的下场…哼！", "battle"),
                ("vo_diona_battle_skill1_06", "我可不好欺负！", "battle"),
            ],
            "session.end": [
                ("vo_diona_dialog_greetingNight2", "你没有猫的夜视能力，走夜路不要紧吧？", None),
                ("vo_diona_dialog_close", "想喝无酒精饮料？难倒是不难，但是没有意义！", None),
            ],
        },
    },
    {
        "folder": "早柚",
        "name": "sayu",
        "display_name": "早柚 / Sayu",
        "description": "风系忍者早柚，嗜睡属性，随时随地都想睡觉，懒散的终末番忍者。",
        "categories": {
            "session.start": [
                ("vo_sayu_dialog_greetingMorning", "已经…已经早上了吗？再睡10分钟…就10分钟嘛…", None),
                ("vo_sayu_dialog_greetingNoon", "好困，午睡时间还不到吗？", None),
                ("vo_sayu_character_idle_01", "呼啊…呼噜呼噜——", None),
            ],
            "task.acknowledge": [
                ("vo_sayu_battle_skill3_02", "出来吧！", "battle"),
                ("vo_sayu_battle_skill1_04", "极意遁走", "battle"),
                ("vo_sayu_battle_skill3_01", "分身之术", "battle"),
            ],
            "task.complete": [
                ("vo_sayu_chest_open_02", "大丰收！可以睡觉了吗？", None),
                ("vo_sayu_battle_skill1_05", "抓不住我…呜", "battle"),
                ("vo_sayu_chest_open_01", "这个箱子…好像可以睡进去", None),
            ],
            "task.error": [
                ("vo_sayu_battle_hit_H_02", "呜，要晕倒了", "battle"),
                ("vo_sayu_life_die_03", "不该偷懒的…", "battle"),
            ],
            "input.required": [
                ("vo_sayu_character_idle_02", "工作还不如睡觉", None),
                ("vo_sayu_life_less30_02", "头晕乎乎的", "battle"),
            ],
            "resource.limit": [
                ("vo_sayu_life_less30_03", "呼，好累", "battle"),
                ("vo_sayu_dialog_idle", "一直拖着不做，就会有更合适的人去做", None),
            ],
            "user.spam": [
                ("vo_sayu_life_less30_teammate_02", "先退下休息", "battle"),
                ("vo_sayu_life_less30_teammate_01", "我来掩护", "battle"),
            ],
            "session.end": [
                ("vo_sayu_dialog_greetingNight", "确认完毕，方圆十里内没有巫女姐姐。今晚可以睡个好觉啦~", None),
                ("vo_sayu_dialog_greetingNight2", "终于…可以睡觉了…晚…晚安…", None),
            ],
        },
    },
    {
        "folder": "瑶瑶",
        "name": "yaoyao",
        "display_name": "瑶瑶 / Yaoyao",
        "description": "仙家弟子瑶瑶，乖巧懂事，师从歌尘浪市真君，月桂是她的好伙伴。",
        "categories": {
            "session.start": [
                ("vo_yaoyao_dialog_greetingMorning", "该起床啦，我已经准备好早饭了！", None),
                ("vo_yaoyao_draw_appear_01", "初次见面，我是瑶瑶，忝列门墙，师从歌尘浪市真君", None),
                ("vo_yaoyao_dialog_greetingNoon", "吃完午饭后，不要立刻躺下午睡哦", None),
            ],
            "task.acknowledge": [
                ("vo_yaoyao_battle_skill1_01", "月桂！该上咯", "battle"),
                ("vo_yaoyao_battle_skill3_01", "预备…跑！", "battle"),
                ("vo_yaoyao_character_idle_01", "「明日复明日」总之，快快行动起来吧", None),
            ],
            "task.complete": [
                ("vo_yaoyao_chest_open_03", "哇！这些够用好几天了吧", None),
                ("vo_yaoyao_battle_skill3_02", "痛痛飞", "battle"),
                ("vo_yaoyao_chest_open_01", "都收好，不要落下哦！", None),
            ],
            "task.error": [
                ("vo_yaoyao_battle_hit_H_02", "好痛好痛…", "battle"),
                ("vo_yaoyao_life_less30_01", "不行不行…", "battle"),
            ],
            "input.required": [
                ("vo_yaoyao_character_idle_02", "那边好像有什么动静，偷偷看一眼应该没事吧！", None),
                ("vo_yaoyao_battle_skill1_02", "不要乱动哦！", "battle"),
            ],
            "resource.limit": [
                ("vo_yaoyao_life_less30_03", "没事，我可以的…", "battle"),
                ("vo_yaoyao_life_less30_02", "我要撑下去…", "battle"),
            ],
            "user.spam": [
                ("vo_yaoyao_life_less30_teammate_02", "人命关天，不要勉强！", "battle"),
                ("vo_yaoyao_life_less30_teammate_01", "让瑶瑶保护你！", "battle"),
            ],
            "session.end": [
                ("vo_yaoyao_dialog_greetingNight", "晚上还要出门吗？天色已晚，小心为上哦~", None),
                ("vo_yaoyao_dialog_greetingNight2", "睡前故事…呼呼…", None),
            ],
        },
    },
    {
        "folder": "七七",
        "name": "qiqi",
        "display_name": "七七 / Qiqi",
        "description": "僵尸小药师七七，记忆差，总是忘事，靠笔记本记录生活。",
        "categories": {
            "session.start": [
                ("vo_qiqi_dialog_greetingMorning", "早上了吗？今天要做的是…我看看笔记", None),
                ("vo_qiqi_dialog_greetingNoon", "…忘记帮白先生分拣药材了", None),
                ("vo_qiqi_chest_open_02", "宝箱…有用吗？", None),
            ],
            "task.acknowledge": [
                ("vo_qiqi_battle_skill1_02", "生生不绝", "battle"),
                ("vo_qiqi_battle_skill1_03", "去", "battle"),
                ("vo_qiqi_battle_skill3_01", "听诏，宣此诰命", "battle"),
            ],
            "task.complete": [
                ("vo_qiqi_chest_open_01", "好看", None),
                ("vo_qiqi_battle_skill1_01", "流转不息", "battle"),
                ("vo_qiqi_battle_skill3_02", "真名，度厄真君", "battle"),
            ],
            "task.error": [
                ("vo_qiqi_battle_hit_H_01", "居然…", "battle"),
                ("vo_qiqi_life_less30_03", "要活下去…", "battle"),
            ],
            "input.required": [
                ("vo_qiqi_dialog_idle", "你问我吗…？对不起，我不记得了…", None),
                ("vo_qiqi_life_less30_teammate_01", "危险", "battle"),
            ],
            "resource.limit": [
                ("vo_qiqi_life_less30_01", "痛", "battle"),
                ("vo_qiqi_life_die_02", "好冷…", "battle"),
            ],
            "user.spam": [
                ("vo_qiqi_life_less30_teammate_02", "我来吧", "battle"),
                ("vo_qiqi_battle_hit_L_02", "没感觉…", "battle"),
            ],
            "session.end": [
                ("vo_qiqi_dialog_greetingNight", "晚上好。今天…我做了什么来着…", None),
                ("vo_qiqi_dialog_close", "很多事情我都记不起来了，但是…也没什么不好", None),
            ],
        },
    },
    {
        "folder": "多莉",
        "name": "dori",
        "display_name": "多莉 / Dori",
        "description": "奸商萝莉多莉，摩拉至上，万能商店应有尽有，神灯精灵是她的助手。",
        "categories": {
            "session.start": [
                ("vo_dori_dialog_greetingMorning", "昨晚的梦里全是圆滚滚的可爱摩拉，今天一定会是盆满钵满的一天", None),
                ("vo_dori_character_idle_01", "我爱摩拉，摩拉爱我，啦啦啦", None),
                ("vo_dori_dialog_idle", "万能的多莉商店，应有尽有，童叟无欺", None),
            ],
            "task.acknowledge": [
                ("vo_dori_battle_skill1_02", "看我的！", "battle"),
                ("vo_dori_chest_open_02", "先让我看看", None),
                ("vo_dori_battle_skill3_01", "魔灯显灵！", "battle"),
            ],
            "task.complete": [
                ("vo_dori_chest_open_01", "哇，分我一半！", None),
                ("vo_dori_battle_skill3_02", "大显身手时间！", "battle"),
                ("vo_dori_battle_skill3_03", "一手交钱，一手交货", "battle"),
            ],
            "task.error": [
                ("vo_dori_battle_hit_H_01", "欺人太甚！", "battle"),
                ("vo_dori_battle_hit_H_02", "列进黑名单！", "battle"),
            ],
            "input.required": [
                ("vo_dori_dialog_annoyed", "拿着才三成利的生意就来打扰我…没有百分百的利润我连听完的兴趣都没有", None),
                ("vo_dori_life_less30_02", "啊救命啊，抢劫啦！", "battle"),
            ],
            "resource.limit": [
                ("vo_dori_life_less30_01", "休想抢走我一分摩拉！", "battle"),
                ("vo_dori_life_less30_03", "一定要保护好摩拉", "battle"),
            ],
            "user.spam": [
                ("vo_dori_life_less30_teammate_02", "命和摩拉一样重要", "battle"),
                ("vo_dori_life_less30_teammate_01", "救命之恩，记得给钱！", "battle"),
            ],
            "session.end": [
                ("vo_dori_dialog_greetingNight", "在夜色中赶路很有挑战性，不过这可难不倒常年在外行商的我！", None),
                ("vo_dori_dialog_greetingNight2", "你要睡觉了吗？嘿嘿，让你试试我的摩拉歌谣催眠法吧！", None),
            ],
        },
    },
    {
        "folder": "琳妮特",
        "name": "lynette",
        "display_name": "琳妮特 / Lynette",
        "description": "枫丹魔术师助手琳妮特，猫耳女仆，话少冷淡，是林尼的忠实搭档。",
        "categories": {
            "session.start": [
                ("vo_lynette_draw_appear_01", "初次见面，我是林尼的魔术助手，工作事宜请咨询林尼", None),
                ("vo_lynette_dialog_greetingMorning", "早安…充能尚未完成，即将再次休眠", None),
                ("vo_lynette_character_idle_01", "茶泡好了，接下来可以休息一会儿了", None),
            ],
            "task.acknowledge": [
                ("vo_lynette_battle_skill3_02", "来点灯光", "battle"),
                ("vo_lynette_battle_skill3_03", "请看这边", "battle"),
                ("vo_lynette_battle_skill1_02", "在这里", "battle"),
            ],
            "task.complete": [
                ("vo_lynette_chest_open_02", "不出所料", None),
                ("vo_lynette_chest_open_03", "轻松到手", None),
                ("vo_lynette_battle_skill3_01", "魔术开场", "battle"),
            ],
            "task.error": [
                ("vo_lynette_battle_hit_H_01", "啊，没躲开", "battle"),
                ("vo_lynette_life_die_02", "魔术失误了…", "battle"),
            ],
            "input.required": [
                ("vo_lynette_character_idle_03", "进入待机模式…希望不要有人来打扰我", None),
                ("vo_lynette_battle_skill1_03", "惊喜", "battle"),
            ],
            "resource.limit": [
                ("vo_lynette_life_less30_03", "启动应敌模式…", "battle"),
                ("vo_lynette_life_less30_01", "保持冷静", "battle"),
            ],
            "user.spam": [
                ("vo_lynette_life_less30_teammate_01", "快退后", "battle"),
                ("vo_lynette_life_less30_teammate_02", "我来吸引火力", "battle"),
            ],
            "session.end": [
                ("vo_lynette_dialog_greetingNight", "晚上的演出会很精彩，要给你留票吗？", None),
                ("vo_lynette_dialog_greetingNight2", "快睡吧，我还要处理白天没做完的事情…", None),
            ],
        },
    },
    {
        "folder": "夏洛蒂",
        "name": "charlotte",
        "display_name": "夏洛蒂 / Charlotte",
        "description": "蒸汽鸟报记者夏洛蒂，热情活泼，追求真实至上的新闻精神。",
        "categories": {
            "session.start": [
                ("vo_charlotte_draw_appear_01", "我是《蒸汽鸟报》记者夏洛蒂，你愿意接受我的专项访谈吗？", None),
                ("vo_charlotte_dialog_greetingMorning", "早上好，今天的报纸看了吗？没有？那我念给你听", None),
                ("vo_charlotte_dialog_greetingNoon", "是午饭时间了呀，我知道一家餐厅很不错，跟我来吧", None),
            ],
            "task.acknowledge": [
                ("vo_charlotte_battle_skill3_01", "真实至上！", "battle"),
                ("vo_charlotte_battle_skill1_01", "看镜头！", "battle"),
                ("vo_charlotte_battle_skill1_02", "笑一个", "battle"),
            ],
            "task.complete": [
                ("vo_charlotte_battle_skill3_02", "爆炸新闻！", "battle"),
                ("vo_charlotte_battle_skill3_03", "夏洛蒂，为您报道！", "battle"),
                ("vo_charlotte_chest_open_01", "喔！看上去不错", None),
            ],
            "task.error": [
                ("vo_charlotte_battle_hit_H_02", "我的镜头！", "battle"),
                ("vo_charlotte_life_less30_02", "还有新闻要报道！", "battle"),
            ],
            "input.required": [
                ("vo_charlotte_character_idle_01", "只要眼睛够尖，脑子够快，每天都能找到好新闻", None),
                ("vo_charlotte_battle_skill1_03", "摆个好姿势！", "battle"),
            ],
            "resource.limit": [
                ("vo_charlotte_life_less30_teammate_02", "喂！我可不想写讣告！", "battle"),
                ("vo_charlotte_battle_hit_L_02", "真不礼貌", "battle"),
            ],
            "user.spam": [
                ("vo_charlotte_life_less30_teammate_01", "小心点！", "battle"),
                ("vo_charlotte_life_less30_01", "我、我还能记录…", "battle"),
            ],
            "session.end": [
                ("vo_charlotte_dialog_greetingNight", "晚上最适合谈心了，你有什么故事愿意和我分享吗？", None),
                ("vo_charlotte_dialog_greetingNight2", "晚安，赶紧休息吧。我还要去报社校对稿件，明天见啦", None),
            ],
        },
    },
    {
        "folder": "米卡",
        "name": "mika",
        "display_name": "米卡 / Mika",
        "description": "西风骑士团前进测绘员米卡，害羞正太，认真负责，热爱队友。",
        "categories": {
            "session.start": [
                ("vo_mika_draw_appear_01", "西风骑士团游击小队所属，前进测绘员米卡，向你报到！", None),
                ("vo_mika_dialog_greetingMorning", "早啊，我准备了远征队常吃的早饭，说说今天的行动计划吧？", None),
                ("vo_mika_dialog_greetingNoon", "游击小队最爱的三号野战午餐很快就准备好", None),
            ],
            "task.acknowledge": [
                ("vo_mika_battle_skill3_02", "我负责医疗！", "battle"),
                ("vo_mika_battle_skill1_04", "精确射击！", "battle"),
                ("vo_mika_battle_skill1_06", "肃清威胁！", "battle"),
            ],
            "task.complete": [
                ("vo_mika_chest_open_01", "是新的收获！", None),
                ("vo_mika_chest_open_03", "找到了宝藏，恭喜大家！", None),
                ("vo_mika_battle_skill3_03", "打开突破口！", "battle"),
            ],
            "task.error": [
                ("vo_mika_life_die_03", "完了…我搞砸了…", "battle"),
                ("vo_mika_battle_hit_H_02", "不能慌张…", "battle"),
            ],
            "input.required": [
                ("vo_mika_character_idle_01", "赶快调整好状态，不知道下个任务什么时候会来", None),
                ("vo_mika_life_less30_02", "要改变战术吗？", "battle"),
            ],
            "resource.limit": [
                ("vo_mika_life_less30_01", "有点麻烦…", "battle"),
                ("vo_mika_life_less30_03", "对手…很强啊", "battle"),
            ],
            "user.spam": [
                ("vo_mika_life_less30_teammate_01", "请后撤，我来顶住！", "battle"),
                ("vo_mika_battle_skill3_01", "大家，请振作！", "battle"),
            ],
            "session.end": [
                ("vo_mika_dialog_greetingNight", "如果有需要维护的装备，也请交给我吧", None),
                ("vo_mika_dialog_greetingNight2", "时间还早，我要整理今天的勘测记录。请你先休息吧", None),
            ],
        },
    },
    {
        "folder": "卡齐娜",
        "name": "kachina",
        "display_name": "卡齐娜 / Kachina",
        "description": "纳塔回声之子卡齐娜，鼠兔设定，喜欢亮晶晶的石头，想要变强。",
        "categories": {
            "session.start": [
                ("vo_kachina_draw_appear_01", "你好呀，我是「回声之子」的卡齐娜。喜欢吃颗粒果，想要变强", None),
                ("vo_kachina_dialog_greetingMorning", "早呀，我已经整理好背包啦，我们随时可以出发", None),
                ("vo_kachina_chest_open_01", "哇哇，有亮晶晶的石头！", None),
            ],
            "task.acknowledge": [
                ("vo_kachina_battle_skill1_01", "旋转！", "battle"),
                ("vo_kachina_battle_skill1_05", "冲地波！", "battle"),
                ("vo_kachina_life_less30_teammate_02", "我在！交给我吧！", "battle"),
            ],
            "task.complete": [
                ("vo_kachina_battle_skill3_01", "清退！", "battle"),
                ("vo_kachina_life_less30_03", "我、我一定可以的！", "battle"),
                ("vo_kachina_battle_skill3_03", "切勿靠近", "battle"),
            ],
            "task.error": [
                ("vo_kachina_life_die_03", "呜…又搞砸了吗…", "battle"),
                ("vo_kachina_battle_hit_H_02", "唔，不要紧", "battle"),
            ],
            "input.required": [
                ("vo_kachina_character_idle_02", "我可以、我不行、我可以…唔唔，没事的，我可以的！", None),
                ("vo_kachina_character_idle_01", "刚刚发现有块砖没有堆整齐。怎么办？心里有只小龙在不停地挠啊挠", None),
            ],
            "resource.limit": [
                ("vo_kachina_life_less30_01", "没事，小伤罢了", "battle"),
                ("vo_kachina_life_less30_02", "我要…振作起来", "battle"),
            ],
            "user.spam": [
                ("vo_kachina_life_less30_teammate_01", "不要忘了还有我呀！", "battle"),
                ("vo_kachina_life_die_01", "对不起，是我逞强了", "battle"),
            ],
            "session.end": [
                ("vo_kachina_dialog_greetingNight2", "今天怎么又把事情给搞砸了，呜呜呜…晚安，谢谢你安慰我…", None),
                ("vo_kachina_friendship_05", "这个世界上一定有我才能做到的事。我会…继续努力", None),
            ],
        },
    },
    {
        "folder": "伊安珊",
        "name": "iansan",
        "display_name": "伊安珊 / Iansan",
        "description": "纳塔健身教练伊安珊，活力少女，力量训练狂热者，热情开朗。",
        "categories": {
            "session.start": [
                ("vo_iansan_draw_appear_01", "叫我伊安珊就好，我是那里最有名的健身教练。对健身感兴趣吗？", None),
                ("vo_iansan_dialog_greetingMorning", "嗨，早上好啊。要不要一起晨跑？", None),
                ("vo_iansan_dialog_greetingNoon", "中午好啊，有好好吃午餐吧？", None),
            ],
            "task.acknowledge": [
                ("vo_iansan_battle_skill3_01", "动起来！", "battle"),
                ("vo_iansan_battle_skill1_01", "风驰电掣！", "battle"),
                ("vo_iansan_battle_skill1_02", "更快，更强！", "battle"),
            ],
            "task.complete": [
                ("vo_iansan_chest_open_01", "天道酬勤", None),
                ("vo_iansan_battle_skill3_02", "计时开始！", "battle"),
                ("vo_iansan_battle_skill3_03", "听我的口号！", "battle"),
            ],
            "task.error": [
                ("vo_iansan_battle_hit_H_02", "这还像回事…", "battle"),
                ("vo_iansan_life_die_02", "这下练出事了…", "battle"),
            ],
            "input.required": [
                ("vo_iansan_character_idle_01", "今天的指标还不够，再做一组吧", None),
                ("vo_iansan_life_less30_02", "快到极限了吗？", "battle"),
            ],
            "resource.limit": [
                ("vo_iansan_life_less30_01", "还行，再咬咬牙！", "battle"),
                ("vo_iansan_life_less30_03", "得留意下肌肉的承受能力了…", "battle"),
            ],
            "user.spam": [
                ("vo_iansan_life_less30_teammate_01", "悠着点！", "battle"),
                ("vo_iansan_life_less30_teammate_02", "小心肌肉拉伤！", "battle"),
            ],
            "session.end": [
                ("vo_iansan_dialog_greetingNight2", "该休息咯，熬夜可是健身的大忌", None),
                ("vo_iansan_dialog_greetingNight", "刚入夜的这段时间很适合到户外做一些运动。要不要试试？", None),
            ],
        },
    },
    {
        "folder": "玛拉妮",
        "name": "mualani",
        "display_name": "玛拉妮 / Mualani",
        "description": "纳塔向导玛拉妮，鲨鱼妹，热情开朗，冲浪是她的标志。",
        "categories": {
            "session.start": [
                ("vo_mualani_draw_appear_01", "尊敬的旅行者，欢迎你参加本次旅行，我是向导玛拉妮！", None),
                ("vo_mualani_dialog_greetingMorning", "好消息，今天没有睡过头！奖励我自己吃顿超豪华早餐吧", None),
                ("vo_mualani_character_idle_01", "只要你来了，剩下的全都交给我来安排吧", None),
            ],
            "task.acknowledge": [
                ("vo_mualani_battle_skill1_01", "起乘！", "battle"),
                ("vo_mualani_battle_skill3_02", "飞澜鲨鲨！", "battle"),
                ("vo_mualani_battle_skill3_03", "看我看我！祝你好运！", "battle"),
            ],
            "task.complete": [
                ("vo_mualani_chest_open_01", "我就说今天是幸运日吧！", None),
                ("vo_mualani_battle_skill1_04", "哟呼！", "battle"),
                ("vo_mualani_battle_skill1_05", "超棒！", "battle"),
            ],
            "task.error": [
                ("vo_mualani_battle_hit_H_01", "别太过分！", "battle"),
                ("vo_mualani_life_less30_02", "今天的运势不太好…", "battle"),
            ],
            "input.required": [
                ("vo_mualani_character_idle_02", "你试过追着海浪奔跑吗？想试吗？要试吗？就现在！", None),
                ("vo_mualani_life_less30_03", "我会赢…我会赢！", "battle"),
            ],
            "resource.limit": [
                ("vo_mualani_life_less30_01", "我还要保护我的旅客", "battle"),
                ("vo_mualani_battle_hit_H_02", "我的冲浪板——", "battle"),
            ],
            "user.spam": [
                ("vo_mualani_life_less30_teammate_02", "过分，换我来揍它！", "battle"),
                ("vo_mualani_character_idle_03", "一群人就能挑战很多不可能！", None),
            ],
            "session.end": [
                ("vo_mualani_dialog_greetingNight2", "在篝火晚会上跳舞跳精神了，今晚肯定睡不着了…呜", None),
                ("vo_mualani_dialog_close1", "我们早就是可以互相托付生命的伙伴了", None),
            ],
        },
    },
    {
        "folder": "茜特菈莉",
        "name": "citlali",
        "display_name": "茜特菈莉 / Citlali",
        "description": "纳塔黑曜石奶奶茜特菈莉，烟谜主，反差萌，神秘又可爱。",
        "categories": {
            "session.start": [
                ("vo_citlali_draw_appear_01", "「烟谜主」的茜特菈莉，已经透过迷烟看到了未来的道路。请让我也同行", None),
                ("vo_citlali_dialog_greetingMorning", "啊——早上好啊。说吧，什么事？", None),
                ("vo_citlali_dialog_greetingNoon", "中午好啊。起床到中午是不会喝酒的…", None),
            ],
            "task.acknowledge": [
                ("vo_citlali_battle_skill1_02", "履行盟约吧，星魔们", "battle"),
                ("vo_citlali_battle_skill3_01", "灭口交给你们俩了！", "battle"),
                ("vo_citlali_battle_skill1_01", "出来干活！", "battle"),
            ],
            "task.complete": [
                ("vo_citlali_chest_open_01", "挺好的，收下吧", None),
                ("vo_citlali_battle_skill3_02", "茜特菈琳、伊兹帕帕，给我上！", "battle"),
                ("vo_citlali_chest_open_02", "先收下，答谢诸星的祈祷我替你做", None),
            ],
            "task.error": [
                ("vo_citlali_battle_hit_H_01", "好胆子！", "battle"),
                ("vo_citlali_battle_hit_H_02", "疼疼！", "battle"),
            ],
            "input.required": [
                ("vo_citlali_dialog_annoyed_01", "看起来什么都不在乎只是我的保护色，其实我什么都很在乎", None),
                ("vo_citlali_life_less30_02", "唉，想回家啊", "battle"),
            ],
            "resource.limit": [
                ("vo_citlali_life_less30_03", "不能…在你面前…", "battle"),
                ("vo_citlali_life_less30_01", "不该出门的…", "battle"),
            ],
            "user.spam": [
                ("vo_citlali_life_less30_teammate_02", "给奶奶我小心点", "battle"),
                ("vo_citlali_life_less30_teammate_01", "…不许死！", "battle"),
            ],
            "session.end": [
                ("vo_citlali_dialog_greetingNight2", "晚安。今晚恶曜不显，地灵微眠。是个好夜晚", None),
                ("vo_citlali_dialog_close1", "在你面前的局促才是真的我。这个真心话我只说一次", None),
            ],
        },
    },
    {
        "folder": "蓝砚",
        "name": "lanyan",
        "display_name": "蓝砚 / Lan Yan",
        "description": "纳塔青鸟设定蓝砚，手工艺工会成员，温柔声线，随心而动。",
        "categories": {
            "session.start": [
                ("vo_lanyan_draw_appear_01", "你好，我是沉玉谷手工艺工会的蓝砚。想做点摆件、篮子还是花瓶？", None),
                ("vo_lanyan_dialog_greetingMorning", "被鸟叫吵醒了？哈哈，我去跟它们商量商量", None),
                ("vo_lanyan_dialog_greetingNoon", "采了些很新鲜的花，你也来嘛，我家里人见到你肯定高兴！", None),
            ],
            "task.acknowledge": [
                ("vo_lanyan_battle_skill3_01", "搬疾运厄", "battle"),
                ("vo_lanyan_battle_skill1_04", "翻飞", "battle"),
                ("vo_lanyan_dialog_close", "坐好。朋友。握手~", None),
            ],
            "task.complete": [
                ("vo_lanyan_chest_open_02", "好消息！你快看里面有什么？", None),
                ("vo_lanyan_battle_skill3_02", "玄燕传喜", "battle"),
                ("vo_lanyan_battle_skill3_03", "漫卷翩翩", "battle"),
            ],
            "task.error": [
                ("vo_lanyan_battle_hit_H_02", "脾气真差！", "battle"),
                ("vo_lanyan_life_die_03", "飞不起来…", "battle"),
            ],
            "input.required": [
                ("vo_lanyan_character_idle_01", "今天的计划？听随当下的心意而动。每天都是，嘻嘻", None),
                ("vo_lanyan_life_less30_02", "有人帮忙吗？", "battle"),
            ],
            "resource.limit": [
                ("vo_lanyan_life_less30_03", "难办了…", "battle"),
                ("vo_lanyan_life_less30_01", "给我点时间…", "battle"),
            ],
            "user.spam": [
                ("vo_lanyan_life_less30_teammate_01", "不能硬撑了，快撤下来！", "battle"),
                ("vo_lanyan_battle_hit_H_01", "不对头！", "battle"),
            ],
            "session.end": [
                ("vo_lanyan_dialog_greetingNight2", "我好困…先睡了先睡了，就不陪你熬夜了", None),
                ("vo_lanyan_friendship_05", "最最重要的，是「开心」。要开心呀！我也是，你也是！", None),
            ],
        },
    },
    {
        "folder": "雷电将军",
        "name": "raiden",
        "display_name": "雷电将军 / Raiden Shogun",
        "description": "稻妻雷电将军，雷神·巴尔泽布，追求永恒的神祇，肃穆威严，言简意赅。",
        "categories": {
            "session.start": [
                ("vo_raidenEi_mimitomo_morning_02", "早安", None),
                ("vo_raidenEi_dialog_greetingNoon", "正午了", None),
                ("vo_raidenEi_mimitomo_hello_02", "你来了", None),
            ],
            "task.acknowledge": [
                ("vo_raidenShogun_battle_skill1_01", "斩！", "battle"),
                ("vo_raidenShogun_battle_skill1_02", "雷罚", "battle"),
                ("vo_raidenShogun_battle_skill3_01", "梦想一刀", "battle"),
            ],
            "task.complete": [
                ("vo_raidenShogun_battle_skill3_02", "一切归于永恒", "battle"),
                ("vo_raidenShogun_battle_skill3_03", "此乃神之裁决", "battle"),
                ("vo_raidenEi_starUp_04", "不负所望", None),
            ],
            "task.error": [
                ("vo_raidenShogun_battle_hit_H_01", "——！", "battle"),
                ("vo_raidenShogun_battle_hit_H_02", "放肆", "battle"),
            ],
            "input.required": [
                ("vo_raidenEi_dialog_annoyed", "心存杂念，则百事难成", None),
                ("vo_raidenEi_dialog_pendant", "永恒之道，不可动摇", None),
            ],
            "resource.limit": [
                ("vo_raidenShogun_life_less30_01", "无妨", "battle"),
                ("vo_raidenShogun_life_less30_02", "坚持", "battle"),
                ("vo_raidenShogun_life_less30_03", "……", "battle"),
            ],
            "user.spam": [
                ("vo_raidenShogun_life_less30_teammate_01", "撤退", "battle"),
                ("vo_raidenShogun_life_less30_teammate_02", "注意", "battle"),
            ],
            "session.end": [
                ("vo_raidenEi_dialog_greetingNight", "夜深了", None),
                ("vo_raidenEi_mimitomo_night_01", "好好休息", None),
            ],
        },
    },
]


MAX_FILE_BYTES = 1_000_000  # 1MB limit per CESP spec


def copy_or_convert(src: Path, dest_dir: Path) -> tuple[str, str]:
    """Copy file to dest_dir, converting to MP3 if WAV exceeds 1MB.
    Returns (filename, extension)."""
    stem = src.stem
    if src.suffix.lower() == ".wav" and src.stat().st_size > MAX_FILE_BYTES:
        # Convert to MP3
        dest_mp3 = dest_dir / f"{stem}.mp3"
        subprocess.run(
            ["ffmpeg", "-i", str(src), "-codec:a", "libmp3lame", "-qscale:a", "4", str(dest_mp3), "-y"],
            capture_output=True, check=True
        )
        return f"{stem}.mp3", ".mp3"
    else:
        dest_wav = dest_dir / f"{stem}.wav"
        shutil.copy2(src, dest_wav)
        return f"{stem}.wav", ".wav"


def find_audio_file(char_folder: str, stem: str, subdir: str | None) -> Path | None:
    """Find a WAV audio file. Returns the path if found, None otherwise."""
    base = SRC_BASE / char_folder
    if subdir == "battle":
        search_dir = base / "战斗语音 - Battle"
    else:
        search_dir = base

    wav_path = search_dir / f"{stem}.wav"
    if wav_path.exists():
        return wav_path
    return None


def build_pack(pack: dict) -> dict:
    """Build a single voice pack. Returns stats."""
    char_name = pack["name"]
    char_folder = pack["folder"]
    out_dir = OUT_BASE / char_name
    sounds_dir = out_dir / "sounds"
    sounds_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    missing = []
    categories_json = {}

    for category, files in pack["categories"].items():
        sound_entries = []
        for stem, label, subdir in files:
            src_path = find_audio_file(char_folder, stem, subdir)
            if src_path:
                dest_name, _ = copy_or_convert(src_path, sounds_dir)
                sound_entries.append({
                    "file": f"sounds/{dest_name}",
                    "label": label
                })
                copied += 1
            else:
                missing.append(f"{category}/{stem}")

        if sound_entries:
            categories_json[category] = {"sounds": sound_entries}

    # Write openpeon.json
    manifest = {
        "cesp_version": "1.0",
        "name": char_name,
        "display_name": pack["display_name"],
        "version": "1.0.0",
        "description": pack["description"],
        "author": {
            "name": "yuanshen-sound-pack",
            "github": "yuanshen-sound-pack"
        },
        "license": "CC-BY-NC-4.0",
        "language": "zh",
        "categories": categories_json
    }

    with open(out_dir / "openpeon.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return {"name": char_name, "copied": copied, "missing": missing}


def main():
    print(f"Building {len(PACKS)} voice packs...")
    OUT_BASE.mkdir(parents=True, exist_ok=True)

    all_stats = []
    for pack in PACKS:
        stats = build_pack(pack)
        all_stats.append(stats)
        status = "✓" if not stats["missing"] else "⚠"
        print(f"  {status} {stats['name']}: {stats['copied']} files copied", end="")
        if stats["missing"]:
            print(f", {len(stats['missing'])} missing: {stats['missing'][:3]}", end="")
        print()

    total_copied = sum(s["copied"] for s in all_stats)
    total_missing = sum(len(s["missing"]) for s in all_stats)
    print(f"\nDone! Total: {total_copied} files copied, {total_missing} missing")
    print(f"Packs written to: {OUT_BASE}")


if __name__ == "__main__":
    main()
