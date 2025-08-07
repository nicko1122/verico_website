const yaml = require("js-yaml");
const fs = require("fs");
const path = require("path");

module.exports = () => {
  const languages = ["en", "de"];
  const contentData = {};
  
  const dataRoot = path.resolve(__dirname, 'content');

  // --- Homepage Data ---
  contentData.homepage = {};
  languages.forEach(lang => {
    const homepagePath = path.join(dataRoot, 'homepage', `${lang}.yml`);
    if (fs.existsSync(homepagePath)) {
      contentData.homepage[lang] = yaml.load(fs.readFileSync(homepagePath, "utf8"));
    }
  });

  // --- Contact Page Data ---
  contentData.contact = {};
  languages.forEach(lang => {
    const contactPath = path.join(dataRoot, 'contact', `${lang}.yml`);
    if (fs.existsSync(contactPath)) {
      contentData.contact[lang] = yaml.load(fs.readFileSync(contactPath, "utf8"));
    }
  });

  // --- Products Data ---
  contentData.products = {
    details: {},
    catalog: {}
  };

  // Catalog Data
  languages.forEach(lang => {
    const catalogPath = path.join(dataRoot, 'products', 'catalog', `${lang}.yml`);
    if (fs.existsSync(catalogPath)) {
      contentData.products.catalog[lang] = yaml.load(fs.readFileSync(catalogPath, "utf8"));
    }
  });
  
  // Details Data (Dynamically)
  const detailsPath = path.join(dataRoot, 'products', 'details');
  if (fs.existsSync(detailsPath)) {
    const productSlugs = fs.readdirSync(detailsPath).filter(file => {
      const filePath = path.join(detailsPath, file);
      return fs.statSync(filePath).isDirectory() && !file.startsWith('.');
    });

    productSlugs.forEach(productSlug => {
      const productKey = productSlug.replace(/-/g, '_');
      contentData.products.details[productKey] = {};
      languages.forEach(lang => {
        const productPath = path.join(detailsPath, productSlug, `${lang}.yml`);
        if (fs.existsSync(productPath)) {
          contentData.products.details[productKey][lang] = yaml.load(fs.readFileSync(productPath, "utf8"));
        }
      });
    });
  }

  return contentData;
};

