module.exports = function(eleventyConfig) {
  // 複製靜態資源
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("static/assets");

  // 設定語言支援
  eleventyConfig.addGlobalData("languages", ["en", "de"]);

  // 設定模板引擎
  eleventyConfig.setTemplateFormats([
    "md",
    "njk",
    "html"
  ]);

  // 設定輸入和輸出目錄
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["njk", "md", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk"
  };
}; 