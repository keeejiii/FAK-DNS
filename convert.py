import os
import glob

def convert_conf_to_txt(conf_file, txt_file, cn_dns):
    with open(conf_file, 'r') as conf:
        with open(txt_file, 'w') as txt:
            for line in conf:
                parts = line.strip().split('=')
                if len(parts) != 2:
                    # 忽略无效行
                    continue
                domain = parts[1].split('/')[1]
                txt.write(f"[/{domain}/]" + cn_dns + "\n")

def main():
    current_directory = os.getcwd()  # 获取当前目录
    converted_directory = os.path.join(current_directory, 'converted')  # 创建 converted 文件夹
    os.makedirs(converted_directory, exist_ok=True)  # 确保 converted 文件夹存在

    # ================= 修改开始 =================
    # 原代码：使用 glob 匹配所有 *china.conf
    # conf_files = glob.glob(os.path.join(current_directory, '*china.conf'))
    
    # 新代码：直接指定只处理 accelerated-domains.china.conf 这一个文件
    target_file = os.path.join(current_directory, 'accelerated-domains.china.conf')
    
    # 判断文件是否存在，防止报错
    if os.path.exists(target_file):
        conf_files = [target_file]
    else:
        print("未找到 accelerated-domains.china.conf 文件")
        conf_files = []
    # ================= 修改结束 =================

    # 逐个读取文件内容（此时列表里只有那一个文件）
    for thefile in conf_files:
        if os.path.basename(thefile) == 'bogus-nxdomain.china.conf':
            continue
        txt_file = os.path.join(converted_directory, os.path.basename(thefile) + ".txt")  # 生成的 txt 文件路径
        convert_conf_to_txt(thefile, txt_file, cn_dns)

    # 合并生成的 txt 文件为 FAK-DNS.txt
    # 因为上面只生成了一个 txt，所以这里也只会合并那一个
    txt_files = glob.glob(os.path.join(converted_directory, '*conf.txt'))
    
    with open(os.path.join(converted_directory, 'FAK-DNS.txt'), 'w') as fak_dns:
        # 写入默认的国外 DNS（THE_DNS）作为第一行（如果不需要可以删掉下面这行）
        if the_dns: 
            fak_dns.write(the_dns + "\n")  
            
        for txt_file in txt_files:
            with open(txt_file, 'r') as txt:
                fak_dns.write(txt.read())

# 从环境变量中获取 DNS URL
cn_dns = os.environ.get('CN_DNS')
# 如果没有设置 THE_DNS，这就不会报错
the_dns = os.environ.get('THE_DNS')

if __name__ == "__main__":
    main()
