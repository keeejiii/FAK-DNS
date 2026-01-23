import os
import glob

def convert_conf_to_txt(conf_file, txt_file, cn_dns):
    with open(conf_file, 'r') as conf:
        with open(txt_file, 'w') as txt:
            for line in conf:
                parts = line.strip().split('=')
                if len(parts) != 2:
                    continue
                domain = parts[1].split('/')[1]
                txt.write(f"[/{domain}/]" + cn_dns + "\n")

def main():
    current_directory = os.getcwd()
    converted_directory = os.path.join(current_directory, 'converted')
    os.makedirs(converted_directory, exist_ok=True)

    # 1. 设定只处理 accelerated-domains 这一个源文件
    target_file = os.path.join(current_directory, 'accelerated-domains.china.conf')
    
    if os.path.exists(target_file):
        # 生成对应的 txt 路径
        target_txt_file = os.path.join(converted_directory, 'accelerated-domains.china.conf.txt')
        convert_conf_to_txt(target_file, target_txt_file, cn_dns)
    else:
        print("未找到源文件")
        return

    # 2. 合并阶段：只读取我们刚刚生成的这一个 txt 文件
    # (不再使用 glob 扫描文件夹，从而避开旧的 apple/google 文件)
    
    final_file = os.path.join(converted_directory, 'FAK-DNS.txt')
    
    with open(final_file, 'w') as fak_dns:
        # 写入头部自定义 DNS
        if the_dns: 
            fak_dns.write(the_dns + "\n")
            
        # 写入 accelerated-domains 的内容
        if os.path.exists(target_txt_file):
            with open(target_txt_file, 'r') as txt:
                fak_dns.write(txt.read())

# 从环境变量中获取 DNS URL
cn_dns = os.environ.get('CN_DNS')
the_dns = os.environ.get('THE_DNS')

if __name__ == "__main__":
    main()
