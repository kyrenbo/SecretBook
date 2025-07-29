import json
import hashlib
from pathlib import Path
from datetime import datetime
from .crypto import CryptoManager


class DataManager:
    """数据管理器"""
    
    def __init__(self):
        self.data_dir = Path.home() / '.secretbook'
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / 'users.json'
        self.current_user = None
        self.encryption_key = None
    
    def load_users(self) -> dict:
        """加载用户数据"""
        if self.users_file.exists():
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_users(self, users_data: dict):
        """保存用户数据"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    def register_user(self, username: str, password: str) -> bool:
        """注册用户"""
        users = self.load_users()
        if username in users:
            return False
        
        # 密码哈希
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users[username] = {
            'password_hash': password_hash,
            'created_at': datetime.now().isoformat(),
            'passwords': []
        }
        self.save_users(users)
        return True
    
    def login_user(self, username: str, password: str) -> bool:
        """用户登录"""
        users = self.load_users()
        if username not in users:
            return False
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if users[username]['password_hash'] != password_hash:
            return False
        
        self.current_user = username
        self.encryption_key = CryptoManager.generate_key(username)
        return True
    
    def get_user_passwords(self) -> list:
        """获取当前用户的密码列表"""
        if not self.current_user:
            return []
        
        users = self.load_users()
        encrypted_passwords = users[self.current_user].get('passwords', [])
        
        passwords = []
        for encrypted_item in encrypted_passwords:
            try:
                decrypted_data = CryptoManager.decrypt_data(
                    encrypted_item['data'], self.encryption_key
                )
                password_data = json.loads(decrypted_data)
                password_data['id'] = encrypted_item['id']
                passwords.append(password_data)
            except Exception:
                continue  # 跳过损坏的数据
        
        return passwords
    
    def check_password_exists(self, website: str, username: str, exclude_id: int = None) -> dict:
        """检查密码是否已存在
        
        Args:
            website: 网站/应用名
            username: 用户名
            exclude_id: 排除的密码ID（用于编辑时检查）
        
        Returns:
            {'exists': bool, 'password': dict or None}
        """
        if not self.current_user:
            return {'exists': False, 'password': None}
        
        passwords = self.get_user_passwords()
        
        for password in passwords:
            if (password.get('website', '').lower() == website.lower() and 
                password.get('username', '').lower() == username.lower() and
                (exclude_id is None or password.get('id') != exclude_id)):
                return {'exists': True, 'password': password}
        
        return {'exists': False, 'password': None}
    
    def save_password(self, password_data: dict, force_save: bool = False) -> tuple[bool, str, dict]:
        """保存密码
        
        Args:
            password_data: 密码数据
            force_save: 强制保存（忽略重复检查）
        
        Returns:
            (成功状态, 消息, 重复的密码数据或None)
        """
        if not self.current_user:
            return False, "用户未登录", None
        
        # 检查唯一性（除非强制保存）
        if not force_save:
            check_result = self.check_password_exists(
                password_data.get('website', ''),
                password_data.get('username', '')
            )
            
            if check_result['exists']:
                return False, "密码已存在", check_result['password']
        
        users = self.load_users()
        
        # 加密密码数据
        data_to_encrypt = json.dumps(password_data, ensure_ascii=False)
        encrypted_data = CryptoManager.encrypt_data(data_to_encrypt, self.encryption_key)
        
        # 生成ID
        password_id = len(users[self.current_user]['passwords']) + 1
        
        encrypted_item = {
            'id': password_id,
            'data': encrypted_data,
            'created_at': datetime.now().isoformat()
        }
        
        users[self.current_user]['passwords'].append(encrypted_item)
        self.save_users(users)
        return True, "保存成功", None
    
    def update_password(self, password_id: int, password_data: dict, force_update: bool = False) -> tuple[bool, str, dict]:
        """更新密码
        
        Args:
            password_id: 密码ID
            password_data: 新的密码数据
            force_update: 强制更新（忽略重复检查）
        
        Returns:
            (成功状态, 消息, 重复的密码数据或None)
        """
        if not self.current_user:
            return False, "用户未登录", None
        
        # 检查唯一性（除非强制更新）
        if not force_update:
            check_result = self.check_password_exists(
                password_data.get('website', ''),
                password_data.get('username', ''),
                exclude_id=password_id
            )
            
            if check_result['exists']:
                return False, "密码已存在", check_result['password']
        
        users = self.load_users()
        passwords = users[self.current_user]['passwords']
        
        for i, item in enumerate(passwords):
            if item['id'] == password_id:
                data_to_encrypt = json.dumps(password_data, ensure_ascii=False)
                encrypted_data = CryptoManager.encrypt_data(data_to_encrypt, self.encryption_key)
                
                passwords[i]['data'] = encrypted_data
                passwords[i]['updated_at'] = datetime.now().isoformat()
                break
        
        self.save_users(users)
        return True, "更新成功", None
    
    def import_passwords(self, file_path: str, merge_mode: bool = True) -> tuple[bool, str, list]:
        """从加密文件导入密码
        
        Args:
            file_path: 导入文件路径
            merge_mode: True=合并模式(保留现有密码), False=替换模式(清空现有密码)
        
        Returns:
            (成功状态, 消息, 重复密码列表)
        """
        if not self.current_user:
            return False, "用户未登录", []
        
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            
            # 验证文件格式
            if not isinstance(file_data, dict) or file_data.get('format') != 'SecretBook_Export_v1.0':
                return False, "不是有效的密码导出文件", []
            
            # 解密数据
            try:
                decrypted_json = CryptoManager.decrypt_data(file_data['data'], self.encryption_key)
                import_data = json.loads(decrypted_json)
            except Exception:
                return False, "文件解密失败，可能是密码错误或文件损坏", []
            
            # 验证数据结构
            if not isinstance(import_data, dict) or 'passwords' not in import_data:
                return False, "导入文件数据格式错误", []
            
            passwords_to_import = import_data['passwords']
            if not isinstance(passwords_to_import, list):
                return False, "密码数据格式错误", []
            
            # 获取当前用户数据
            users = self.load_users()
            
            if not merge_mode:
                # 替换模式：清空现有密码
                users[self.current_user]['passwords'] = []
            
            # 检查重复密码
            duplicates = []
            valid_passwords = []
            
            for password_data in passwords_to_import:
                # 移除ID字段，让系统重新分配
                if 'id' in password_data:
                    del password_data['id']
                
                # 验证必要字段
                if not all(key in password_data for key in ['website', 'username', 'password']):
                    continue
                
                # 检查是否重复
                check_result = self.check_password_exists(
                    password_data.get('website', ''),
                    password_data.get('username', '')
                )
                
                if check_result['exists']:
                    duplicates.append({
                        'import_data': password_data,
                        'existing_data': check_result['password']
                    })
                else:
                    valid_passwords.append(password_data)
            
            # 导入非重复密码
            imported_count = 0
            for password_data in valid_passwords:
                success, _, _ = self.save_password(password_data, force_save=True)
                if success:
                    imported_count += 1
            
            if duplicates:
                return True, f"导入完成。成功导入 {imported_count} 条密码，发现 {len(duplicates)} 条重复密码需要处理。", duplicates
            else:
                return True, f"成功导入 {imported_count} 条密码记录", []
            
        except FileNotFoundError:
            return False, "文件不存在", []
        except json.JSONDecodeError:
            return False, "文件格式错误，不是有效的JSON文件", []
        except Exception as e:
            return False, f"导入失败: {str(e)}", []
    
    def delete_password(self, password_id: int) -> bool:
        """删除密码"""
        if not self.current_user:
            return False
        
        users = self.load_users()
        passwords = users[self.current_user]['passwords']
        
        users[self.current_user]['passwords'] = [
            item for item in passwords if item['id'] != password_id
        ]
        
        self.save_users(users)
        return True
    
    def export_passwords(self, file_path: str) -> bool:
        """导出密码到加密文件"""
        if not self.current_user:
            return False
        
        try:
            # 获取所有密码数据
            passwords = self.get_user_passwords()
            
            # 创建导出数据结构
            export_data = {
                'version': '1.0',
                'exported_at': datetime.now().isoformat(),
                'user': self.current_user,
                'passwords': passwords
            }
            
            # 转换为JSON字符串
            json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
            
            # 使用当前用户的加密密钥加密整个数据
            encrypted_data = CryptoManager.encrypt_data(json_data, self.encryption_key)
            
            # 创建最终的导出文件格式
            export_file_data = {
                'format': 'SecretBook_Export_v1.0',
                'data': encrypted_data
            }
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_file_data, f, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False