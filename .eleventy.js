module.exports = function(eleventyConfig) {
  // 輸入和輸出目錄
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addWatchTarget("src/assets");

  // 模板格式
  eleventyConfig.setTemplateFormats([
    "html",
    "md",
    "njk"
  ]);

  // 自定義過濾器：生成時間戳
  eleventyConfig.addFilter("timestamp", function() {
    return new Date().getTime();
  });

  // 動態生成產品詳情頁面
  eleventyConfig.addCollection("productPages", function(collectionApi) {
    const products = require('./src/_data/products.json');
    const pages = [];
    
    for (const [productId, product] of Object.entries(products.products)) {
      pages.push({
        url: `/products/${productId}/`,
        layout: "product-spec.njk",
        title: product.name,
        description: product.description,
        product: product,
        products: products.products
      });
    }
    
    return pages;
  });

  // 目錄結構
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    // 開發服務器選項
    serverOptions: {
      // 添加快取控制標頭
      headers: {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
      }
    }
  };
}; 