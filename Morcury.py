import jieba
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

jieba.load_userdict(r"围棋词库.txt")

def display(vector, name):
    # 创建3D坐标系
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 定义向量

    v = np.array(vector)
    v = 5 * v / np.sqrt(np.sum(v ** 2))

    # 绘制原点到向量的箭头
    ax.quiver(0, 0, 0, v[0], v[1], v[2], color='r')

    # 设置坐标轴标签

    ax.set_xlabel('peace <——> fight')
    ax.set_ylabel('area <——> potential')
    ax.set_zlabel('fun <——> serious')

    # 设置坐标轴范围
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])
    fig.suptitle("Style of this player")
    text = "f_or_p: {}\np_or_a: {}\ns_or_f: {}".format(v[0], v[1], v[2])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(-200, 200, 200, text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    # 显示图形
    plt.show()  # 创建3D坐标系


fight_or_peace = [['战斗', '乱战', '厮杀', '凶狠', '凌厉','中盘', '复杂', '急躁', '缠斗', '计算',
                   '严厉', '杀棋', '凶悍', '战力', '大龙','难解', '杀', '搏杀', '强硬', '气合',
                   '攻击', '对攻', '攻杀', '战', '混战', '作战', '挑衅', '顽强'],
                  ['稳健', '平稳', '保守', '围空', '大局', '大局观', '简明', '和平', '厚实', '厚味',
                   '胆小', '软弱', '避战', '铺地板', '老实', '官子', '防守', '稳重', '功夫', '稳妥',
                   '均衡', '收官', '布局', '崩盘']]

potential_or_area = [['外势', '厚势', '模样', '大模样', '宇宙流', '三连星', '天元', '取势', '潜力', '屠龙',
                      '规模', '大龙', '气势', '围剿', '中腹', '高目', '目外', '自由', '奔放', '大空'],
                     ['实地', '取地', '地盘', '打入', '治孤', '抢空', '目数', '腾挪', '地沟流', '做活',
                      '活棋', '实空', '先捞后洗', '捞', '洗', '逃亡', '侵入', '点三三', '小块', '割据']]

serious_or_fun = [['长考', '认真', '棋道', '艺术', '美感', '人生', '纹枰', '细腻', '精细', '境界',
                   '流水'],
                  ['快棋', '打勺', '勺', '勺子', '等勺流', '愚形', '飞刀', '快乐', '娱乐', '玩',
                   '抽象', '自由', '随性', '搅局']]


class Player:
    def __init__(self, name, level, style):
        self.name = name
        self.level = level
        self.style = style

    def save(self):
        with open("players.txt", "a") as f:
            f.write(f"{self.name},{self.level},{self.style}\n")


def add_player():
    name = input("请输入选手姓名：")
    level = input("请输入选手棋力：")
    style = input("请输入选手风格：")
    player = Player(name, level, style)
    player.save()
    print("选手信息已保存！")


def find_player_by_name(name):
    with open("players.txt", "r") as f:
        for i, line in enumerate(f):
            player_info = line.strip().split(",")
            if player_info[0] == name:
                return Player(player_info[0], player_info[1], player_info[2]), i
    return None, None


def match_all_players():
    with open("players.txt", "r") as f:
        for i, line in enumerate(f):
            player_info = line.strip().split(",")
            name = player_info[0]
            find_best_match_player2(name)
            print('\n')


def find_player():
    name = input("请输入要查找的选手姓名：")
    player, i = find_player_by_name(name)
    if player is not None:
        print(f"选手姓名：{player.name}")
        print(f"选手棋力：{player.level}")
        print(f"选手风格：{player.style}")
        style_words = [word for word in jieba.cut(player.style) if word != '，']
        print(style_words)
        value = style_to_value(style_words)
        print(value)
        display(value, name)
    else:
        print("未找到该选手！")


def delete_player():
    name = input("请输入要删除的选手姓名：")
    player, line_num = find_player_by_name(name)
    if player is not None:
        with open("players.txt", "r") as f:
            lines = f.readlines()
        with open("players.txt", "w") as f:
            for i, line in enumerate(lines):
                if i != line_num:
                    f.write(line)
        print(f"已删除选手：{player.name}")
    else:
        print("未找到该选手！")


def style_to_value(style_words):
    style_value = [0, 0, 0]
    for i in style_words:
        if i in fight_or_peace[0]:
            style_value[0] += len(i)
        elif i in fight_or_peace[1]:
            style_value[0] -= len(i)
        if i in potential_or_area[0]:
            style_value[1] += len(i)
        elif i in potential_or_area[1]:
            style_value[1] -= len(i)
        if i in serious_or_fun[0]:
            style_value[2] += len(i)
        elif i in serious_or_fun[1]:
            style_value[2] -= len(i)

    return style_value


def find_best_match_player2(name):
    print(name)
    player_a, _ = find_player_by_name(name)
    if player_a is None:
        print("没有找到该选手！")
        return
    style_words_a = [word for word in jieba.cut(player_a.style) if word != '，']
    a = style_to_value(style_words_a)

    a_level = eval(player_a.level)

    best_match_name = None
    max_match_value = -1000
    for line in open("players.txt", "r"):
        player_info = line.strip().split(",")
        if player_info[0] != name:
            player_b = Player(player_info[0], player_info[1], player_info[2])
            style_words_b = [word for word in jieba.cut(player_b.style) if word != '，']
            b = style_to_value(style_words_b)
            b_level = eval(player_b.level)
            # 匹配的对手：同时喜欢战争或和平，一个喜欢外势一个喜欢实地，同时认真围棋或快乐围棋
            match_value = a[0] * b[0] - a[1] * b[1] + a[2] * b[2] - abs((a_level - b_level) / 100)
            #print(player_b.name, "和TA的匹配分数为: ", match_value)
            if match_value > max_match_value:
                max_match_value = match_value
                best_match_name = player_b.name
    if max_match_value == -1000:
        print("没有匹配的选手！")
    else:
        print(f"最匹配的选手是{best_match_name}")


print("欢迎使用围棋比赛选手信息管理系统！")
print("请输入棋风时在50字以内~")
while True:
    print("请输入您的操作: ")
    print("1. 添加选手")
    print("2. 查找选手")
    print("3. 删除选手")
    print("4. 匹配选手")
    print("5. 一键匹配")
    print("6. 退出系统")
    choice = input("请选择操作：")
    if choice == "1":
        add_player()
    elif choice == "2":
        find_player()
    elif choice == "3":
        delete_player()
    elif choice == '4':
        Name = input("请输入要匹配的选手名字：")
        find_best_match_player2(Name)
    elif choice == '5':
        match_all_players()
    elif choice == '6':
        break
    else:
        print("无效的选项，请重新选择！")
print("墨尘棋社倾情感谢您使用本产品，欢迎下次再来！")