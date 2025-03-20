def return_function():
    print("开始执行 return 函数")
    print("执行一些操作...")
    return "返回值"
    print("这一行不会执行") # return 之后的代码不会执行

def yield_function():
    print("开始执行 yield 函数")
    print("执行第一部分操作...")
    yield "第一个值"
    print("执行第二部分操作...") # yield 之后的代码会在下次调用时执行
    yield "第二个值"
    print("执行第三部分操作...")
    yield "第三个值"

# 测试 return 函数
print("===== 测试 return 函数 =====")
result = return_function()
print(f"return 函数返回: {result}")
print("尝试再次调用 return 函数")
result = return_function()
print(f"return 函数返回: {result}")

# 测试 yield 函数
print("\n===== 测试 yield 函数 =====")
gen = yield_function()  # 创建生成器对象，此时函数体还未执行
print(f"yield 函数返回的是: {type(gen)}")

# 通过 next() 逐步执行生成器
print("\n执行生成器的第一步:")
print(f"yield 返回: {next(gen)}")

print("\n执行生成器的第二步:")
print(f"yield 返回: {next(gen)}")

print("\n执行生成器的第三步:")
print(f"yield 返回: {next(gen)}")

# 生成器耗尽后再次调用会引发 StopIteration 异常
print("\n生成器已耗尽，再次调用:")
try:
    next(gen)
except StopIteration:
    print("生成器已结束!")
