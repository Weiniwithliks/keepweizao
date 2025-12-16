import os
import random
import re
import shutil
import tkinter as tk
from tkinter import *
from tkinter import filedialog

from PIL import ImageFont, ImageDraw, Image

import test


def save_image():
    filepath = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[("JPEG files", "*.jpg")])
    if filepath:
        try:
            img = Image.open('combined_image.jpg')  # 打开之前生成的图片
            img.save(filepath)  # 保存到用户指定的位置
            print(f"Image saved to: {filepath}")
        except Exception as e:
            print(f"Error saving image: {e}")

        # 窗口主函数


def create_window():
    root = tk.Tk()
    root.title("Input Window")

    # 创建变量来保存输入框的内容
    month_var = tk.StringVar()
    num_suiji_var = tk.StringVar()
    pace_min_var = tk.StringVar()
    pace_max_var = tk.StringVar()
    distance_min_var = tk.StringVar()
    distance_max_var = tk.StringVar()
    start_day_var = tk.StringVar()
    end_day_var = tk.StringVar()
    start_time_var = tk.StringVar()
    end_time_var = tk.StringVar()

    # 创建输入框
    entries = [
        (tk.Entry(root, textvariable=month_var), "月份（单月/逗号/区间，例如 1,3,5 或 1-3)"),
        (tk.Entry(root, textvariable=num_suiji_var), "次数，输入整数，每月生成的次数"),
        (tk.Entry(root, textvariable=pace_min_var), "配速最小值，输入整数（分钟/公里）"),
        (tk.Entry(root, textvariable=pace_max_var), "配速最大值，输入整数（分钟/公里）"),
        (tk.Entry(root, textvariable=distance_min_var), "路程最小值，输入整数（公里）"),
        (tk.Entry(root, textvariable=distance_max_var), "路程最大值，输入整数（公里）"),
        (tk.Entry(root, textvariable=start_day_var), "起始日(1-31),可与月份联合限制生成范围"),
        (tk.Entry(root, textvariable=end_day_var), "结束日(1-31,)可与月份联合限制生成范围"),
        (tk.Entry(root, textvariable=start_time_var), "起始小时(0-23)，用于随机时间生成，默认6"),
        (tk.Entry(root, textvariable=end_time_var), "结束小时(0-23)，用于随机时间生成，默认23")
    ]

    # 布局输入框
    for i, (entry, label) in enumerate(entries):
        entry.grid(row=i, column=0)
        tk.Label(root, text=label).grid(row=i, column=1)

        # 创建处理按钮
    # 根据输入框数量动态设置按钮位置，避免重叠
    btn_row = len(entries)
    tk.Button(root, text="Process", command=lambda: main(
        month_var.get(), num_suiji_var.get(), pace_min_var.get(), pace_max_var.get(), distance_min_var.get(),
        distance_max_var.get(), start_day_var.get(), end_day_var.get(), start_time_var.get(), end_time_var.get()
    )).grid(row=btn_row, column=0, columnspan=2, pady=4)

    # 创建另存为按钮
    tk.Button(root, text="Save Image", command=save_image).grid(row=btn_row+1, column=0, columnspan=2, pady=4)

    root.mainloop()


