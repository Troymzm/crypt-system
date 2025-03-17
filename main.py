import os
from util import SubstitutionCipher

def print_menu():
    """打印菜单"""
    print("*" * 50)
    print("\t单表代换密码辅助工具")
    print("*" * 50)
    print("0: 退出系统")
    print("1: 加密明文")
    print("2: 解密密文")
    print("3: 加载密文进行分析")
    print("4: 显示当前密文")
    print("5: 频率分析")
    print("6: 单词分析")
    print("7: 更新字母映射")
    print("8: 清除字母映射")
    print("9: 显示当前破译结果")
    print("*" * 50)

def load_sample_from_file():
    """从文件加载示例密文"""
    try:
        sample_file_path = os.path.join(os.path.dirname(__file__), 'sample.txt')
        with open(sample_file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("警告: 示例密文文件未找到，使用内置示例。")
        return "hzsrnqc klyy wqc flo mflwf ol zqdn nsoznj wskn lj xzsrbjnf"
    except Exception as e:
        print(f"读取示例文件时出错: {e}，使用内置示例。")
        return "hzsrnqc klyy wqc flo mflwf ol zqdn nsoznj wskn lj xzsrbjnf"

def main():
    """主函数"""
    cipher = SubstitutionCipher()
    loaded_text = ""
    print_menu()
    
    while True:
        choice = input("请选择功能: ").strip()
        
        if choice == '0':
            print("程序结束！")
            break
            
        elif choice == '1':
            plaintext = input("请输入要加密的明文: ").strip()
            key = input("请输入26个小写字母的密钥(按字母表顺序对应): ").strip()
            result = cipher.encrypt(plaintext, key)
            if result:
                print(f"加密结果: {result}")
            
        elif choice == '2':
            ciphertext = input("请输入要解密的密文: ").strip()
            key = input("请输入26个小写字母的密钥(按字母表顺序对应): ").strip()
            result = cipher.decrypt(ciphertext, key)
            if result:
                print(f"解密结果: {result}")
            
        elif choice == '3':
            print("1: 使用示例密文")
            print("2: 输入自定义密文")
            sub_choice = input("请选择: ").strip()
            
            if sub_choice == '1':
                loaded_text = load_sample_from_file()
                cipher.load_ciphertext(loaded_text)
                print("已加载示例密文")
            elif sub_choice == '2':
                loaded_text = input("请输入密文: ").strip()
                cipher.load_ciphertext(loaded_text)
                print("已加载自定义密文")
            
        elif choice == '4':
            if loaded_text:
                print(f"当前密文: {loaded_text}")
            else:
                print("尚未加载密文")
            
        elif choice == '5':
            if not cipher.frequency:
                print("请先加载密文")
                continue
            print("基于频率分析建议:")
            for suggestion in cipher.suggest_mapping():
                print(suggestion)
            
        elif choice == '6':
            if not cipher.words:
                print("请先加载密文")
                continue
                
            print("基于单词分析建议:")
            for suggestion in cipher.suggest_patterns():
                print(suggestion)
                
        elif choice == '7':
            if not loaded_text:
                print("请先加载密文")
                continue
                
            cipher_char = input("请输入密文字母: ").strip().lower()
            if not cipher_char or len(cipher_char) != 1 or not cipher_char.islower():
                print("输入无效")
                continue
                
            plain_char = input("请输入对应明文字母: ").strip().upper()
            if not plain_char or len(plain_char) != 1 or not plain_char.isupper():
                print("输入无效")
                continue
                
            if cipher.update_mapping(cipher_char, plain_char):
                print(f"已更新映射: {cipher_char} -> {plain_char}")
                
        elif choice == '8':
            if not cipher.key_mapping:
                print("尚无映射需要清除")
                continue
                
            cipher_char = input("请输入要清除的密文字母，直接回车清除所有: ").strip().lower()
            if cipher_char:
                if len(cipher_char) != 1 or not cipher_char.islower():
                    print("输入无效")
                    continue
                    
                if cipher_char in cipher.key_mapping:
                    cipher.clear_mapping(cipher_char)
                    print(f"已清除 '{cipher_char}' 的映射")
                else:
                    print(f"'{cipher_char}' 尚无映射")
            else:
                confirm = input("确定要清除所有映射吗? (y/n): ").strip().lower()
                if confirm == 'y':
                    cipher.clear_mapping()
                    print("已清除所有映射")
            
        elif choice == '9':
            if not loaded_text:
                print("请先加载密文")
                continue
                
            print("当前密钥映射:", cipher.get_current_key())
            print("当前破译状态:")
            print(cipher.display_current_state())
        
        input("按回车键继续...")

if __name__ == "__main__":
    main()
