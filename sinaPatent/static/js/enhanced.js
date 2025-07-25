// 增强的JavaScript功能 - 新浪专利管理系统

// 粒子效果
function createParticles() {
  const particlesContainer = document.createElement("div");
  particlesContainer.className = "particles";
  document.body.appendChild(particlesContainer);

  for (let i = 0; i < 50; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    particle.style.left = Math.random() * 100 + "%";
    particle.style.animationDelay = Math.random() * 15 + "s";
    particle.style.animationDuration = Math.random() * 10 + 10 + "s";
    particlesContainer.appendChild(particle);
  }
}

// 打字机效果
function typeWriter(element, text, speed = 100) {
  let i = 0;
  element.innerHTML = "";

  function type() {
    if (i < text.length) {
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }

  type();
}

// 滚动进度条
function createScrollProgress() {
  const progressBar = document.createElement("div");
  progressBar.className = "scroll-progress";
  progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
  document.body.appendChild(progressBar);

  window.addEventListener("scroll", () => {
    const scrollTop = window.pageYOffset;
    const docHeight = document.body.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    progressBar.style.width = scrollPercent + "%";
  });
}

// 平滑滚动
function smoothScrollTo(target) {
  const element = document.querySelector(target);
  if (element) {
    element.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }
}

// 卡片翻转效果
function addCardFlipEffect() {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-8px) rotateY(5deg)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0) rotateY(0deg)";
    });
  });
}

// 按钮波纹效果
function addRippleEffect() {
  const buttons = document.querySelectorAll(".btn");

  buttons.forEach((button) => {
    button.addEventListener("click", function (e) {
      const ripple = document.createElement("span");
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;

      this.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });
}

// 添加波纹动画CSS
const rippleCSS = `
@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}`;

// 搜索建议增强
function enhanceSearchSuggestions() {
  const searchInput = document.getElementById("search-query");
  if (searchInput) {
    searchInput.addEventListener("focus", function () {
      this.parentElement.style.transform = "scale(1.02)";
      this.parentElement.style.boxShadow =
        "0 0 0 0.2rem rgba(99, 102, 241, 0.25)";
    });

    searchInput.addEventListener("blur", function () {
      this.parentElement.style.transform = "scale(1)";
      this.parentElement.style.boxShadow = "none";
    });
  }
}

// 页面加载动画
function addPageLoadAnimation() {
  const elements = document.querySelectorAll("[data-aos]");
  elements.forEach((element, index) => {
    element.style.opacity = "0";
    element.style.transform = "translateY(30px)";

    setTimeout(() => {
      element.style.transition = "all 0.6s ease";
      element.style.opacity = "1";
      element.style.transform = "translateY(0)";
    }, index * 100);
  });
}

// 数字计数动画
function animateNumbers() {
  const numbers = document.querySelectorAll(".animate-number");
  numbers.forEach((number) => {
    const target = parseInt(number.textContent);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      number.textContent = Math.floor(current);
    }, 16);
  });
}

// 主题切换增强
function enhanceThemeToggle() {
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const html = document.documentElement;
      const icon = this.querySelector("i");

      // 添加切换动画
      this.style.transform = "scale(0.8)";
      setTimeout(() => {
        this.style.transform = "scale(1)";
      }, 150);

      if (html.getAttribute("data-bs-theme") === "dark") {
        html.setAttribute("data-bs-theme", "light");
        icon.className = "fas fa-moon";
        this.title = "切换到深色模式";
        showToast("info", "主题切换", "已切换到浅色模式");
      } else {
        html.setAttribute("data-bs-theme", "dark");
        icon.className = "fas fa-sun";
        this.title = "切换到浅色模式";
        showToast("info", "主题切换", "已切换到深色模式");
      }
    });
  }
}

// 增强的Toast通知
function showToast(type, title, message, duration = 5000) {
  const toastContainer =
    document.querySelector(".toast-container") || document.createElement("div");

  if (!document.querySelector(".toast-container")) {
    toastContainer.className =
      "toast-container position-fixed bottom-0 end-0 p-3";
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement("div");
  toast.className = "toast show";
  toast.style.cssText = `
        border-radius: 12px;
        border: none;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.95);
        margin-bottom: 0.5rem;
        animation: slideInRight 0.3s ease;
    `;

  const iconMap = {
    success: "fas fa-check-circle",
    error: "fas fa-exclamation-circle",
    warning: "fas fa-exclamation-triangle",
    info: "fas fa-info-circle",
  };

  const bgMap = {
    success: "bg-success",
    error: "bg-danger",
    warning: "bg-warning",
    info: "bg-info",
  };

  toast.innerHTML = `
        <div class="toast-header ${bgMap[type]} text-white">
            <i class="${iconMap[type]} me-2"></i>
            <strong class="me-auto">${title}</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;

  toastContainer.appendChild(toast);

  // 自动隐藏
  setTimeout(() => {
    toast.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, duration);
}

// 键盘快捷键
function addKeyboardShortcuts() {
  document.addEventListener("keydown", function (e) {
    // Ctrl/Cmd + K: 聚焦搜索框
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      const searchInput =
        document.getElementById("search-query") ||
        document.getElementById("search-input");
      if (searchInput) {
        searchInput.focus();
      }
    }

    // Ctrl/Cmd + T: 切换主题
    if ((e.ctrlKey || e.metaKey) && e.key === "t") {
      e.preventDefault();
      const themeToggle = document.getElementById("theme-toggle");
      if (themeToggle) {
        themeToggle.click();
      }
    }

    // Escape: 关闭所有模态框和通知
    if (e.key === "Escape") {
      const toasts = document.querySelectorAll(".toast");
      toasts.forEach((toast) => {
        toast.style.animation = "slideOutRight 0.3s ease";
        setTimeout(() => toast.remove(), 300);
      });
    }
  });
}

// 性能监控
function addPerformanceMonitoring() {
  window.addEventListener("load", function () {
    const loadTime =
      performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log(`页面加载时间: ${loadTime}ms`);

    if (loadTime > 3000) {
      showToast("warning", "性能提示", "页面加载较慢，请检查网络连接");
    }
  });
}

// 错误处理
function addErrorHandling() {
  window.addEventListener("error", function (e) {
    console.error("页面错误:", e.error);
    showToast("error", "系统错误", "发生了一个错误，请刷新页面重试");
  });
}

// 初始化所有功能
document.addEventListener("DOMContentLoaded", function () {
  // 添加CSS动画
  const style = document.createElement("style");
  style.textContent = `
        ${rippleCSS}
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        .scroll-progress {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            z-index: 9999;
            transition: width 0.1s ease;
        }
    `;
  document.head.appendChild(style);

  // 初始化功能
  createParticles();
  createScrollProgress();
  addCardFlipEffect();
  addRippleEffect();
  enhanceSearchSuggestions();
  addPageLoadAnimation();
  enhanceThemeToggle();
  addKeyboardShortcuts();
  addPerformanceMonitoring();
  addErrorHandling();

  // 延迟执行数字动画
  setTimeout(animateNumbers, 1000);

  console.log("🎉 增强功能已加载完成！");
});

// 导出函数供其他脚本使用
window.EnhancedUI = {
  showToast,
  smoothScrollTo,
  typeWriter,
  animateNumbers,
};