def main(month, num_suiji, pace_min, pace_max, distance_min, distance_max, start_day, end_day, start_time, end_time):
    temp_dir = 'output_temp'
    os.makedirs(temp_dir, exist_ok=True)

    # 解析months输入，支持单月、逗号分隔或区间（例如: 1,3,5 或 1-3）
    def parse_months(month_str):
        months = set()
        for part in month_str.split(','):
            part = part.strip()
            if not part:
                continue
            if '-' in part:
                a, b = part.split('-', 1)
                try:
                    start = int(a); end = int(b)
                except ValueError:
                    continue
                if start <= end:
                    months.update(range(start, end + 1))
                else:
                    months.update(range(end, start + 1))
            else:
                try:
                    months.add(int(part))
                except ValueError:
                    continue
        return sorted(m for m in months if 1 <= m <= 12)

    months_list = parse_months(month)
    if not months_list:
        tk.messagebox.showerror(title='错误', message='月份输入无效')
        return

    # 解析起始/结束日
    def parse_day(d_str, default):
        try:
            v = int(d_str)
            if 1 <= v <= 31:
                return v
        except Exception:
            pass
        return default

    start_day_val = parse_day(start_day, 1)
    end_day_val = parse_day(end_day, 31)

    # 解析起始/结束小时
    def parse_hour(h_str, default):
        try:
            v = int(h_str)
            if 0 <= v <= 23:
                return v
        except Exception:
            pass
        return default

    start_hour_val = parse_hour(start_time, 6)
    end_hour_val = parse_hour(end_time, 23)

    # 为每个月生成图片，保存到 temp_dir/{month}月
    for m in months_list:
        month_dir = os.path.join(temp_dir, f"{m}月")
        os.makedirs(month_dir, exist_ok=True)

        # 生成随机天数列表，按月份最大天数和全局起止日进行裁剪
        num = int(num_suiji)
        if m == 2:
            month_max = 28
        elif m in (1, 3, 5, 7, 8, 10, 12):
            month_max = 31
        else:
            month_max = 30

        # 计算当月有效起止日
        # 全局起始/结束日可能跨月份，例如 9-12 月且起始21 结束16 -> 从9月21开始到12月16结束
        # 如果只有单个月，使用 start_day_val..end_day_val，否则根据月份位置裁剪
        if len(months_list) == 1:
            low = max(1, start_day_val)
            high = min(month_max, end_day_val)
        else:
            first_month = months_list[0]
            last_month = months_list[-1]
            if m == first_month:
                low = max(1, start_day_val)
                high = month_max
            elif m == last_month:
                low = 1
                high = min(month_max, end_day_val)
            else:
                low = 1
                high = month_max

        if low > high:
            # 当起止日在同月无效时，跳过该月
            continue

        available = list(range(low, high + 1))
        if num > len(available):
            num = len(available)
        random_numbers = random.sample(available, num)
        sorted_numbers = sorted(random_numbers)

        for i in sorted_numbers:
            pace, distance, time = test.generate_run_stats(int(pace_min), int(pace_max), float(distance_min),
                                                           float(distance_max))
            pace_get = pace
            distance_get = str(distance)[:4]
            time1 = test.convert_pace_to_time_format(time)
            time_get = time1
            random_time = test.generate_random_time_between_hours(start_hour_val, end_hour_val)

            img = Image.open('back.jpg')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype('msyh.ttc', size=34)
            text = "{}月{}日".format(m, i)
            draw.rectangle((46, 50, 178, 83), fill='white')
            draw.text((46, 50), text, font=font, fill=(105, 105, 105))

            text2 = "户外跑步{} 公里".format(distance_get)
            font2 = ImageFont.truetype('msyh.ttc', size=40)
            draw.rectangle((169, 172, 512, 210), fill='white')
            draw.text((169, 172), text2, font=font2, fill=(35, 35, 35))

            text3 = "用时 {}  配速 {}".format(time_get, pace_get)
            font = ImageFont.truetype('msyh.ttc', size=34)
            draw.rectangle((170, 247, 589, 275), fill='white')
            draw.text((170, 242), text3, font=font, fill=(74, 74, 74))

            text4 = random_time
            font = ImageFont.truetype('msyh.ttc', size=36)
            draw.rectangle((938, 209, 1030, 238), fill='white')
            draw.text((938, 209), text4, font=font, fill=(152, 152, 152))
            # 文件名包含月份，避免不同月份冲突
            img.save(os.path.join(month_dir, f"{m}_{i}.jpg"))

    # 将 100.jpg（若存在）复制到 temp 根目录以参与合并
    if os.path.exists('100.jpg'):
        try:
            shutil.copyfile('100.jpg', os.path.join(temp_dir, '100.jpg'))
        except Exception:
            pass

    # 收集所有生成的图片（包括子文件夹）
    image_files = []
    for root, _, files in os.walk(temp_dir):
        for f in files:
            if f.endswith('.jpg'):
                image_files.append(os.path.join(root, f))

    if not image_files:
        tk.messagebox.showerror(title='错误', message='没有找到生成的图片')
        return

    # 按文件名中出现的数字进行排序（支持月份与日子组合，如 3_12.jpg）
    def num_key(path):
        nums = re.findall(r'\d+', os.path.basename(path))
        return tuple(int(n) for n in nums) if nums else (0,)

    image_files.sort(key=num_key, reverse=True)

    widths, heights = zip(*(Image.open(f).size for f in image_files))
    max_width = max(widths)
    total_height = sum(heights)

    new_img = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for img_file in image_files:
        with Image.open(img_file) as img:
            new_img.paste(img, (0, y_offset))
            y_offset += img.height

    new_img.save('combined_image.jpg')
    # 清理临时目录
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass

    message = '图片创建成功，请点击Save Image获取'
    tk.messagebox.showinfo(title='提示', message=message)


# 运行窗口主函数
create_window()
