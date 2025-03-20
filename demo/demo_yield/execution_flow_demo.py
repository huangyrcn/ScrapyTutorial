"""
演示Python中yield和return的执行流程差异
此示例展示了生成器函数和普通函数在执行过程中的根本区别
"""

def calculate_with_return():
    """使用return的普通函数示例
    
    特点：
    1. 一次性计算所有结果
    2. 函数执行完毕后立即返回
    3. return后的代码不会执行
    """
    print("\n=== Return函数执行开始 ===")
    result = 0
    for i in range(1, 6):
        print(f"[Return] 步骤 {i}: 当前result = {result}")
        result += i
    print("[Return] 计算完成，即将返回最终结果")
    return result
    print("这行代码永远不会执行")  # 不可达代码

def calculate_with_yield():
    """使用yield的生成器函数示例
    
    特点：
    1. 逐步计算并产生结果
    2. 每次yield后函数暂停执行
    3. 下次调用时从暂停处继续
    4. 可以多次产生值
    """
    print("\n=== Yield函数执行开始 ===")
    result = 0
    for i in range(1, 6):
        result += i
        print(f"[Yield] 步骤 {i}: 当前result = {result}")
        print(f"[Yield] 暂停执行，产生中间结果: {result}")
        yield result
        print(f"[Yield] 继续执行步骤 {i} 之后的代码")
    print("[Yield] 生成器执行完毕")

def demonstrate_yield_send():
    """演示yield的send功能
    
    展示如何向生成器发送值并获取响应
    """
    print("\n=== Yield Send示例开始 ===")
    current = 0
    while True:
        print(f"[Yield-Send] 当前值: {current}")
        try:
            received = yield current
            if received is None:
                current += 1
            else:
                print(f"[Yield-Send] 收到外部值: {received}")
                current = received
        except GeneratorExit:
            print("[Yield-Send] 生成器被关闭")
            break

def main():
    # 演示return函数
    print("\n1. Return函数演示")
    print("-" * 50)
    result = calculate_with_return()
    print(f"Return函数返回值: {result}")
    
    # 演示yield函数
    print("\n2. Yield函数演示")
    print("-" * 50)
    generator = calculate_with_yield()
    print("创建生成器对象，函数体尚未执行")
    
    print("\n逐步获取生成器的值:")
    try:
        while True:
            value = next(generator)
            print(f"获得生成器的值: {value}")
    except StopIteration:
        print("生成器执行完毕")
    
    # 演示yield send功能
    print("\n3. Yield Send演示")
    print("-" * 50)
    gen = demonstrate_yield_send()
    next(gen)  # 启动生成器
    
    print("\n向生成器发送值:")
    gen.send(10)  # 发送值10
    next(gen)     # 继续执行
    gen.send(20)  # 发送值20
    gen.close()   # 关闭生成器

if __name__ == "__main__":
    main()
