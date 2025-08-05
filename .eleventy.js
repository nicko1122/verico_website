const yaml = require("js-yaml");
const fs = require("fs");
const path = require("path");

module.exports = function(eleventyConfig) {
  // 複製靜態資源
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("static/assets");

  // 設定模板引擎
  eleventyConfig.setTemplateFormats([
    "html",
    "njk",
    "md"
  ]);

  // 設定預設 layout
  eleventyConfig.addGlobalData("layout", "layout.njk");

  // 設定語言
  const languages = ["en", "de"];

  // 為每個語言建立頁面
  languages.forEach(lang => {
    eleventyConfig.addGlobalData("lang", lang);
  });

  // 添加 absoluteUrl filter
  eleventyConfig.addFilter("absoluteUrl", function(url) {
    if (!url) return "";
    if (url.startsWith("http")) return url;
    return url;
  });

  // 添加 dump filter 用於調試
  eleventyConfig.addFilter("dump", function(obj) {
    return JSON.stringify(obj, null, 2);
  });

  // 明確配置 YAML 支援
  eleventyConfig.addDataExtension("yaml", contents => yaml.load(contents));
  eleventyConfig.addDataExtension("yml", contents => yaml.load(contents));

  // 設定輸出目錄
  eleventyConfig.addPassthroughCopy("src/assets");

  // 設定監視檔案
  eleventyConfig.addWatchTarget("src/assets/");

  // 數據處理邏輯
  eleventyConfig.addGlobalData("site", () => {
    const siteConfigPath = "src/_data/site/config.yml";
    if (fs.existsSync(siteConfigPath)) {
      return yaml.load(fs.readFileSync(siteConfigPath, "utf8"));
    }
    return {};
  });

  eleventyConfig.addGlobalData("navigation", () => {
    const navConfigPath = "src/_data/site/navigation.yml";
    if (fs.existsSync(navConfigPath)) {
      return yaml.load(fs.readFileSync(navConfigPath, "utf8"));
    }
    return {};
  });

  // 處理內容數據
  eleventyConfig.addGlobalData("content", () => {
    const contentData = {};
    
    // 處理首頁數據
    languages.forEach(lang => {
      const homepagePath = `src/_data/content/homepage/${lang}.yml`;
      if (fs.existsSync(homepagePath)) {
        if (!contentData.homepage) contentData.homepage = {};
        contentData.homepage[lang] = yaml.load(fs.readFileSync(homepagePath, "utf8"));
      }
    });

    // 處理聯繫頁面數據
    languages.forEach(lang => {
      const contactPath = `src/_data/content/contact/${lang}.yml`;
      if (fs.existsSync(contactPath)) {
        if (!contentData.contact) contentData.contact = {};
        contentData.contact[lang] = yaml.load(fs.readFileSync(contactPath, "utf8"));
      }
    });

    // 處理產品目錄數據
    languages.forEach(lang => {
      const productsPath = `src/_data/content/products/catalog/${lang}.yml`;
      if (fs.existsSync(productsPath)) {
        if (!contentData.products) contentData.products = {};
        contentData.products[lang] = yaml.load(fs.readFileSync(productsPath, "utf8"));
      }
    });

    // 處理產品詳情數據
    if (!contentData.products) contentData.products = {};
    if (!contentData.products.details) contentData.products.details = {};
    
    // 產品詳情頁面配置
    const productDetails = [
      // 所有產品將由自動化系統動態添加
    ];
    
    productDetails.forEach(productSlug => {
      languages.forEach(lang => {
        const productPath = `src/_data/content/products/details/${productSlug}/${lang}.yml`;
        if (fs.existsSync(productPath)) {
          if (!contentData.products.details[productSlug.replace(/-/g, '_')]) {
            contentData.products.details[productSlug.replace(/-/g, '_')] = {};
          }
          contentData.products.details[productSlug.replace(/-/g, '_')][lang] = yaml.load(fs.readFileSync(productPath, "utf8"));
        }
      });
    });

    return contentData;
  });

  // 為了向後兼容，保留舊的數據引用
  eleventyConfig.addGlobalData("homepageen", () => {
    const path = "src/_data/content/homepage/en.yml";
    if (fs.existsSync(path)) {
      return yaml.load(fs.readFileSync(path, "utf8"));
    }
    return {};
  });

  eleventyConfig.addGlobalData("homepagede", () => {
    const path = "src/_data/content/homepage/de.yml";
    if (fs.existsSync(path)) {
      return yaml.load(fs.readFileSync(path, "utf8"));
    }
    return {};
  });

  eleventyConfig.addGlobalData("contact", () => {
    const contactData = {};
    languages.forEach(lang => {
      const path = `src/_data/content/contact/${lang}.yml`;
      if (fs.existsSync(path)) {
        contactData[lang] = yaml.load(fs.readFileSync(path, "utf8"));
      }
    });
    return contactData;
  });

  eleventyConfig.addGlobalData("products", () => {
    const productsData = {};
    languages.forEach(lang => {
      const path = `src/_data/content/products/catalog/${lang}.yml`;
      if (fs.existsSync(path)) {
        productsData[lang] = yaml.load(fs.readFileSync(path, "utf8"));
      }
    });
    return productsData;
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["html", "njk", "md"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
    dataTemplateEngine: "njk"
  };
}; 