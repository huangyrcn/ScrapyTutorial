# Python中的异步编程详解

## 什么是异步编程？

异步编程是一种编程范式，允许程序在等待某些操作完成（如I/O操作）时继续执行其他代码，而不是被阻塞。Python通过`async`和`await`关键字支持异步编程，使用`asyncio`库来管理异步任务。

## 同步vs异步：基本区别

| 同步编程 | 异步编程 |
|--------|-------|
| 按顺序执行代码，一次一个任务 | 可以并发执行多个任务 |
| 当遇到I/O操作时会被阻塞 | 在I/O操作时可以切换到其他任务 |
| 代码结构直观，易于理解 | 需要特殊的关键字和控制流 |
| 适合CPU密集型任务 | 适合I/O密集型任务 |

## 核心概念

### 协程 (Coroutines)

协程是使用`async def`定义的函数，它们可以在执行过程中暂停并稍后恢复：

```python
async def my_coroutine():
    # 这是一个协程函数
    await asyncio.sleep(1)
    return "结果"
```

### await 关键字

`await`用于等待一个协程的结果，同时将控制权让出给事件循环：

```python
result = await some_coroutine()
```

### 事件循环 (Event Loop)

事件循环是异步编程的核心，它负责调度和执行协程：

```python
asyncio.run(main())  # 创建事件循环并运行main协程
```

### Tasks

任务是对协程的封装，允许它们被调度执行：

```python
task = asyncio.create_task(some_coroutine())
await task  # 等待任务完成
```

## 常见使用模式

### 并发执行多个协程

```python
async def main():
    results = await asyncio.gather(
        coroutine1(),
        coroutine2(),
        coroutine3()
    )
```

### 超时处理

```python
try:
    result = await asyncio.wait_for(slow_operation(), timeout=1.5)
except asyncio.TimeoutError:
    print("操作超时")
```

### 异步上下文管理器

```python
async with async_resource() as resource:
    await resource.use()
```

### 异步生成器

与普通生成器类似，但使用`async`和`await`：

```python
async def async_generator():
    for i in range(5):
        await asyncio.sleep(1)
        yield i
```

## 与其他并发模型的比较

| 特性 | 线程 | 进程 | 异步 |
|-----|-----|-----|-----|
| CPU利用 | 一个核内分时 | 可利用多核 | 主要单核 |
| 内存开销 | 中等 | 大 | 小 |
| 上下文切换成本 | 中等 | 高 | 低 |
| 并行执行 | 支持 | 支持 | 仅并发不并行 |
| 状态共享 | 简单但需加锁 | 复杂 | 简单 |

