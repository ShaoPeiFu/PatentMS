// jQuery功能演示和测试文件

$(document).ready(function () {
  console.log("PatentMS jQuery文件加载成功！");
  console.log("jQuery版本:", $.fn.jquery);

  // 1. 检查jQuery是否加载
  if (typeof jQuery !== "undefined") {
    console.log("✅ jQuery已成功加载");
  } else {
    console.log("❌ jQuery加载失败");
  }

  // 2. 鼠标悬停效果 - 为所有p标签添加红色效果
  $("p").hover(
    function () {
      $(this).css("color", "red");
    },
    function () {
      $(this).css("color", "");
    }
  );

  // 3. 点击效果 - 点击元素时改变背景色
  $(".clickable").click(function () {
    $(this).css("background-color", "yellow");
    setTimeout(() => {
      $(this).css("background-color", "");
    }, 1000);
  });

  // 4. 淡入淡出效果
  $(".fade-effect").hover(function () {
    $(this).fadeOut(200).fadeIn(200);
  });

  // 5. 滑动效果
  $(".slide-effect").click(function () {
    $(this).slideUp(300).slideDown(300);
  });

  // 6. 添加/删除CSS类
  $(".toggle-class").click(function () {
    $(this).toggleClass("highlight");
  });

  // 7. 修改文本内容
  $(".change-text").click(function () {
    var originalText = $(this).text();
    $(this).text("文本已更改！");
    setTimeout(() => {
      $(this).text(originalText);
    }, 2000);
  });

  // 8. 表单验证
  $('input[type="text"]').blur(function () {
    if ($(this).val().length < 3) {
      $(this).css("border-color", "red");
    } else {
      $(this).css("border-color", "green");
    }
  });

  // 9. AJAX示例（如果需要的话）
  $(".ajax-test").click(function () {
    $.ajax({
      url: "/api/test/",
      method: "GET",
      success: function (data) {
        console.log("AJAX请求成功:", data);
      },
      error: function (xhr, status, error) {
        console.log("AJAX请求失败:", error);
      },
    });
  });

  // 10. 动画效果
  $(".animate-effect").hover(
    function () {
      $(this).animate(
        {
          fontSize: "+=2px",
          opacity: 0.8,
        },
        200
      );
    },
    function () {
      $(this).animate(
        {
          fontSize: "-=2px",
          opacity: 1,
        },
        200
      );
    }
  );

  // 11. 键盘事件
  $(document).keydown(function (e) {
    if (e.ctrlKey && e.keyCode === 65) {
      // Ctrl+A
      console.log("全选快捷键被按下");
    }
  });

  // 12. 窗口大小改变事件
  $(window).resize(function () {
    console.log("窗口大小改变:", $(window).width(), "x", $(window).height());
  });

  // 13. 滚动事件
  $(window).scroll(function () {
    var scrollTop = $(window).scrollTop();
    if (scrollTop > 100) {
      $(".scroll-indicator").fadeIn();
    } else {
      $(".scroll-indicator").fadeOut();
    }
  });

  // 14. 动态添加元素
  $(".add-element").click(function () {
    var newElement = $('<div class="dynamic-element">动态添加的元素</div>');
    $(this).after(newElement);
  });

  // 15. 删除元素
  $(".remove-element").click(function () {
    $(this).remove();
  });

  console.log("所有jQuery功能已初始化完成！");
});

// 全局jQuery函数
function testJQuery() {
  alert("jQuery工作正常！版本: " + $.fn.jquery);
}

// 工具函数
function highlightElement(selector) {
  $(selector).css("background-color", "yellow");
  setTimeout(() => {
    $(selector).css("background-color", "");
  }, 2000);
}

$(document).ready(function () {
  $("#like_btn").click(function () {
    var categoryIdVar;
    categoryIdVar = $(this).attr("data-categoryid");

    $.get("/like_category/", { category_id: categoryIdVar }, function (data) {
      $("#like_count").html(data);
      $("#like_btn").hide();
    });
  });
  $("#search-input").keyup(function () {
    var query;
    query = $(this).val();

    $.get("/suggest/", { suggestion: query }, function (data) {
      $("#categories-listing").html(data);
    });
  });

  // 搜索功能
  $("#search-btn").click(function () {
    var query = $("#search-query").val();
    if (query.trim() === "") {
      alert("请输入搜索关键词");
      return;
    }

    // 模拟搜索结果（此处在日后应该调用真实的搜索API）
    var mockResults = [
      { title: query + " 教程", url: "https://example.com/tutorial" },
      { title: query + " 文档", url: "https://example.com/docs" },
      { title: query + " 指南", url: "https://example.com/guide" },
    ];

    displaySearchResults(mockResults);
  });

  // 显示搜索结果
  function displaySearchResults(results) {
    var html = '<div class="mt-3"><h4>搜索结果:</h4><ul class="list-group">';
    results.forEach(function (result) {
      html +=
        '<li class="list-group-item d-flex justify-content-between align-items-center">';
      html +=
        '<div><a href="' +
        result.url +
        '" target="_blank">' +
        result.title +
        "</a></div>";
      html +=
        '<button class="btn btn-success btn-sm add-page-btn" ' +
        'data-title="' +
        result.title +
        '" ' +
        'data-url="' +
        result.url +
        '">添加</button>';
      html += "</li>";
    });
    html += "</ul></div>";

    $("#search-results").html(html);
  }

  // 添加页面按钮事件（使用类选择器）
  $(document).on("click", ".add-page-btn", function () {
    var title = $(this).data("title");
    var url = $(this).data("url");
    var categoryId = $("body").data("category-id") || "1"; // 从页面获取分类ID

    console.log("添加页面:", title, url, categoryId);

    $.get(
      "/search_add_page/",
      {
        title: title,
        url: url,
        category_id: categoryId,
      },
      function (data) {
        $("#pages-container").html(data);
        $("#search-results").html(
          '<div class="alert alert-success">页面添加成功！</div>'
        );
      }
    ).fail(function (xhr, status, error) {
      alert("添加页面失败: " + error);
    });
  });
});
