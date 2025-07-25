"""
搜索服务模块
实现百度搜索API功能
"""

import requests
import json
import re
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
import logging
from django.conf import settings
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class MockSearchService:
    """模拟搜索服务，用于演示功能"""

    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """模拟搜索功能"""
        # 根据查询关键词生成模拟结果
        mock_results = []

        # 技术相关关键词
        tech_keywords = {
            "python": [
                {
                    "title": "Python官方教程 - 官方文档",
                    "url": "https://docs.python.org/zh-cn/3/tutorial/",
                    "abstract": "Python官方教程，包含Python基础语法、数据结构、模块等完整学习指南。",
                },
                {
                    "title": "Python入门教程 - 菜鸟教程",
                    "url": "https://www.runoob.com/python3/python3-tutorial.html",
                    "abstract": "Python3教程，从基础语法到高级特性，适合初学者学习。",
                },
                {
                    "title": "Python学习笔记 - 廖雪峰",
                    "url": "https://www.liaoxuefeng.com/wiki/1016959663602400",
                    "abstract": "廖雪峰的Python教程，深入浅出地讲解Python编程。",
                },
            ],
            "django": [
                {
                    "title": "Django官方文档",
                    "url": "https://docs.djangoproject.com/zh-hans/4.2/",
                    "abstract": "Django官方文档，包含完整的Web开发框架指南。",
                },
                {
                    "title": "Django教程 - 菜鸟教程",
                    "url": "https://www.runoob.com/django/django-tutorial.html",
                    "abstract": "Django Web框架教程，从安装到部署的完整指南。",
                },
            ],
            "javascript": [
                {
                    "title": "JavaScript教程 - MDN",
                    "url": "https://developer.mozilla.org/zh-CN/docs/Web/JavaScript",
                    "abstract": "MDN JavaScript教程，权威的JavaScript学习资源。",
                },
                {
                    "title": "JavaScript基础教程",
                    "url": "https://www.w3school.com.cn/js/",
                    "abstract": "W3School JavaScript教程，适合初学者的基础教程。",
                },
            ],
            "html": [
                {
                    "title": "HTML教程 - MDN",
                    "url": "https://developer.mozilla.org/zh-CN/docs/Web/HTML",
                    "abstract": "MDN HTML教程，学习HTML标记语言的基础知识。",
                },
                {
                    "title": "HTML5教程",
                    "url": "https://www.w3school.com.cn/html5/",
                    "abstract": "W3School HTML5教程，现代Web开发必备技能。",
                },
            ],
            "css": [
                {
                    "title": "CSS教程 - MDN",
                    "url": "https://developer.mozilla.org/zh-CN/docs/Web/CSS",
                    "abstract": "MDN CSS教程，学习网页样式设计。",
                },
                {
                    "title": "CSS3教程",
                    "url": "https://www.w3school.com.cn/css3/",
                    "abstract": "W3School CSS3教程，现代CSS技术指南。",
                },
            ],
            "sql": [
                {
                    "title": "SQL教程 - W3School",
                    "url": "https://www.w3school.com.cn/sql/",
                    "abstract": "W3School SQL教程，数据库查询语言学习指南。",
                },
                {
                    "title": "MySQL教程",
                    "url": "https://www.runoob.com/mysql/mysql-tutorial.html",
                    "abstract": "MySQL数据库教程，从基础到高级的完整指南。",
                },
            ],
            "git": [
                {
                    "title": "Git教程 - 廖雪峰",
                    "url": "https://www.liaoxuefeng.com/wiki/896043488029600",
                    "abstract": "廖雪峰的Git教程，深入浅出地讲解版本控制。",
                },
                {
                    "title": "Git官方文档",
                    "url": "https://git-scm.com/doc",
                    "abstract": "Git官方文档，最权威的Git使用指南。",
                },
            ],
            "docker": [
                {
                    "title": "Docker官方文档",
                    "url": "https://docs.docker.com/",
                    "abstract": "Docker官方文档，容器化技术学习指南。",
                },
                {
                    "title": "Docker教程",
                    "url": "https://www.runoob.com/docker/docker-tutorial.html",
                    "abstract": "Docker容器教程，从入门到实践的完整指南。",
                },
            ],
        }

        # 通用教程
        general_tutorials = [
            {
                "title": f"{query} 入门教程",
                "url": f"https://example.com/tutorial/{query.lower()}",
                "abstract": f"{query}入门教程，适合初学者学习。",
            },
            {
                "title": f"{query} 官方文档",
                "url": f"https://docs.example.com/{query.lower()}",
                "abstract": f"{query}官方文档，包含完整的API参考和使用指南。",
            },
            {
                "title": f"{query} 学习指南",
                "url": f"https://learn.example.com/{query.lower()}",
                "abstract": f"{query}学习指南，从基础到高级的完整学习路径。",
            },
        ]

        # 查找匹配的关键词
        query_lower = query.lower()
        for keyword, results in tech_keywords.items():
            if keyword in query_lower:
                mock_results.extend(results)
                break

        # 如果没有找到匹配的关键词，使用通用教程
        if not mock_results:
            mock_results = general_tutorials

        # 添加来源信息
        for result in mock_results:
            result["source"] = "mock"

        return mock_results[:num_results]

    def get_suggestions(self, query: str) -> List[str]:
        """获取搜索建议"""
        suggestions = {
            "python": [
                "python教程",
                "python安装",
                "python基础",
                "python进阶",
                "python实战",
            ],
            "django": [
                "django教程",
                "django安装",
                "django模型",
                "django视图",
                "django模板",
            ],
            "javascript": [
                "javascript教程",
                "javascript基础",
                "javascript进阶",
                "javascript实战",
            ],
            "html": ["html教程", "html基础", "html5教程", "html标签", "html表单"],
            "css": ["css教程", "css基础", "css3教程", "css布局", "css动画"],
            "sql": ["sql教程", "sql基础", "mysql教程", "sql查询", "sql优化"],
            "git": ["git教程", "git基础", "git命令", "git分支", "git合并"],
            "docker": [
                "docker教程",
                "docker基础",
                "docker安装",
                "docker镜像",
                "docker容器",
            ],
        }

        query_lower = query.lower()
        for keyword, suggestion_list in suggestions.items():
            if keyword in query_lower:
                return suggestion_list

        return [f"{query}教程", f"{query}基础", f"{query}入门", f"{query}实战"]


