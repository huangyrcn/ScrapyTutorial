"""
Python异步编程实战示例
展示异步编程的各种应用场景和最佳实践
"""

import asyncio
import time
import random
import aiohttp
import aiofiles
from contextlib import asynccontextmanager
from typing import List, Dict, Any
import sys

# 基础异步操作
async def hello_world():
    """基础异步函数示例
    
    展示最简单的异步操作和非阻塞休眠
    """
    print("开始执行...")
    await asyncio.sleep(1)  # 非阻塞休眠
    print("执行完成!")
    return "Hello World"

# 模拟网络请求
async def fetch_data(url: str, delay: float) -> Dict[str, Any]:
    """模拟异步网络请求
    
    Args:
        url: 请求的URL
        delay: 模拟的网络延迟（秒）
    
    Returns:
        包含响应数据的字典
    """
    print(f"开始请求 {url} (延迟: {delay}秒)")
    await asyncio.sleep(delay)  # 模拟网络延迟
    print(f"完成请求 {url}")
    return {
        "url": url,
        "status": 200,
        "data": f"来自 {url} 的数据"
    }

# 并发请求示例
async def concurrent_requests():
    """并发执行多个网络请求的示例"""
    urls = [
        "http://api1.example.com",
        "http://api2.example.com",
        "http://api3.example.com"
    ]
    delays = [1, 2, 3]
    
    print("开始并发请求...")
    start = time.time()
    
    # 使用gather并发执行多个请求
    tasks = [fetch_data(url, delay) 
             for url, delay in zip(urls, delays)]
    results = await asyncio.gather(*tasks)
    
    print(f"所有请求完成，耗时: {time.time()-start:.2f}秒")
    return results

# 异步上下文管理器
@asynccontextmanager
async def managed_resource():
    """异步资源管理器示例
    
    展示如何正确管理异步资源的获取和释放
    """
    print("获取资源...")
    await asyncio.sleep(0.5)  # 模拟资源获取
    try:
        yield "资源"
    finally:
        print("释放资源...")
        await asyncio.sleep(0.5)  # 模拟资源释放

# 异步文件操作
async def file_operations():
    """异步文件操作示例"""
    # 写入文件
    async with aiofiles.open('test.txt', 'w') as f:
        await f.write('Hello, Async World!\n')
        await f.write('这是第二行\n')
    
    # 读取文件
    async with aiofiles.open('test.txt', 'r') as f:
        content = await f.read()
        print(f"文件内容:\n{content}")

# 异步迭代器
async def async_number_generator():
    """异步数字生成器示例"""
    for i in range(5):
        await asyncio.sleep(0.5)  # 模拟异步操作
        yield i

async def use_async_iterator():
    """使用异步迭代器的示例"""
    print("开始异步迭代...")
    async for number in async_number_generator():
        print(f"获得数字: {number}")

# 错误处理
async def error_handling_demo():
    """异步代码中的错误处理示例"""
    try:
        await asyncio.sleep(1)
        raise ValueError("模拟的错误")
    except ValueError as e:
        print(f"捕获到错误: {e}")
        return "从错误中恢复"

# 超时处理
async def timeout_handling():
    """超时处理示例"""
    try:
        # 设置1.5秒超时
        async with asyncio.timeout(1.5):
            await asyncio.sleep(2)  # 这个操作会超时
    except asyncio.TimeoutError:
        print("操作超时!")
        return "超时后的处理"

# 实际应用场景：并发网络爬虫
async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    """异步获取URL内容"""
    async with session.get(url) as response:
        return await response.text()

async def web_crawler(urls: List[str]):
    """并发网络爬虫示例"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return dict(zip(urls, results))

# 主函数
async def main():
    """运行所有异步示例"""
    print("\n1. 基础异步操作")
    print("-" * 50)
    result = await hello_world()
    print(f"结果: {result}")
    
    print("\n2. 并发请求示例")
    print("-" * 50)
    results = await concurrent_requests()
    print(f"请求结果: {results}")
    
    print("\n3. 异步上下文管理器")
    print("-" * 50)
    async with managed_resource() as resource:
        print(f"使用资源: {resource}")
    
    print("\n4. 异步文件操作")
    print("-" * 50)
    await file_operations()
    
    print("\n5. 异步迭代器")
    print("-" * 50)
    await use_async_iterator()
    
    print("\n6. 错误处理")
    print("-" * 50)
    result = await error_handling_demo()
    print(f"错误处理结果: {result}")
    
    print("\n7. 超时处理")
    print("-" * 50)
    result = await timeout_handling()
    print(f"超时处理结果: {result}")
    
    print("\n8. 网络爬虫示例")
    print("-" * 50)
    urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net"
    ]
    results = await web_crawler(urls)
    print(f"爬虫结果: {results}")

if __name__ == "__main__":
    # 在Windows上需要使用特定的事件循环策略
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
    
    # 运行主函数
    asyncio.run(main())
