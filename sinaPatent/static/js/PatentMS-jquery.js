// jQuery功能文件

$(document).ready(function () {
  console.log("PatentMS jQuery文件加载成功！");
  console.log("jQuery版本:", $.fn.jquery);

  // 检查jQuery是否加载
  if (typeof jQuery !== "undefined") {
    console.log("✅ jQuery已成功加载");
  } else {
    console.log("❌ jQuery加载失败");
  }

  console.log("jQuery功能已初始化完成！");
});

$(document).ready(function () {
  // 移除重复的点赞按钮事件绑定，避免与category.html中的事件冲突
  // $("#like_btn").click(function () {
  //   var categoryIdVar;
  //   categoryIdVar = $(this).attr("data-categoryid");

  //   $.get("/like_category/", { category_id: categoryIdVar }, function (data) {
  //     $("#like_count").html(data);
  //     $("#like_btn").hide();
  //   });
  // });

  $("#search-input").keyup(function () {
    var query;
    query = $(this).val();

    $.get("/suggest/", { suggestion: query }, function (data) {
      $("#categories-listing").html(data);
    });
  });

  // 搜索功能 - 调用真实的搜索API
  $("#search-btn").click(function () {
    var query = $("#search-query").val();
    if (query.trim() === "") {
      alert("请输入搜索关键词");
      return;
    }

    // 显示加载状态
    $("#search-loading").show();
    $("#search-results").empty();

    // 获取分类ID
    var categoryId = $("[data-category-id]").data("category-id");

    // 调用真实的搜索API
    $.ajax({
      url: "/api/search/",
      method: "GET",
      data: {
        query: query,
        category_id: categoryId,
      },
      success: function (data) {
        $("#search-loading").hide();

        if (data.success && data.results.length > 0) {
          displaySearchResults(data.results);
        } else {
          $("#search-results").html(
            '<div class="alert alert-info">' +
              '<i class="fas fa-info-circle me-2"></i> 没有找到相关结果，请尝试其他关键词' +
              "</div>"
          );
        }
      },
      error: function (xhr, status, error) {
        $("#search-loading").hide();
        console.error("搜索失败:", error);

        var errorMsg = "搜索失败，请稍后重试";
        if (xhr.responseJSON && xhr.responseJSON.error) {
          errorMsg = xhr.responseJSON.error;
        }

        $("#search-results").html(
          '<div class="alert alert-danger">' +
            '<i class="fas fa-exclamation-triangle me-2"></i> ' +
            errorMsg +
            "</div>"
        );
      },
    });
  });

  // 显示搜索结果
  function displaySearchResults(results) {
    var html = '<div class="mt-3">';
    html +=
      '<h5 class="mb-3"><i class="fas fa-list me-2"></i>搜索结果 (' +
      results.length +
      "个结果)</h5>";
    html += '<div class="list-group">';

    results.forEach(function (result, index) {
      var existsClass = result.exists ? "list-group-item-secondary" : "";
      var existsText = result.exists
        ? '<span class="badge bg-secondary ms-2">已存在</span>'
        : "";

      html +=
        '<div class="list-group-item ' + existsClass + ' search-result-item">';
      html += '<div class="d-flex justify-content-between align-items-start">';
      html += '<div class="flex-grow-1">';
      html += '<h6 class="mb-1">';
      html +=
        '<a href="' +
        result.url +
        '" target="_blank" class="text-primary fw-bold">' +
        result.title +
        "</a>";
      html += existsText;
      html += "</h6>";
      html += '<p class="mb-1 text-muted small">' + result.abstract + "</p>";
      html +=
        '<small class="text-muted"><i class="fas fa-link me-1"></i>' +
        result.url +
        "</small>";
      html += "</div>";

      if (!result.exists) {
        html +=
          '<button class="btn btn-success btn-sm add-page-btn ms-3" ' +
          'data-title="' +
          result.title.replace(/"/g, "&quot;") +
          '" ' +
          'data-url="' +
          result.url +
          '">' +
          '<i class="fas fa-plus me-1"></i> 添加</button>';
      }

      html += "</div>";
      html += "</div>";
    });

    html += "</div>";
    html += '<div class="mt-3">';
    html += '<small class="text-muted">';
    html +=
      '<i class="fas fa-info-circle me-1"></i> 搜索结果来自真实搜索，点击"添加"按钮将页面添加到当前分类';
    html += "</small>";
    html += "</div>";
    html += "</div>";

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
