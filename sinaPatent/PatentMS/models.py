from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
import unicodedata


def chinese_slugify(value):
    """
    自定义slugify函数，支持中文字符
    将中文字符转换为拼音或英文，如果无法转换则使用ID
    """
    if not value:
        return ""

    # 中文字符映射表（常用中文到英文的映射）
    chinese_to_english = {
        "你好": "ni-hao",
        "世界": "world",
        "中国": "china",
        "北京": "beijing",
        "上海": "shanghai",
        "广州": "guangzhou",
        "深圳": "shenzhen",
        "杭州": "hangzhou",
        "南京": "nanjing",
        "武汉": "wuhan",
        "成都": "chengdu",
        "西安": "xian",
        "重庆": "chongqing",
        "天津": "tianjin",
        "青岛": "qingdao",
        "大连": "dalian",
        "厦门": "xiamen",
        "苏州": "suzhou",
        "无锡": "wuxi",
        "宁波": "ningbo",
        "佛山": "foshan",
        "东莞": "dongguan",
        "中山": "zhongshan",
        "珠海": "zhuhai",
        "惠州": "huizhou",
        "江门": "jiangmen",
        "肇庆": "zhaoqing",
        "清远": "qingyuan",
        "韶关": "shaoguan",
        "河源": "heyuan",
        "梅州": "meizhou",
        "潮州": "chaozhou",
        "揭阳": "jieyang",
        "汕尾": "shanwei",
        "阳江": "yangjiang",
        "茂名": "maoming",
        "湛江": "zhanjiang",
        "云浮": "yunfu",
        "南宁": "nanning",
        "柳州": "liuzhou",
        "桂林": "guilin",
        "梧州": "wuzhou",
        "北海": "beihai",
        "防城港": "fangchenggang",
        "钦州": "qinzhou",
        "贵港": "guigang",
        "玉林": "yulin",
        "百色": "baise",
        "贺州": "hezhou",
        "河池": "hechi",
        "来宾": "laibin",
        "崇左": "chongzuo",
        "海口": "haikou",
        "三亚": "sanya",
        "三沙": "sansha",
        "儋州": "danzhou",
        "五指山": "wuzhishan",
        "琼海": "qionghai",
        "文昌": "wenchang",
        "万宁": "wanning",
        "东方": "dongfang",
        "定安": "dingan",
        "屯昌": "tunchang",
        "澄迈": "chengmai",
        "临高": "lingao",
        "白沙": "baisha",
        "昌江": "changjiang",
        "乐东": "ledong",
        "陵水": "lingshui",
        "保亭": "baoting",
        "琼中": "qiongzhong",
        "编程": "programming",
        "开发": "development",
        "技术": "technology",
        "学习": "learning",
        "教程": "tutorial",
        "文档": "documentation",
        "代码": "code",
        "项目": "project",
        "框架": "framework",
        "库": "library",
        "工具": "tools",
        "软件": "software",
        "应用": "application",
        "网站": "website",
        "网页": "webpage",
        "前端": "frontend",
        "后端": "backend",
        "数据库": "database",
        "服务器": "server",
        "客户端": "client",
        "移动端": "mobile",
        "桌面端": "desktop",
        "云服务": "cloud",
        "人工智能": "ai",
        "机器学习": "machine-learning",
        "深度学习": "deep-learning",
        "数据科学": "data-science",
        "大数据": "big-data",
        "区块链": "blockchain",
        "物联网": "iot",
        "网络安全": "cybersecurity",
        "算法": "algorithm",
        "数据结构": "data-structure",
        "设计模式": "design-pattern",
        "测试": "testing",
        "部署": "deployment",
        "运维": "operations",
        "监控": "monitoring",
        "日志": "logging",
        "性能": "performance",
        "优化": "optimization",
        "重构": "refactoring",
        "版本控制": "version-control",
        "持续集成": "ci",
        "持续部署": "cd",
        "微服务": "microservices",
        "容器化": "containerization",
        "虚拟化": "virtualization",
        "分布式": "distributed",
        "高可用": "high-availability",
        "负载均衡": "load-balancing",
        "缓存": "caching",
        "消息队列": "message-queue",
        "搜索引擎": "search-engine",
        "推荐系统": "recommendation-system",
        "电商": "ecommerce",
        "社交": "social",
        "游戏": "gaming",
        "教育": "education",
        "医疗": "healthcare",
        "金融": "finance",
        "物流": "logistics",
        "制造": "manufacturing",
        "农业": "agriculture",
        "环保": "environmental",
        "能源": "energy",
        "交通": "transportation",
        "建筑": "construction",
        "房地产": "real-estate",
        "旅游": "tourism",
        "娱乐": "entertainment",
        "媒体": "media",
        "新闻": "news",
        "体育": "sports",
        "音乐": "music",
        "电影": "movie",
        "书籍": "books",
        "艺术": "art",
        "设计": "design",
        "摄影": "photography",
        "视频": "video",
        "音频": "audio",
        "图像": "image",
        "文本": "text",
        "语音": "speech",
        "自然语言": "nlp",
        "计算机视觉": "computer-vision",
        "语音识别": "speech-recognition",
        "机器翻译": "machine-translation",
        "情感分析": "sentiment-analysis",
        "知识图谱": "knowledge-graph",
        "语义分析": "semantic-analysis",
        "信息抽取": "information-extraction",
        "问答系统": "qa-system",
        "聊天机器人": "chatbot",
        "虚拟助手": "virtual-assistant",
        "智能客服": "intelligent-customer-service",
        "智能家居": "smart-home",
        "自动驾驶": "autonomous-driving",
        "无人机": "drone",
        "机器人": "robot",
        "传感器": "sensor",
        "摄像头": "camera",
        "雷达": "radar",
        "激光": "laser",
        "卫星": "satellite",
        "导航": "navigation",
        "定位": "positioning",
        "地图": "map",
        "地理信息": "gis",
        "遥感": "remote-sensing",
        "气象": "meteorology",
        "海洋": "ocean",
        "地质": "geology",
        "生物": "biology",
        "化学": "chemistry",
        "物理": "physics",
        "数学": "mathematics",
        "统计": "statistics",
        "概率": "probability",
        "线性代数": "linear-algebra",
        "微积分": "calculus",
        "离散数学": "discrete-mathematics",
        "图论": "graph-theory",
        "组合数学": "combinatorics",
        "数论": "number-theory",
        "几何": "geometry",
        "拓扑": "topology",
        "分析": "analysis",
        "代数": "algebra",
        "群论": "group-theory",
        "环论": "ring-theory",
        "域论": "field-theory",
        "模论": "module-theory",
        "表示论": "representation-theory",
        "李群": "lie-group",
        "李代数": "lie-algebra",
        "微分几何": "differential-geometry",
        "代数几何": "algebraic-geometry",
        "复分析": "complex-analysis",
        "实分析": "real-analysis",
        "泛函分析": "functional-analysis",
        "调和分析": "harmonic-analysis",
        "傅里叶分析": "fourier-analysis",
        "小波分析": "wavelet-analysis",
        "变分法": "calculus-of-variations",
        "最优控制": "optimal-control",
        "动态规划": "dynamic-programming",
        "博弈论": "game-theory",
        "决策论": "decision-theory",
        "运筹学": "operations-research",
        "优化理论": "optimization-theory",
        "凸优化": "convex-optimization",
        "非凸优化": "non-convex-optimization",
        "随机优化": "stochastic-optimization",
        "多目标优化": "multi-objective-optimization",
        "约束优化": "constrained-optimization",
        "无约束优化": "unconstrained-optimization",
        "梯度下降": "gradient-descent",
        "牛顿法": "newton-method",
        "拟牛顿法": "quasi-newton-method",
        "共轭梯度": "conjugate-gradient",
        "信赖域": "trust-region",
        "内点法": "interior-point-method",
        "单纯形法": "simplex-method",
        "分支定界": "branch-and-bound",
        "割平面": "cutting-plane",
        "列生成": "column-generation",
        "拉格朗日松弛": "lagrangian-relaxation",
        "对偶理论": "duality-theory",
        "灵敏度分析": "sensitivity-analysis",
        "鲁棒优化": "robust-optimization",
        "随机规划": "stochastic-programming",
        "模糊规划": "fuzzy-programming",
        "区间规划": "interval-programming",
        "目标规划": "goal-programming",
        "数据包络分析": "data-envelopment-analysis",
        "层次分析法": "analytic-hierarchy-process",
        "网络分析": "network-analysis",
        "图算法": "graph-algorithms",
        "最短路径": "shortest-path",
        "最小生成树": "minimum-spanning-tree",
        "最大流": "maximum-flow",
        "最小割": "minimum-cut",
        "匹配": "matching",
        "着色": "coloring",
        "覆盖": "covering",
        "支配": "domination",
        "独立集": "independent-set",
        "团": "clique",
        "连通性": "connectivity",
        "平面图": "planar-graph",
        "树": "tree",
        "森林": "forest",
        "二分图": "bipartite-graph",
        "有向图": "directed-graph",
        "无向图": "undirected-graph",
        "加权图": "weighted-graph",
        "多重图": "multigraph",
        "超图": "hypergraph",
        "随机图": "random-graph",
        "小世界网络": "small-world-network",
        "无标度网络": "scale-free-network",
        "社交网络": "social-network",
        "复杂网络": "complex-network",
        "网络科学": "network-science",
        "系统科学": "systems-science",
        "控制论": "cybernetics",
        "信息论": "information-theory",
        "编码理论": "coding-theory",
        "密码学": "cryptography",
        "数字签名": "digital-signature",
        "公钥密码": "public-key-cryptography",
        "对称密码": "symmetric-cryptography",
        "哈希函数": "hash-function",
        "随机数生成": "random-number-generation",
        "零知识证明": "zero-knowledge-proof",
        "同态加密": "homomorphic-encryption",
        "多方计算": "secure-multi-party-computation",
        "量子密码": "quantum-cryptography",
        "后量子密码": "post-quantum-cryptography",
        "侧信道攻击": "side-channel-attack",
        "差分攻击": "differential-attack",
        "线性攻击": "linear-attack",
        "代数攻击": "algebraic-attack",
        "生日攻击": "birthday-attack",
        "中间人攻击": "man-in-the-middle-attack",
        "重放攻击": "replay-attack",
        "字典攻击": "dictionary-attack",
        "暴力攻击": "brute-force-attack",
        "彩虹表": "rainbow-table",
        "盐值": "salt",
        "密钥派生": "key-derivation",
        "密钥交换": "key-exchange",
        "密钥管理": "key-management",
        "证书": "certificate",
        "公钥基础设施": "pki",
        "数字证书": "digital-certificate",
        "证书颁发机构": "ca",
        "证书撤销": "certificate-revocation",
        "在线证书状态协议": "ocsp",
        "证书透明度": "certificate-transparency",
        "域名验证": "domain-validation",
        "组织验证": "organization-validation",
        "扩展验证": "extended-validation",
        "通配符证书": "wildcard-certificate",
        "多域名证书": "multi-domain-certificate",
        "统一通信证书": "unified-communications-certificate",
        "代码签名": "code-signing",
        "时间戳": "timestamp",
        "不可否认性": "non-repudiation",
        "完整性": "integrity",
        "机密性": "confidentiality",
        "可用性": "availability",
        "认证": "authentication",
        "授权": "authorization",
        "审计": "audit",
        "合规": "compliance",
        "风险管理": "risk-management",
        "安全评估": "security-assessment",
        "渗透测试": "penetration-testing",
        "漏洞扫描": "vulnerability-scanning",
        "入侵检测": "intrusion-detection",
        "入侵防御": "intrusion-prevention",
        "防火墙": "firewall",
        "虚拟专用网络": "vpn",
        "网络地址转换": "nat",
        "端口转发": "port-forwarding",
        "负载均衡": "load-balancing",
        "内容分发网络": "cdn",
        "域名系统": "dns",
        "动态主机配置协议": "dhcp",
        "简单网络管理协议": "snmp",
        "网络时间协议": "ntp",
        "简单邮件传输协议": "smtp",
        "邮局协议": "pop",
        "互联网消息访问协议": "imap",
        "超文本传输协议": "http",
        "超文本传输安全协议": "https",
        "文件传输协议": "ftp",
        "安全文件传输协议": "sftp",
        "安全外壳协议": "ssh",
        "远程登录": "telnet",
        "远程桌面协议": "rdp",
        "虚拟网络计算": "vnc",
        "网络文件系统": "nfs",
        "服务器消息块": "smb",
        "通用互联网文件系统": "cifs",
        "网络附加存储": "nas",
        "存储区域网络": "san",
        "直接附加存储": "das",
        "云存储": "cloud-storage",
        "对象存储": "object-storage",
        "块存储": "block-storage",
        "文件存储": "file-storage",
        "数据库": "database",
        "关系数据库": "relational-database",
        "非关系数据库": "non-relational-database",
        "文档数据库": "document-database",
        "键值数据库": "key-value-database",
        "列族数据库": "column-family-database",
        "图数据库": "graph-database",
        "时序数据库": "time-series-database",
        "内存数据库": "in-memory-database",
        "分布式数据库": "distributed-database",
        "主从复制": "master-slave-replication",
        "读写分离": "read-write-splitting",
        "分片": "sharding",
        "分区": "partitioning",
        "索引": "index",
        "事务": "transaction",
        "锁": "lock",
        "死锁": "deadlock",
        "并发控制": "concurrency-control",
        "一致性": "consistency",
        "隔离性": "isolation",
        "持久性": "durability",
        "原子性": "atomicity",
        "acid": "acid",
        "base": "base",
        "cap定理": "cap-theorem",
        "最终一致性": "eventual-consistency",
        "强一致性": "strong-consistency",
        "弱一致性": "weak-consistency",
        "因果一致性": "causal-consistency",
        "会话一致性": "session-consistency",
        "单调读": "monotonic-reads",
        "单调写": "monotonic-writes",
        "读写一致性": "read-your-writes",
        "前缀一致性": "prefix-consistency",
        "线性化": "linearizability",
        "顺序一致性": "sequential-consistency",
        "处理器一致性": "processor-consistency",
        "释放一致性": "release-consistency",
        "入口一致性": "entry-consistency",
        "延迟一致性": "lazy-consistency",
        "即时一致性": "eager-consistency",
        "乐观并发控制": "optimistic-concurrency-control",
        "悲观并发控制": "pessimistic-concurrency-control",
        "多版本并发控制": "mvcc",
        "时间戳排序": "timestamp-ordering",
        "两阶段锁定": "two-phase-locking",
        "严格两阶段锁定": "strict-two-phase-locking",
        "保守两阶段锁定": "conservative-two-phase-locking",
        "树协议": "tree-protocol",
        "图协议": "graph-protocol",
        "验证协议": "validation-protocol",
        "提交协议": "commit-protocol",
        "两阶段提交": "two-phase-commit",
        "三阶段提交": "three-phase-commit",
        "paxos": "paxos",
        "raft": "raft",
        "zab": "zab",
        "拜占庭容错": "byzantine-fault-tolerance",
        "实用拜占庭容错": "practical-byzantine-fault-tolerance",
        "联邦拜占庭协议": "federated-byzantine-agreement",
        "权益证明": "proof-of-stake",
        "工作量证明": "proof-of-work",
        "委托权益证明": "delegated-proof-of-stake",
        "实用权益证明": "practical-proof-of-stake",
        "混合共识": "hybrid-consensus",
        "分片共识": "sharded-consensus",
        "分层共识": "layered-consensus",
        "异步共识": "asynchronous-consensus",
        "同步共识": "synchronous-consensus",
        "部分同步共识": "partially-synchronous-consensus",
        "最终性": "finality",
        "活性": "liveness",
        "安全性": "safety",
        "容错性": "fault-tolerance",
        "可用性": "availability",
        "可靠性": "reliability",
        "可扩展性": "scalability",
        "性能": "performance",
        "吞吐量": "throughput",
        "延迟": "latency",
        "带宽": "bandwidth",
        "容量": "capacity",
        "效率": "efficiency",
        "优化": "optimization",
        "调优": "tuning",
        "监控": "monitoring",
        "日志": "logging",
        "追踪": "tracing",
        "指标": "metrics",
        "告警": "alerting",
        "仪表板": "dashboard",
        "可视化": "visualization",
        "分析": "analytics",
        "报告": "reporting",
        "仪表板": "dashboard",
        "仪表板": "dashboard",
    }

    # 首先尝试直接映射
    if value in chinese_to_english:
        return chinese_to_english[value]

    # 尝试部分匹配
    for chinese, english in chinese_to_english.items():
        if chinese in value:
            # 替换中文部分
            result = value.replace(chinese, english)
            # 继续处理剩余部分
            result = slugify(result)
            return result

    # 如果无法映射，使用原始slugify
    result = slugify(value)

    # 如果结果为空，生成一个基于ID的slug
    if not result:
        # 这里我们暂时返回一个默认值，实际使用时会在save方法中处理
        return "category"

    return result