class BaiduSearchService:
    """百度搜索服务类"""

    def __init__(self):
        self.base_url = "https://www.baidu.com/s"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",  # 不接受br压缩
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        执行百度搜索

        Args:
            query: 搜索关键词
            num_results: 返回结果数量

        Returns:
            搜索结果列表
        """
        try:
            # 构建搜索参数
            params = {
                "wd": query,
                "rn": num_results,
                "ie": "utf-8",
                "tn": "baiduhome_pg",
                "rsv_idx": "2",
                "rsv_crq": "1",
                "rsv_enter": "1",
            }

            # 发送请求
            response = self.session.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            response.encoding = "utf-8"

            logger.info(f"百度搜索请求成功: {query}")

            # 解析搜索结果
            return self._parse_search_results(response.text, query)

        except requests.RequestException as e:
            logger.error(f"百度搜索请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"百度搜索解析失败: {e}")
            return []

    def _parse_search_results(self, html_content: str, query: str) -> List[Dict]:
        """
        解析百度搜索结果HTML

        Args:
            html_content: HTML内容
            query: 原始搜索关键词

        Returns:
            解析后的搜索结果列表
        """
        results = []

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # 方法1: 查找标准搜索结果容器
            result_containers = soup.find_all("div", class_="result")
            if result_containers:
                logger.info(f"找到 {len(result_containers)} 个标准搜索结果")
                for container in result_containers[:10]:
                    result = self._extract_result_info(container, query)
                    if result:
                        results.append(result)

            # 方法2: 查找新的搜索结果结构
            if not results:
                logger.info("尝试新结构解析方法")
                results = self._parse_new_structure_results(soup, query)

            # 方法3: 如果没有找到标准结果，尝试其他选择器
            if not results:
                logger.info("尝试备用解析方法")
                results = self._parse_alternative_results(soup, query)

            # 方法4: 如果还是没有结果，尝试更宽松的解析
            if not results:
                logger.info("尝试宽松解析方法")
                results = self._parse_loose_results(soup, query)

        except Exception as e:
            logger.error(f"解析搜索结果失败: {e}")

        logger.info(f"最终解析到 {len(results)} 个搜索结果")
        return results

    def _parse_new_structure_results(self, soup, query: str) -> List[Dict]:
        """
        解析新的百度搜索结果结构

        Args:
            soup: BeautifulSoup对象
            query: 搜索关键词

        Returns:
            解析结果列表
        """
        results = []

        try:
            # 查找所有可能的搜索结果容器
            # 百度搜索结果可能有多种class名称
            possible_selectors = [
                'div[class*="result"]',
                'div[class*="c-container"]',
                'div[class*="result-op"]',
                'div[class*="c-result"]',
                'div[class*="result-item"]',
                'div[class*="search-result"]',
            ]

            for selector in possible_selectors:
                containers = soup.select(selector)
                if containers:
                    logger.info(f"使用选择器 {selector} 找到 {len(containers)} 个结果")
                    for container in containers[:15]:
                        result = self._extract_from_container(container, query)
                        if result:
                            results.append(result)
                            if len(results) >= 10:
                                break
                    if results:
                        break

            # 如果没有找到，尝试查找所有包含链接的div
            if not results:
                logger.info("尝试查找所有包含链接的div")
                all_divs = soup.find_all("div")
                for div in all_divs[:50]:  # 限制搜索范围
                    links = div.find_all("a", href=True)
                    for link in links:
                        href = link.get("href", "")
                        title = link.get_text(strip=True)

                        # 过滤条件
                        if (
                            href.startswith("http")
                            and len(title) > 10
                            and len(title) < 200
                            and not self._is_inappropriate_site(href)
                            and not href.startswith("https://www.baidu.com")
                            and not href.startswith("https://baidu.com")
                            and "baidu" not in href.lower()
                        ):

                            # 查找摘要
                            abstract_elem = div.find(
                                ["div", "p", "span"],
                                class_=re.compile(r"abstract|summary|desc|content"),
                            )
                            abstract = (
                                abstract_elem.get_text(strip=True)
                                if abstract_elem
                                else f"关于 {query} 的相关信息"
                            )

                            results.append(
                                {
                                    "title": title,
                                    "url": href,
                                    "abstract": (
                                        abstract[:200] + "..."
                                        if len(abstract) > 200
                                        else abstract
                                    ),
                                    "source": "baidu",
                                }
                            )

                            if len(results) >= 10:
                                break

                    if len(results) >= 10:
                        break

        except Exception as e:
            logger.error(f"新结构解析方法失败: {e}")

        return results

    def _extract_from_container(self, container, query: str) -> Optional[Dict]:
        """
        从容器中提取搜索结果信息

        Args:
            container: 搜索结果容器
            query: 搜索关键词

        Returns:
            提取的结果信息
        """
        try:
            # 查找标题和链接
            title_selectors = [
                "h3 a",
                "h2 a",
                "h1 a",
                'a[class*="title"]',
                'a[class*="link"]',
            ]
            title_link = None

            for selector in title_selectors:
                title_link = container.select_one(selector)
                if title_link:
                    break

            if not title_link:
                return None

            title = title_link.get_text(strip=True)
            url = title_link.get("href", "")

            # 验证URL
            if not url or not url.startswith("http"):
                return None

            # 过滤不合适的网站
            if self._is_inappropriate_site(url):
                return None

            # 查找摘要
            abstract_selectors = [
                'div[class*="abstract"]',
                'div[class*="summary"]',
                'div[class*="desc"]',
                'div[class*="content"]',
                'p[class*="abstract"]',
                'p[class*="summary"]',
                'span[class*="abstract"]',
                'span[class*="summary"]',
            ]

            abstract = f"关于 {query} 的相关信息"
            for selector in abstract_selectors:
                abstract_elem = container.select_one(selector)
                if abstract_elem:
                    abstract = abstract_elem.get_text(strip=True)
                    break

            return {
                "title": title,
                "url": url,
                "abstract": abstract[:200] + "..." if len(abstract) > 200 else abstract,
                "source": "baidu",
            }

        except Exception as e:
            logger.error(f"从容器提取信息失败: {e}")
            return None

    def _extract_result_info(self, container, query: str) -> Optional[Dict]:
        """
        从搜索结果容器中提取信息

        Args:
            container: 搜索结果容器
            query: 搜索关键词

        Returns:
            提取的结果信息
        """
        try:
            # 查找标题和链接
            title_element = container.find("h3")
            if not title_element:
                return None

            title_link = title_element.find("a")
            if not title_link:
                return None

            title = title_link.get_text(strip=True)
            url = title_link.get("href", "")

            # 查找摘要
            abstract_element = container.find("div", class_="c-abstract")
            if abstract_element:
                abstract = abstract_element.get_text(strip=True)
            else:
                abstract = f"关于 {query} 的相关信息"

            # 验证URL
            if not url or not url.startswith("http"):
                return None

            # 过滤掉一些不合适的网站
            if self._is_inappropriate_site(url):
                return None

            return {"title": title, "url": url, "abstract": abstract, "source": "baidu"}

        except Exception as e:
            logger.error(f"提取结果信息失败: {e}")
            return None

    def _parse_alternative_results(self, soup, query: str) -> List[Dict]:
        """
        使用备用方法解析搜索结果

        Args:
            soup: BeautifulSoup对象
            query: 搜索关键词

        Returns:
            解析结果列表
        """
        results = []

        try:
            # 查找所有可能的搜索结果容器
            containers = soup.find_all(
                ["div", "li"], class_=re.compile(r"result|item|list-item")
            )

            for container in containers[:20]:
                # 查找链接
                link = container.find("a", href=True)
                if not link:
                    continue

                href = link.get("href", "")
                title = link.get_text(strip=True)

                # 过滤有效链接
                if (
                    href.startswith("http")
                    and len(title) > 5
                    and not self._is_inappropriate_site(href)
                    and not href.startswith("https://www.baidu.com")
                ):

                    # 查找摘要
                    abstract_elem = container.find(
                        ["div", "p"], class_=re.compile(r"abstract|summary|desc")
                    )
                    abstract = (
                        abstract_elem.get_text(strip=True)
                        if abstract_elem
                        else f"关于 {query} 的相关信息"
                    )

                    results.append(
                        {
                            "title": title,
                            "url": href,
                            "abstract": abstract,
                            "source": "baidu",
                        }
                    )

                    if len(results) >= 10:
                        break

        except Exception as e:
            logger.error(f"备用解析方法失败: {e}")

        return results

    def _parse_loose_results(self, soup, query: str) -> List[Dict]:
        """
        使用宽松方法解析搜索结果

        Args:
            soup: BeautifulSoup对象
            query: 搜索关键词

        Returns:
            解析结果列表
        """
        results = []

        try:
            # 查找所有外部链接
            links = soup.find_all("a", href=True)

            for link in links:
                href = link.get("href", "")
                title = link.get_text(strip=True)

                # 过滤条件
                if (
                    href.startswith("http")
                    and len(title) > 10
                    and len(title) < 200
                    and not self._is_inappropriate_site(href)
                    and not href.startswith("https://www.baidu.com")
                    and not href.startswith("https://baidu.com")
                    and "baidu" not in href.lower()
                ):

                    # 检查标题是否包含查询关键词
                    if query.lower() in title.lower():
                        results.append(
                            {
                                "title": title,
                                "url": href,
                                "abstract": f"关于 {query} 的相关信息",
                                "source": "baidu",
                            }
                        )

                        if len(results) >= 10:
                            break

        except Exception as e:
            logger.error(f"宽松解析方法失败: {e}")

        return results

    def _is_inappropriate_site(self, url: str) -> bool:
        """
        检查是否为不合适的网站

        Args:
            url: 网站URL

        Returns:
            是否为不合适的网站
        """
        inappropriate_domains = [
            "baidu.com",
            "google.com",
            "youtube.com",
            "facebook.com",
            "twitter.com",
            "instagram.com",
            "tiktok.com",
            "douyin.com",
            "weibo.com",
            "zhihu.com",
            "qq.com",
            "wechat.com",
            "taobao.com",
            "tmall.com",
            "jd.com",
            "amazon.com",
            "ebay.com",
            "sina.com",
            "sohu.com",
            "163.com",
            "126.com",
            "mail.qq.com",
            "mail.163.com",
        ]

        url_lower = url.lower()
        return any(domain in url_lower for domain in inappropriate_domains)

    def get_suggestions(self, query: str) -> List[str]:
        """
        获取搜索建议

        Args:
            query: 搜索关键词

        Returns:
            搜索建议列表
        """
        try:
            suggest_url = "https://www.baidu.com/sugrec"
            params = {"prod": "pc", "wd": query, "cb": "callback"}

            response = self.session.get(suggest_url, params=params, timeout=5)
            response.raise_for_status()

            # 解析JSONP响应
            content = response.text
            match = re.search(r"callback\((.*)\)", content)

            if match:
                data = json.loads(match.group(1))
                suggestions = data.get("g", [])
                return [item.get("q", "") for item in suggestions if item.get("q")]

        except Exception as e:
            logger.error(f"获取搜索建议失败: {e}")

        return []


class PublicSearchService:
    """使用公开搜索API的服务"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        使用DuckDuckGo搜索（无需API密钥）

        Args:
            query: 搜索关键词
            num_results: 返回结果数量

        Returns:
            搜索结果列表
        """
        try:
            # 使用DuckDuckGo搜索
            search_url = "https://html.duckduckgo.com/html/"
            params = {
                "q": query,
                "kl": "cn-zh",  # 中文结果
            }

            response = self.session.get(search_url, params=params, timeout=15)
            response.raise_for_status()
            response.encoding = "utf-8"

            logger.info(f"DuckDuckGo搜索请求成功: {query}")

            # 解析搜索结果
            return self._parse_duckduckgo_results(response.text, query)

        except requests.RequestException as e:
            logger.error(f"DuckDuckGo搜索请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"DuckDuckGo搜索解析失败: {e}")
            return []

    def _parse_duckduckgo_results(self, html_content: str, query: str) -> List[Dict]:
        """
        解析DuckDuckGo搜索结果

        Args:
            html_content: HTML内容
            query: 搜索关键词

        Returns:
            解析后的搜索结果列表
        """
        results = []

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # 查找搜索结果
            result_containers = soup.find_all("div", class_="result")

            for container in result_containers[:10]:
                result = self._extract_duckduckgo_result(container, query)
                if result:
                    results.append(result)

            logger.info(f"解析到 {len(results)} 个搜索结果")

        except Exception as e:
            logger.error(f"解析DuckDuckGo搜索结果失败: {e}")

        return results

    def _extract_duckduckgo_result(self, container, query: str) -> Optional[Dict]:
        """
        从DuckDuckGo结果容器中提取信息

        Args:
            container: 搜索结果容器
            query: 搜索关键词

        Returns:
            提取的结果信息
        """
        try:
            # 查找标题和链接
            title_elem = container.find("a", class_="result__a")
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            url = title_elem.get("href", "")

            # 验证URL
            if not url or not url.startswith("http"):
                return None

            # 过滤不合适的网站
            if self._is_inappropriate_site(url):
                return None

            # 查找摘要
            abstract_elem = container.find("a", class_="result__snippet")
            abstract = (
                abstract_elem.get_text(strip=True)
                if abstract_elem
                else f"关于 {query} 的相关信息"
            )

            return {
                "title": title,
                "url": url,
                "abstract": abstract[:200] + "..." if len(abstract) > 200 else abstract,
                "source": "duckduckgo",
            }

        except Exception as e:
            logger.error(f"提取DuckDuckGo结果信息失败: {e}")
            return None

    def _is_inappropriate_site(self, url: str) -> bool:
        """
        检查是否为不合适的网站

        Args:
            url: 网站URL

        Returns:
            是否为不合适的网站
        """
        inappropriate_domains = [
            "duckduckgo.com",
            "google.com",
            "youtube.com",
            "facebook.com",
            "twitter.com",
            "instagram.com",
            "tiktok.com",
            "douyin.com",
            "weibo.com",
            "qq.com",
            "wechat.com",
            "taobao.com",
            "tmall.com",
            "jd.com",
            "amazon.com",
            "ebay.com",
            "sina.com",
            "sohu.com",
            "163.com",
            "126.com",
            "mail.qq.com",
            "mail.163.com",
        ]

        url_lower = url.lower()
        return any(domain in url_lower for domain in inappropriate_domains)

    def get_suggestions(self, query: str) -> List[str]:
        """
        获取搜索建议（使用DuckDuckGo建议API）

        Args:
            query: 搜索关键词

        Returns:
            搜索建议列表
        """
        try:
            suggest_url = "https://duckduckgo.com/ac/"
            params = {"q": query, "kl": "cn-zh", "callback": "callback"}

            response = self.session.get(suggest_url, params=params, timeout=5)
            response.raise_for_status()

            # 解析JSONP响应
            content = response.text
            match = re.search(r"callback\((.*)\)", content)

            if match:
                data = json.loads(match.group(1))
                suggestions = []
                for item in data:
                    if "phrase" in item:
                        suggestions.append(item["phrase"])
                return suggestions[:5]  # 限制建议数量

        except Exception as e:
            logger.error(f"获取DuckDuckGo搜索建议失败: {e}")

        return []


class SimpleSearchService:
    """简单的搜索服务，使用必应搜索"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        使用必应搜索

        Args:
            query: 搜索关键词
            num_results: 返回结果数量

        Returns:
            搜索结果列表
        """
        try:
            # 使用必应搜索
            search_url = "https://cn.bing.com/search"
            params = {
                "q": query,
                "ensearch": "0",  # 中文搜索
            }

            response = self.session.get(search_url, params=params, timeout=15)
            response.raise_for_status()
            response.encoding = "utf-8"

            logger.info(f"必应搜索请求成功: {query}")

            # 解析搜索结果
            return self._parse_bing_results(response.text, query, num_results)

        except requests.RequestException as e:
            logger.error(f"必应搜索请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"必应搜索解析失败: {e}")
            return []

    def _parse_bing_results(
        self, html_content: str, query: str, num_results: int
    ) -> List[Dict]:
        """
        解析必应搜索结果

        Args:
            html_content: HTML内容
            query: 搜索关键词
            num_results: 结果数量

        Returns:
            解析后的搜索结果列表
        """
        results = []

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # 查找搜索结果
            result_containers = soup.find_all("li", class_="b_algo")

            for container in result_containers[:num_results]:
                result = self._extract_bing_result(container, query)
                if result:
                    results.append(result)

            logger.info(f"解析到 {len(results)} 个搜索结果")

        except Exception as e:
            logger.error(f"解析必应搜索结果失败: {e}")

        return results

    def _extract_bing_result(self, container, query: str) -> Optional[Dict]:
        """
        从必应结果容器中提取信息

        Args:
            container: 搜索结果容器
            query: 搜索关键词

        Returns:
            提取的结果信息
        """
        try:
            # 查找标题和链接
            title_elem = container.find("h2")
            if not title_elem:
                return None

            title_link = title_elem.find("a")
            if not title_link:
                return None

            title = title_link.get_text(strip=True)
            url = title_link.get("href", "")

            # 验证URL
            if not url or not url.startswith("http"):
                return None

            # 过滤不合适的网站
            if self._is_inappropriate_site(url):
                return None

            # 查找摘要
            abstract_elem = container.find("p")
            abstract = (
                abstract_elem.get_text(strip=True)
                if abstract_elem
                else f"关于 {query} 的相关信息"
            )

            return {
                "title": title,
                "url": url,
                "abstract": abstract[:200] + "..." if len(abstract) > 200 else abstract,
                "source": "bing",
            }

        except Exception as e:
            logger.error(f"提取必应结果信息失败: {e}")
            return None

    def _is_inappropriate_site(self, url: str) -> bool:
        """
        检查是否为不合适的网站

        Args:
            url: 网站URL

        Returns:
            是否为不合适的网站
        """
        inappropriate_domains = [
            "bing.com",
            "google.com",
            "youtube.com",
            "facebook.com",
            "twitter.com",
            "instagram.com",
            "tiktok.com",
            "douyin.com",
            "weibo.com",
            "qq.com",
            "wechat.com",
            "taobao.com",
            "tmall.com",
            "jd.com",
            "amazon.com",
            "ebay.com",
            "sina.com",
            "sohu.com",
            "163.com",
            "126.com",
            "mail.qq.com",
            "mail.163.com",
        ]

        url_lower = url.lower()
        return any(domain in url_lower for domain in inappropriate_domains)

    def get_suggestions(self, query: str) -> List[str]:
        """
        获取搜索建议

        Args:
            query: 搜索关键词

        Returns:
            搜索建议列表
        """
        try:
            suggest_url = "https://cn.bing.com/AS/Suggestions"
            params = {
                "qry": query,
                "cvid": "1",
                "IG": "1",
                "IID": "1",
                "type": "cb",
            }

            response = self.session.get(suggest_url, params=params, timeout=5)
            response.raise_for_status()

            # 解析JSON响应
            data = response.json()
            suggestions = []

            if "Suggests" in data:
                for item in data["Suggests"]:
                    if "Txt" in item:
                        suggestions.append(item["Txt"])

            return suggestions[:5]  # 限制建议数量

        except Exception as e:
            logger.error(f"获取必应搜索建议失败: {e}")

        return []


class SearchService:
    """搜索服务主类"""

    def __init__(self, use_mock=False, use_simple_search=False):
        if use_mock:
            self.search_engine = MockSearchService()
        elif use_simple_search:
            self.search_engine = SimpleSearchService()
        else:
            self.search_engine = BaiduSearchService()

    def search_pages(
        self, query: str, category_name: str = "", num_results: int = 10
    ) -> List[Dict]:
        """
        搜索相关页面

        Args:
            query: 搜索关键词
            category_name: 分类名称（用于优化搜索）
            num_results: 返回结果数量

        Returns:
            搜索结果列表
        """
        # 优化搜索关键词
        optimized_query = self._optimize_query(query, category_name)

        # 执行搜索
        results = self.search_engine.search(optimized_query, num_results)

        # 过滤和排序结果
        filtered_results = self._filter_results(results, query, category_name)

        return filtered_results[:num_results]

    def _optimize_query(self, query: str, category_name: str) -> str:
        """
        优化搜索关键词

        Args:
            query: 原始查询
            category_name: 分类名称

        Returns:
            优化后的查询
        """
        # 添加分类相关关键词
        if category_name:
            # 根据分类名称添加相关关键词
            category_keywords = {
                "python": "python 教程 文档 学习",
                "java": "java 教程 文档 学习",
                "javascript": "javascript 教程 文档 学习",
                "html": "html 教程 文档 学习",
                "css": "css 教程 文档 学习",
                "sql": "sql 教程 文档 学习",
                "linux": "linux 教程 文档 学习",
                "git": "git 教程 文档 学习",
                "docker": "docker 教程 文档 学习",
                "kubernetes": "kubernetes 教程 文档 学习",
            }

            for key, keywords in category_keywords.items():
                if key.lower() in category_name.lower():
                    return f"{query} {keywords}"

        # 默认添加一些通用关键词
        return f"{query} 教程 文档 学习 指南"

    def _filter_results(
        self, results: List[Dict], query: str, category_name: str
    ) -> List[Dict]:
        """
        过滤和排序搜索结果

        Args:
            results: 原始搜索结果
            query: 搜索关键词
            category_name: 分类名称

        Returns:
            过滤后的结果
        """
        filtered_results = []

        for result in results:
            # 检查标题相关性
            title = result.get("title", "").lower()
            query_lower = query.lower()
            category_lower = category_name.lower()

            # 计算相关性分数
            relevance_score = 0

            # 标题包含查询关键词
            if query_lower in title:
                relevance_score += 3

            # 标题包含分类关键词
            if category_lower in title:
                relevance_score += 2

            # 检查是否为教程、文档等教育类内容
            educational_keywords = [
                "教程",
                "文档",
                "学习",
                "指南",
                "手册",
                "参考",
                "api",
                "开发",
                "入门",
                "基础",
            ]
            if any(keyword in title for keyword in educational_keywords):
                relevance_score += 1

            # 过滤低相关性结果
            if relevance_score > 0:
                result["relevance_score"] = relevance_score
                filtered_results.append(result)

        # 按相关性排序
        filtered_results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        return filtered_results

    def get_suggestions(self, query: str) -> List[str]:
        """
        获取搜索建议

        Args:
            query: 搜索关键词

        Returns:
            搜索建议列表
        """
        return self.search_engine.get_suggestions(query)


# 全局搜索服务实例（使用Bing搜索，更稳定可靠）
search_service = SearchService(use_mock=False, use_simple_search=True)
