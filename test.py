import random

def generate_run_stats(pace_min, pace_max, distance_min, distance_max):
    # 设置配速和路程的区间
    # pace_min, pace_max = 5, 7  # 配速区间（分钟/公里）
    # distance_min, distance_max = 0.8, 1.2  # 路程区间（公里）

    # 随机生成配速和路程
    random_pace = random.uniform(pace_min, pace_max)
    random_distance = random.uniform(distance_min, distance_max)

    # 计算所需时间（配速乘以路程）
    time_needed = random_pace * random_distance

    minutes1 = int(random_pace)
    seconds1 = round((random_pace - minutes1) * 60)

    # 处理秒数可能为60的进位情况
    if seconds1 == 60:
        minutes1 += 1
        seconds1 = 0

    # 使用字符串格式化来确保分钟和秒数都是合适的两位显示
    seconds_str1 = f"{seconds1:02d}"
    minutes_str1 = f"{minutes1:02d}"

    # 拼接成时间格式，例如 05'30" 或 11'05"
    time_str1 = f"{minutes_str1}'{seconds_str1}\""

    # 返回配速、路程和所需时间
    return time_str1, random_distance, time_needed


# 调用函数并输出结果
def convert_pace_to_time_format(pace_in_minutes_per_km):
    # 分离整数部分和小数部分
    minutes = int(pace_in_minutes_per_km)
    seconds = round((pace_in_minutes_per_km - minutes) * 60)
    if minutes < 10:
        minutes = "00:0" + str(minutes)
    elif 10 <= minutes < 60:
        minutes = "00:" + str(minutes)
    elif minutes >= 60:
        hours = minutes // 60
        if hours < 10:
            minutes = "0" + str(hours) + ":" + str(minutes - hours * 60)
        elif hours >= 10:
            minutes = str(hours) + ":" + str(minutes - hours * 60)

    # 使用字符串格式化来确保秒数是两位数
    seconds_str = f"{seconds:02d}"

    # 拼接成时间格式
    time_str = f"{minutes}:{seconds_str}"

    return time_str

def generate_random_time_between_22_and_23():
    # 生成0到59之间的随机分钟数
    random_minutes = random.randint(0, 59)
    random_hours = random.randint(6, 23)

    # 格式化时间为24小时制字符串
    random_time = f"{random_hours}:{random_minutes:02d}"

    return random_time


def generate_random_time_between_hours(start_hour, end_hour):
    """生成在给定小时范围内的随机时间（24 小时制）。

    支持跨午夜范围（例如 start_hour=22, end_hour=5），返回格式为 'HH:MM'。
    """
    minute = random.randint(0, 59)
    if start_hour is None:
        start_hour = 0
    if end_hour is None:
        end_hour = 23

    try:
        sh = int(start_hour)
        eh = int(end_hour)
    except Exception:
        sh, eh = 6, 23

    sh = max(0, min(23, sh))
    eh = max(0, min(23, eh))

    if sh <= eh:
        hour = random.randint(sh, eh)
    else:
        # 跨午夜：在 sh..23 或 0..eh 中选一个小时
        if random.choice([True, False]):
            hour = random.randint(sh, 23)
        else:
            hour = random.randint(0, eh)

    return f"{hour:02d}:{minute:02d}"

# 生成并打印随机时间
