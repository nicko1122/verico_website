const yaml = require("js-yaml");
const fs = require("fs");
const path = require("path");
const slugify = require("slugify");

module.exports = function(eleventyConfig) {
    // Pass through assets
    eleventyConfig.addPassthroughCopy("src/assets");

    // Add YAML support for data files
    eleventyConfig.addDataExtension("yml", contents => yaml.load(contents));

    // Create a custom collection for products
    eleventyConfig.addCollection("allProducts", function(collectionApi) {
        const productDataPath = path.join(__dirname, "src/_data/products");
        if (!fs.existsSync(productDataPath)) {
            console.warn("[Eleventy] Products data directory not found at:", productDataPath);
            return [];
        }
        const productFiles = fs.readdirSync(productDataPath).filter(file => file.endsWith(".yml"));
        
        const products = [];
        for (const file of productFiles) {
            const filePath = path.join(productDataPath, file);
            const content = fs.readFileSync(filePath, "utf8");

            // Skip empty files
            if (!content.trim()) {
                console.warn(`[Eleventy] Skipping empty product file: ${file}`);
                continue;
            }

            const data = yaml.load(content);

            // Skip if data is not a valid object or doesn't contain language keys
            if (!data || typeof data !== 'object' || !data.en || !data.de) {
                console.warn(`[Eleventy] Skipping invalid or incomplete product data in file: ${file}`);
                continue;
            }
            
            // Add both language versions to the collection
            products.push({ lang: 'en', ...data });
            products.push({ lang: 'de', ...data });
        }
        return products;
    });

    // Register the slugify filter
    eleventyConfig.addFilter("slug", (input) => {
        if (typeof input !== 'string') {
            console.error(`[Slugify Error] Expected a string but got a ${typeof input}. Value:`, input);
            return 'invalid-slug';
        }
        const options = {
            replacement: '-',
            remove: /[&,+()$~%.'":*?<>{}]/g,
            lower: true
        };
        return slugify(input, options);
    });

    return {
        dir: {
            input: "src",
            includes: "_includes",
            data: "_data",
            output: "_site"
        },
        templateFormats: ["md", "njk", "html"],
        markdownTemplateEngine: "njk",
        htmlTemplateEngine: "njk",
        dataTemplateEngine: "njk",
    };
};