class Category(models.Model):
    """专利分类模型"""

    name = models.CharField(max_length=128, unique=True, verbose_name="分类名称")
    views = models.IntegerField(default=0, verbose_name="浏览次数")
    likes = models.IntegerField(default=0, verbose_name="点赞次数")
    slug = models.SlugField(blank=True, unique=True, verbose_name="URL别名")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["-likes", "-views", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """保存时自动生成slug并验证数据"""
        # 验证数据
        if self.views < 0:
            self.views = 0
        if self.likes < 0:
            self.likes = 0

        # 生成slug
        if not self.slug:
            self.slug = chinese_slugify(self.name)

            # 确保slug唯一性
            if self.slug == "category":
                # 如果是默认值，使用ID生成唯一slug
                counter = 1
                while Category.objects.filter(slug=f"category-{counter}").exists():
                    counter += 1
                self.slug = f"category-{counter}"
            else:
                # 检查slug唯一性
                counter = 1
                original_slug = self.slug
                while (
                    Category.objects.filter(slug=self.slug).exclude(id=self.id).exists()
                ):
                    self.slug = f"{original_slug}-{counter}"
                    counter += 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """获取分类的绝对URL"""
        return reverse("show_category", args=[self.slug])

    def get_pages_count(self):
        """获取分类下的页面数量"""
        return self.page_set.count()

    def get_popular_pages(self, limit=5):
        """获取分类下的热门页面"""
        return self.page_set.order_by("-views")[:limit]

    def increment_views(self):
        """增加浏览次数"""
        self.views += 1
        self.save(update_fields=["views"])

    def increment_likes(self):
        """增加点赞次数"""
        self.likes += 1
        self.save(update_fields=["likes"])

    def clean(self):
        """模型验证"""
        if len(self.name.strip()) < 2:
            raise ValidationError("分类名称至少需要2个字符")

        if self.views < 0:
            raise ValidationError("浏览次数不能为负数")

        if self.likes < 0:
            raise ValidationError("点赞次数不能为负数")


class Page(models.Model):
    """专利页面模型"""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="所属分类"
    )
    title = models.CharField(max_length=128, verbose_name="页面标题")
    url = models.URLField(verbose_name="页面URL")
    views = models.IntegerField(default=0, verbose_name="浏览次数")

    class Meta:
        verbose_name = "页面"
        verbose_name_plural = "页面"
        ordering = ["-views", "title"]
        unique_together = ["category", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """保存时验证数据"""
        if self.views < 0:
            self.views = 0
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """获取页面的绝对URL"""
        return reverse("goto") + f"?page_id={self.id}"

    def increment_views(self):
        """增加浏览次数"""
        self.views += 1
        self.save(update_fields=["views"])

    def clean(self):
        """模型验证"""
        if len(self.title.strip()) < 2:
            raise ValidationError("页面标题至少需要2个字符")

        if not self.url.startswith(("http://", "https://")):
            raise ValidationError("URL必须以http://或https://开头")

        if self.views < 0:
            raise ValidationError("浏览次数不能为负数")

    @property
    def is_popular(self):
        """判断是否为热门页面（浏览次数超过10次）"""
        return self.views > 10


class UserProfile(models.Model):
    """用户档案模型"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    website = models.URLField(blank=True, verbose_name="个人网站")
    picture = models.ImageField(
        upload_to="profile_images", blank=True, verbose_name="头像"
    )

    class Meta:
        verbose_name = "用户档案"
        verbose_name_plural = "用户档案"

    def __str__(self):
        return f"{self.user.username}的档案"

    def get_absolute_url(self):
        """获取用户档案的绝对URL"""
        return reverse("profile", args=[self.user.username])

    def get_full_name(self):
        """获取用户全名"""
        return self.user.get_full_name() or self.user.username

    def get_avatar_url(self):
        """获取头像URL"""
        if self.picture:
            return self.picture.url
        return None

    def get_user_pages_count(self):
        """获取用户添加的页面数量"""
        return Page.objects.filter(category__user=self.user).count()

    def clean(self):
        """模型验证"""
        if self.website and not self.website.startswith(("http://", "https://")):
            raise ValidationError("网站地址必须以http://或https://开头")
