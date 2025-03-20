"""
演示Python生成器在内存使用方面的优势
包含多个实际场景的对比测试
"""

import sys
import time
import psutil
import os

def get_process_memory():
    """获取当前进程的内存使用情况"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

def memory_usage_decorator(func):
    """装饰器：测量函数执行期间的内存使用"""
    def wrapper(*args, **kwargs):
        memory_before = get_process_memory()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        memory_after = get_process_memory()
        
        print(f"\n{func.__name__} 性能指标:")
        print(f"内存使用: {(memory_after - memory_before) / 1024 / 1024:.2f} MB")
        print(f"执行时间: {end_time - start_time:.2f} 秒")
        return result
    return wrapper

@memory_usage_decorator
def return_large_list(n):
    """使用return返回大列表的函数
    
    一次性在内存中创建包含n个元素的列表
    """
    result = []
    for i in range(n):
        result.append(i)
    return result

@memory_usage_decorator
def yield_large_list(n):
    """使用yield生成大列表的函数
    
    逐个生成元素，不占用大量内存
    """
    for i in range(n):
        yield i

class MemoryTest:
    """内存使用测试类"""
    
    def __init__(self, size):
        self.size = size
    
    @memory_usage_decorator
    def test_list_comprehension(self):
        """测试列表推导式的内存使用"""
        return [i * i for i in range(self.size)]
    
    @memory_usage_decorator
    def test_generator_expression(self):
        """测试生成器表达式的内存使用"""
        return (i * i for i in range(self.size))
    
    @memory_usage_decorator
    def test_file_reading_with_list(self, filename):
        """测试使用列表读取文件的内存使用"""
        with open(filename, 'w') as f:
            for i in range(self.size):
                f.write(f"Line {i}\n")
        
        with open(filename, 'r') as f:
            return [line for line in f]
    
    @memory_usage_decorator
    def test_file_reading_with_generator(self, filename):
        """测试使用生成器读取文件的内存使用"""
        with open(filename, 'r') as f:
            for line in f:
                yield line

def main():
    # 测试参数
    n = 10**6  # 百万级元素
    test_file = "test_data.txt"
    
    print("=== 内存使用对比测试 ===")
    
    # 1. 基本列表生成对比
    print("\n1. 基本列表生成测试")
    print("-" * 50)
    return_list = return_large_list(n)
    gen = yield_large_list(n)
    # 消耗生成器以便进行公平比较
    list(gen)
    
    # 2. 列表推导式vs生成器表达式
    print("\n2. 列表推导式 vs 生成器表达式")
    print("-" * 50)
    memory_test = MemoryTest(n)
    list_comp = memory_test.test_list_comprehension()
    gen_exp = memory_test.test_generator_expression()
    # 消耗生成器表达式
    list(gen_exp)
    
    # 3. 文件读取测试
    print("\n3. 文件读取测试")
    print("-" * 50)
    list_reading = memory_test.test_file_reading_with_list(test_file)
    gen_reading = memory_test.test_file_reading_with_generator(test_file)
    # 消耗生成器
    list(gen_reading)
    
    # 清理测试文件
    try:
        os.remove(test_file)
    except:
        pass

if __name__ == "__main__":
    main()
