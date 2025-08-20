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

    // Create trendingProducts collection (unique, based on en block badge)
    eleventyConfig.addCollection("trendingProducts", function(collectionApi) {
        const productDataPath = path.join(__dirname, "src/_data/products");
        if (!fs.existsSync(productDataPath)) return [];
        const productFiles = fs.readdirSync(productDataPath).filter(file => file.endsWith('.yml'));
        const trending = [];
        const seen = new Set();
        const slugOptions = {
            replacement: '-',
            remove: /[&,+()$~%.'":*?<>{}]/g,
            lower: true
        };
        for (const file of productFiles) {
            const filePath = path.join(productDataPath, file);
            const content = fs.readFileSync(filePath, 'utf8');
            if (!content.trim()) continue;
            const data = yaml.load(content) || {};
            const en = data.en || {};
            if (en.badge !== 'trending') continue;
            const name = en.name || '';
            if (!name) continue;
            const de = data.de || {};
            const slugEn = slugify((en.name || '') || '', slugOptions);
            const slugDe = slugify((de.name || en.name || '') || '', slugOptions);
            // skip if no slug or already seen
            if ((!slugEn && !slugDe) || seen.has(slugEn) || seen.has(slugDe)) continue;
            const image = en.catalog_image || (en.images && en.images.length ? en.images[0] : null);
            if (!image) continue;
            if (slugEn) seen.add(slugEn);
            if (slugDe) seen.add(slugDe);
            // include both en and de names/urls and also provide common fields for templates
            const deName = (de && de.name) || name;
            const descEn = en.description || '';
            const descDe = (de && de.description) || descEn;
            const detailsEn = en.details || '';
            const detailsDe = (de && de.details) || detailsEn;
            const urlEn = `/${'en'}/products/${slugEn}/`;
            const urlDe = `/${'de'}/products/${slugDe}/`;
            trending.push({
                name: name,
                name_en: name,
                name_de: deName,
                description_en: descEn,
                description_de: descDe,
                details_en: detailsEn,
                details_de: detailsDe,
                image,
                url: urlEn,
                url_en: urlEn,
                url_de: urlDe,
                featured_rank: (typeof en.featured_rank === 'number') ? en.featured_rank : Infinity
            });
        }
        // sort by featured_rank (ascending), then by name_en
        trending.sort((a, b) => {
            if ((a.featured_rank || Infinity) !== (b.featured_rank || Infinity)) {
                return (a.featured_rank || Infinity) - (b.featured_rank || Infinity);
            }
            return (a.name_en || a.name || '').localeCompare(b.name_en || b.name || '');
        });
        return trending;
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

    // Cache-busting version filter for asset URLs
    const BUILD_VERSION = String(Math.floor(Date.now() / 1000));
    eleventyConfig.addFilter("v", (inputUrl) => {
        try {
            if (!inputUrl || typeof inputUrl !== 'string') return inputUrl;
            const urlPath = inputUrl;
            let rel = urlPath.startsWith('/') ? urlPath.slice(1) : urlPath;
            const srcPath = path.join(__dirname, 'src', rel);
            let v = BUILD_VERSION;
            if (fs.existsSync(srcPath)) {
                const stat = fs.statSync(srcPath);
                v = String(Math.floor(stat.mtimeMs));
            }
            return urlPath + (urlPath.includes('?') ? '&' : '?') + 'v=' + v;
        } catch (e) {
            return inputUrl;
        }
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
